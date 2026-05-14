"""
B1 Hören TTS audio generator — Phase 1b.

Reads the JSON scripts produced by horen_script_generator.py and renders each
to an MP3. Single-speaker scripts (Teil 1, Teil 2) are one TTS call. Multi-
speaker scripts (Teil 3, Teil 4) are split into speaker turns, each rendered
separately with a per-speaker voice, then stitched together with ffmpeg using
a short silence between turns.

Idempotent: re-runs skip scripts whose MP3 already exists. Use --force to
regenerate.

Provider abstraction
--------------------
TTS is behind a small `TTSProvider` interface. Each provider exposes a name,
a voice_map from abstract voice_role → concrete voice id, a default voice,
and a synthesize() method. Adding a new provider (Azure, ElevenLabs, Polly,
Piper) is a ~30-line class that goes in PROVIDERS. The CLI's --provider flag
selects which one is used.

Default provider is edge_tts (free, native German Azure Neural voices via the
Edge browser's TTS endpoint). Swap to openai for paid tts-1-hd by passing
--provider openai.

Usage:
    # Render every script in seed/draft_horen_scripts.json with edge_tts (free)
    python -m agents._tools.horen_audio_generator

    # First 3 only (smoke test)
    python -m agents._tools.horen_audio_generator --max 3

    # Different provider
    python -m agents._tools.horen_audio_generator --provider openai

    # Different input file
    python -m agents._tools.horen_audio_generator --input ~/my_scripts.json

    # Force regenerate all
    python -m agents._tools.horen_audio_generator --force

Requires:
    - ffmpeg on PATH (used to concat multi-speaker turns).
    - For edge_tts:   the edge-tts package (pinned in requirements.txt). No API key.
    - For openai:     the openai package + OPENAI_API_KEY in the environment.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TURN_PAUSE_SECONDS = 0.4

# Edge TTS sometimes returns empty audio under load (the "No audio was received"
# error). Retry the websocket call with exponential backoff before giving up.
EDGE_TTS_MAX_ATTEMPTS = 4
EDGE_TTS_BACKOFF_SECONDS = (1.0, 2.0, 4.0)  # delays between attempts 1→2, 2→3, 3→4


def _resolve_ffmpeg() -> str:
    """Find ffmpeg without depending on the runtime $PATH.

    uvicorn is often launched from an IDE / service manager that doesn't
    inherit the user's shell PATH, so a bare `"ffmpeg"` in subprocess.run
    raises FileNotFoundError even when `which ffmpeg` works in the terminal.
    Resolve once at import time, falling back to known Homebrew locations.
    """
    found = shutil.which("ffmpeg")
    if found:
        return found
    for candidate in ("/usr/local/bin/ffmpeg", "/opt/homebrew/bin/ffmpeg", "/usr/bin/ffmpeg"):
        if Path(candidate).exists():
            return candidate
    # Fall through — let subprocess raise its own clearer error if/when used,
    # so importing this module never crashes the process at boot.
    return "ffmpeg"


FFMPEG_BIN = _resolve_ffmpeg()


# ── TTS Provider abstraction ──────────────────────────────────────────────────


class TTSProvider:
    """Minimal interface every TTS backend implements.

    Adding a new provider:
      1. Subclass TTSProvider.
      2. Set `name`, `voice_map` (voice_role → concrete voice id), `default_voice`.
      3. Implement synthesize(text, voice_role, out_path).
      4. Register in PROVIDERS at the bottom of this file.
    """

    name: ClassVar[str] = ""
    voice_map: ClassVar[dict[str, str]] = {}
    default_voice: ClassVar[str] = ""

    def __init__(self) -> None:
        """Override to lazy-import the underlying SDK and validate config."""

    def voice_for(self, voice_role: str) -> str:
        return self.voice_map.get(voice_role, self.default_voice)

    def synthesize(self, text: str, voice_role: str, out_path: Path) -> None:
        """Render `text` to an MP3 at `out_path` with the voice for `voice_role`."""
        raise NotImplementedError


class EdgeTTSProvider(TTSProvider):
    """Microsoft Edge TTS — free, native German Azure Neural voices.

    Uses the same neural voices as paid Azure Cognitive Speech, accessed via the
    Edge browser's TTS endpoint. No API key required. Sample rate 24 kHz mono
    MP3, matching the silence file used during stitching.
    """

    name = "edge_tts"
    # NOTE: Microsoft retires Edge TTS voices periodically. Validate against
    # `edge-tts --list-voices | grep de-DE` if a voice starts returning
    # "No audio was received" — that's the failure mode for a removed voice.
    # de-DE-JonasNeural was removed in 2026 and replaced here with KillianNeural.
    voice_map = {
        "female_neutral_formal": "de-DE-KatjaNeural",   # clear female, news-anchor / station-announcement register
        "male_neutral_formal":   "de-DE-ConradNeural",  # deeper male, authoritative
        "female_casual":         "de-DE-AmalaNeural",   # warm female, friendly conversation
        "male_casual":           "de-DE-KillianNeural", # conversational male (replaces de-DE-JonasNeural)
    }
    default_voice = "de-DE-KatjaNeural"

    def __init__(self) -> None:
        import edge_tts  # lazy — optional dep
        self._edge_tts = edge_tts

    def synthesize(self, text: str, voice_role: str, out_path: Path) -> None:
        text = (text or "").strip()
        if not text:
            raise ValueError("Edge TTS called with empty text")

        voice = self.voice_for(voice_role)
        last_err: Exception | None = None
        for attempt in range(1, EDGE_TTS_MAX_ATTEMPTS + 1):
            try:
                communicate = self._edge_tts.Communicate(text, voice)
                asyncio.run(communicate.save(str(out_path)))
                # Edge TTS sometimes "succeeds" but writes a zero-byte file when
                # the upstream returns no audio frames — treat that as a retry.
                if out_path.exists() and out_path.stat().st_size > 1024:
                    return
                last_err = RuntimeError(
                    f"Edge TTS produced an empty/short file ({out_path.stat().st_size if out_path.exists() else 0} bytes)"
                )
            except Exception as e:
                last_err = e

            if attempt < EDGE_TTS_MAX_ATTEMPTS:
                backoff = EDGE_TTS_BACKOFF_SECONDS[attempt - 1]
                logger.warning(
                    "Edge TTS attempt %d/%d failed for %d-char text (%s); retrying in %.1fs",
                    attempt, EDGE_TTS_MAX_ATTEMPTS, len(text), last_err, backoff,
                )
                time.sleep(backoff)

        raise RuntimeError(
            f"Edge TTS failed after {EDGE_TTS_MAX_ATTEMPTS} attempts for "
            f"{len(text)}-char text (voice={voice}): {last_err}"
        )


class OpenAITTSProvider(TTSProvider):
    """OpenAI tts-1-hd. Paid (~$0.030 / 1K input chars). Slight English accent
    on German output but very natural prosody."""

    name = "openai"
    voice_map = {
        "female_neutral_formal": "nova",
        "male_neutral_formal":   "onyx",
        "female_casual":         "shimmer",
        "male_casual":           "echo",
    }
    default_voice = "alloy"

    def __init__(self) -> None:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY not set in environment")
        from openai import OpenAI  # lazy — optional dep
        self._client = OpenAI()

    def synthesize(self, text: str, voice_role: str, out_path: Path) -> None:
        voice = self.voice_for(voice_role)
        with self._client.audio.speech.with_streaming_response.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
        ) as response:
            response.stream_to_file(out_path)


PROVIDERS: dict[str, type[TTSProvider]] = {
    EdgeTTSProvider.name: EdgeTTSProvider,
    OpenAITTSProvider.name: OpenAITTSProvider,
}


# ── Speaker tag parsing ───────────────────────────────────────────────────────


def parse_turns(script: str, expected_first_names: list[str]) -> list[tuple[str, str]]:
    """Parse a multi-speaker script into [(speaker_first_name, text), ...].

    Accepts speaker tags in either form:
        Anna: Hallo, wie geht's?
        [Anna]: Hallo, wie geht's?
        Anna (Moderatorin): Willkommen.
    The first matching first name from `expected_first_names` is the canonical
    speaker for that turn. Turns can span multiple lines — text up to the next
    speaker tag (or end of script) is the turn body. Returns [] if no tags are
    found — caller decides how to handle that.
    """
    if not expected_first_names:
        return []
    name_alt = "|".join(re.escape(n) for n in expected_first_names)
    tag_re = re.compile(
        rf"^\s*\[?\s*({name_alt})(?:\s*\([^)]*\))?\s*\]?\s*:\s*",
        re.MULTILINE,
    )
    matches = list(tag_re.finditer(script))
    if not matches:
        return []
    turns = []
    for i, m in enumerate(matches):
        speaker = m.group(1)
        text_start = m.end()
        text_end = matches[i + 1].start() if i + 1 < len(matches) else len(script)
        # Collapse newlines/extra whitespace inside a turn — TTS shouldn't pause
        # mid-turn just because the source script wrapped to a new line.
        text = " ".join(script[text_start:text_end].split()).strip()
        if text:
            turns.append((speaker, text))
    return turns


# ── ffmpeg stitching ──────────────────────────────────────────────────────────


def _make_silence(seconds: float, out: Path) -> None:
    """Generate a short MP3 of silence at 24 kHz mono, matching what Azure /
    OpenAI TTS produce — so concat doesn't re-sample."""
    subprocess.run(
        [
            FFMPEG_BIN, "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", str(seconds),
            "-c:a", "libmp3lame", "-q:a", "4",
            str(out),
        ],
        check=True,
    )


def stitch_turns(turn_files: list[Path], out: Path, pause_seconds: float) -> None:
    """Concat per-turn MP3s with `pause_seconds` of silence between each."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        silence = tmp / "silence.mp3"
        _make_silence(pause_seconds, silence)

        concat_list = tmp / "concat.txt"
        with concat_list.open("w") as f:
            for i, turn_file in enumerate(turn_files):
                f.write(f"file '{turn_file.absolute()}'\n")
                if i < len(turn_files) - 1:
                    f.write(f"file '{silence.absolute()}'\n")

        # Re-encode to keep MP3 timing accurate with mixed-source frames.
        subprocess.run(
            [
                FFMPEG_BIN, "-y", "-loglevel", "error",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_list),
                "-c:a", "libmp3lame", "-q:a", "4",
                str(out),
            ],
            check=True,
        )


# ── Rendering ─────────────────────────────────────────────────────────────────


def render_script(provider: TTSProvider, item: dict, out_path: Path) -> dict:
    """Render one script item to one MP3 at `out_path`. Returns a small dict
    summary (voices used, turn count) for logging."""
    script_text = item.get("script") or ""
    if not script_text.strip():
        raise ValueError("empty 'script' field")

    speakers = item.get("speakers") or []
    if not isinstance(speakers, list) or not speakers:
        # Fallback — treat as single-speaker with the provider's default voice
        provider.synthesize(script_text, "", out_path)
        return {"speakers": 0, "turns": 1, "voices": [provider.default_voice]}

    # Single speaker: one TTS call, no stitching needed.
    if len(speakers) == 1:
        role = speakers[0].get("voice_role", "")
        provider.synthesize(script_text, role, out_path)
        return {"speakers": 1, "turns": 1, "voices": [provider.voice_for(role)]}

    # Multi-speaker: parse turns, render each, stitch.
    speaker_first_names = [s["name"].split()[0] for s in speakers if s.get("name")]
    role_by_name = {
        s["name"].split()[0]: s.get("voice_role", "")
        for s in speakers
        if s.get("name")
    }
    turns = parse_turns(script_text, speaker_first_names)
    if not turns:
        raise ValueError(
            f"could not parse any turns from a {len(speakers)}-speaker script "
            f"(expected names: {speaker_first_names})"
        )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        turn_files: list[Path] = []
        voices_used: list[str] = []
        for i, (speaker, text) in enumerate(turns):
            role = role_by_name.get(speaker, "")
            voices_used.append(provider.voice_for(role))
            turn_path = tmp / f"turn_{i:03d}.mp3"
            provider.synthesize(text, role, turn_path)
            turn_files.append(turn_path)
        stitch_turns(turn_files, out_path, TURN_PAUSE_SECONDS)

    return {"speakers": len(speakers), "turns": len(turns), "voices": voices_used}


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Render B1 Hören scripts to MP3.")
    parser.add_argument(
        "--provider",
        default="edge_tts",
        choices=list(PROVIDERS.keys()),
        help="TTS provider. Default 'edge_tts' (free, native German). Use 'openai' for paid tts-1-hd.",
    )
    parser.add_argument(
        "--input",
        default="",
        help="Path to draft_horen_scripts.json. Default: agents/deutsch_b1_horen/knowledge_base/seed/draft_horen_scripts.json",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Where MP3s go. Default: backend/uploads/horen/ (the same dir the API serves).",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=0,
        help="Maximum number of scripts to render (0 = all). Useful for smoke tests.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-render even if the target MP3 already exists.",
    )
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ERROR: ffmpeg not found on PATH (required for multi-speaker stitching).", file=sys.stderr)
        return 1

    backend_root = Path(__file__).parent.parent.parent  # backend/
    input_path = Path(args.input) if args.input else (
        backend_root / "agents" / "deutsch_b1_horen" / "knowledge_base" / "seed" / "draft_horen_scripts.json"
    )
    output_dir = Path(args.output_dir) if args.output_dir else (
        backend_root / "uploads" / "horen"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        print("       Run horen_script_generator first to produce scripts.", file=sys.stderr)
        return 1

    try:
        scripts = json.loads(input_path.read_text())
    except json.JSONDecodeError as e:
        print(f"ERROR: {input_path} is not valid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(scripts, list):
        print(f"ERROR: expected a JSON array at the top of {input_path}", file=sys.stderr)
        return 1

    if args.max > 0:
        scripts = scripts[: args.max]

    try:
        provider = PROVIDERS[args.provider]()
    except Exception as e:
        print(f"ERROR initialising provider '{args.provider}': {e}", file=sys.stderr)
        return 1

    print(f"Provider: {provider.name}   →   {output_dir}")
    print(f"Rendering {len(scripts)} script(s)…")
    rendered = 0
    skipped = 0
    failed = 0
    for idx, item in enumerate(scripts):
        teil = item.get("teil", "x")
        context = item.get("context", "") or "?"
        out_path = output_dir / f"teil{teil}_{idx:03d}.mp3"

        if out_path.exists() and not args.force:
            print(f"  [{idx + 1:>3}] SKIP (exists): {out_path.name}")
            skipped += 1
            continue

        try:
            summary = render_script(provider, item, out_path)
        except Exception as e:
            print(f"  [{idx + 1:>3}] FAIL Teil {teil} ({context}): {e}", file=sys.stderr)
            failed += 1
            continue

        size_kb = out_path.stat().st_size // 1024
        print(
            f"  [{idx + 1:>3}] OK   Teil {teil} ({context}): "
            f"{summary['speakers']}-speaker, {summary['turns']} turn(s), "
            f"voices={summary['voices']}, {size_kb}KB → {out_path.name}"
        )
        rendered += 1

    print()
    print(f"Rendered: {rendered}, Skipped: {skipped}, Failed: {failed}")
    print(f"Output:   {output_dir}")
    if rendered or skipped:
        print()
        print("Listen on macOS:")
        print(f"  open {output_dir}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
