"""
End-to-end A2 Hören generation pipeline.

Mirrors agents/deutsch_b1_horen/services/generation.py with A2-specific
constants (instruction text, play limits, agent imports). Kept as a sibling
copy rather than a shared library because the per-Teil German instructions
and play rules genuinely differ between A2 and B1, and future evolution per
level may diverge further.

Two-step pipeline:
  1. Gemini -> JSON script(s) matching the Teil's format spec
  2. TTS provider -> MP3 file(s) per script (single-speaker = 1 call,
     multi-speaker = stitched per-turn via ffmpeg)

The output of `generate_session` is a manifest dict ready to drop into
`Quiz.content`: a flat `questions` array (each question references the
audio segment it belongs to), so the existing `calculate_quiz_score`
function works without modification.
"""

from __future__ import annotations

import json
import logging
import os
import random
import re
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

from agents.deutsch_a2_horen import (
    DEUTSCH_A2_HOREN_CHAPTERS,
    INSTRUCTIONS,
    get_chapter_by_slug,
    topics_for_teil,
)

# Bumped above the default to give the model real prosody/wording variety
# within an assigned topic. Topic variety itself is handled by random
# selection from TOPICS_BY_TEIL — temperature alone won't rescue a model
# that keeps picking the same default scenario.
GEMINI_TEMPERATURE = 1.1

# How many audio items make up a complete session per Teil (matches the real
# Goethe-Zertifikat A2 Hören exam structure — Teil 1 is 5 short independent
# texts; Teile 2/3/4 are each one longer audio with multiple comprehension
# items inside).
ITEMS_PER_SESSION = {1: 5, 2: 1, 3: 1, 4: 1}

# Goethe-Zertifikat A2 Hören play rules — Teil 1, 3, and 4 play twice; Teil 2
# plays once. (B1 differs: only Teil 4 plays twice on B1.)
PLAY_LIMIT_PER_TEIL = {1: 2, 2: 1, 3: 2, 4: 2}

INSTRUCTIONS_PER_TEIL = {
    1: "Sie hören fünf kurze Mitteilungen. Sie hören jede Mitteilung zweimal. Wählen Sie für jede Aufgabe die richtige Antwort.",
    2: "Sie hören eine kurze Präsentation. Sie hören den Text einmal. Wählen Sie für jede Aufgabe die richtige Antwort.",
    3: "Sie hören ein Gespräch. Sie hören das Gespräch zweimal. Entscheiden Sie, ob die Aussagen richtig oder falsch sind.",
    4: "Sie hören eine Diskussion. Sie hören die Diskussion zweimal. Wer sagt was?",
}


# ── Step 1: Gemini script generation ──────────────────────────────────────────


def _extract_json(text: str) -> dict:
    """Pull a JSON object out of raw model output, stripping any code fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
    payload = match.group(1) if match else cleaned
    return json.loads(payload)


def _teil_chapter_slug(teil: int) -> str:
    return next(
        (c["slug"] for c in DEUTSCH_A2_HOREN_CHAPTERS if c["slug"].startswith(f"teil_{teil}_")),
        f"teil_{teil}",
    )


def teil_name(teil: int) -> str:
    """Human-readable name for a Teil, sourced from the chapters definition."""
    chapter = get_chapter_by_slug(_teil_chapter_slug(teil))
    return chapter["name"] if chapter else f"Teil {teil}"


def pick_topic_for_teil(teil: int) -> str:
    """Return a random topic from the catalog for this Teil. Empty string if no
    catalog is defined (in which case the model falls back to picking from the
    topic hints inside the format spec)."""
    pool = topics_for_teil(teil)
    return random.choice(pool) if pool else ""


def build_script_prompt(teil: int, chosen_topic: Optional[str] = None) -> str:
    chapter = get_chapter_by_slug(_teil_chapter_slug(teil))
    if not chapter:
        raise ValueError(f"unknown teil {teil}")

    if chosen_topic:
        topic_block = f"""## Assigned Topic for THIS Generation

Write the script about exactly this scenario — do NOT pick a different topic:

  **{chosen_topic}**

The format spec below mentions a topic catalog as guidance. For THIS request,
the topic is fixed above. Use the format spec for length, voices, register, and
comprehension-item shape, but write the content about the assigned topic.
"""
    else:
        topic_block = (
            "Pick a topic from the topic catalog in the format spec that fits the spec."
        )

    return f"""{INSTRUCTIONS}

---

## This Request

Generate ONE complete item for {chapter['name']}.

{topic_block}

## Format Spec

{chapter['content']}

Return ONLY the JSON object described in the schema for Teil {teil}. No markdown
fence, no prose, no explanation outside the JSON.
"""


def _gemini_client():
    """Lazy-construct a Gemini client. Raises if GEMINI_API_KEY is missing."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    from google import genai
    return genai.Client(api_key=api_key)


def generate_one_script(teil: int, client=None, *, chosen_topic: Optional[str] = None) -> dict:
    """Single Gemini call returning one parsed script JSON for the given Teil.

    If `chosen_topic` is None, picks one at random from the Teil's topic catalog
    (TOPICS_BY_TEIL) so successive calls don't all default to the same scenario.
    Pass `chosen_topic=""` to disable injection and let the model choose.
    """
    client = client or _gemini_client()
    if chosen_topic is None:
        chosen_topic = pick_topic_for_teil(teil)
    prompt = build_script_prompt(teil, chosen_topic=chosen_topic)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"temperature": GEMINI_TEMPERATURE},
    )
    return _extract_json(response.text)


def generate_scripts(teil: int, n: int, client=None) -> list[dict]:
    """Generate `n` independent scripts for the same Teil."""
    client = client or _gemini_client()
    return [generate_one_script(teil, client) for _ in range(n)]


# ── Step 2: TTS rendering ─────────────────────────────────────────────────────


def render_audio_for_script(provider, script: dict, out_path: Path) -> dict:
    """Render one script item to an MP3. Delegates to the provider abstraction
    in `agents._tools.horen_audio_generator`."""
    from agents._tools.horen_audio_generator import render_script as _render
    return _render(provider, script, out_path)


def get_provider(provider_name: str = "edge_tts"):
    from agents._tools.horen_audio_generator import PROVIDERS
    if provider_name not in PROVIDERS:
        raise ValueError(
            f"unknown provider '{provider_name}'. Available: {list(PROVIDERS.keys())}"
        )
    return PROVIDERS[provider_name]()


# ── End-to-end: scripts + audio + manifest ────────────────────────────────────


def _flatten_questions(script: dict, teil: int, audio_url: str) -> list[dict]:
    """Convert a script's comprehension items into a flat list of questions
    that match the Quiz.content shape used by `calculate_quiz_score`. Every
    question carries its own `audio_url` so the runner can group questions
    by audio segment for playback."""
    topic = teil_name(teil)
    audio_context = script.get("context", "") or ""
    out: list[dict] = []

    if teil == 1:
        q = script.get("question") or {}
        if not q:
            return out
        out.append({
            "topic": topic,
            "stem": q.get("stem", ""),
            "options": q.get("options", []),
            "correct_option_index": q.get("correct_index", 0),
            "explanation": q.get("explanation", ""),
            "audio_url": audio_url,
            "audio_context": audio_context,
        })
        return out

    if teil == 2:
        for q in script.get("questions") or []:
            out.append({
                "topic": topic,
                "stem": q.get("stem", ""),
                "options": q.get("options", []),
                "correct_option_index": q.get("correct_index", 0),
                "explanation": q.get("explanation", ""),
                "audio_url": audio_url,
                "audio_context": audio_context,
            })
        return out

    if teil == 3:
        # 5 richtig/falsch items at A2 (vs 7 at B1)
        for q in script.get("questions") or []:
            answer_idx = 0 if (q.get("answer") or "").lower().startswith("richt") else 1
            out.append({
                "topic": topic,
                "stem": q.get("stem", ""),
                "options": ["Richtig", "Falsch"],
                "correct_option_index": answer_idx,
                "explanation": q.get("explanation", ""),
                "audio_url": audio_url,
                "audio_context": audio_context,
            })
        return out

    if teil == 4:
        # 5 'who said what' MCQs at A2 (vs 8 at B1)
        for q in script.get("questions") or []:
            out.append({
                "topic": topic,
                "stem": q.get("stem", ""),
                "options": q.get("options", []),
                "correct_option_index": q.get("correct_index", 0),
                "explanation": q.get("explanation", ""),
                "audio_url": audio_url,
                "audio_context": audio_context,
            })
        return out

    return out


def generate_session(
    teil: int,
    audio_dir: Path,
    *,
    provider_name: str = "edge_tts",
    audio_url_prefix: str = "/static/horen",
    progress=None,
) -> dict:
    """Generate a complete A2 Hören session: scripts + audio + manifest.

    Args:
        teil: which Teil (1–4).
        audio_dir: directory where MP3s are written.
        provider_name: TTS provider key from the PROVIDERS dict.
        audio_url_prefix: URL prefix that the StaticFiles mount serves the
                         audio dir under.
        progress: optional callable `progress(stage: str, current: int, total: int)`
                  invoked at each step so callers can surface progress UX.

    Returns:
        A manifest dict ready to drop into Quiz.content. Same shape as B1.
    """
    if teil not in ITEMS_PER_SESSION:
        raise ValueError(f"teil must be 1–4, got {teil}")

    audio_dir.mkdir(parents=True, exist_ok=True)
    n_items = ITEMS_PER_SESSION[teil]

    if progress:
        progress("scripts", 0, n_items)
    scripts = generate_scripts(teil, n_items)
    if progress:
        progress("scripts", n_items, n_items)

    provider = get_provider(provider_name)

    audio_segments: list[dict] = []
    flat_questions: list[dict] = []
    for i, script in enumerate(scripts):
        if progress:
            progress("audio", i, n_items)
        audio_filename = f"{uuid.uuid4().hex}.mp3"
        audio_path = audio_dir / audio_filename
        render_audio_for_script(provider, script, audio_path)
        audio_url = f"{audio_url_prefix}/{audio_filename}"

        audio_segments.append({
            "audio_url": audio_url,
            "context": script.get("context", "") or "",
            "duration_seconds": script.get("estimated_duration_seconds", 25),
        })
        flat_questions.extend(_flatten_questions(script, teil, audio_url))

    if progress:
        progress("audio", n_items, n_items)

    return {
        "teil": teil,
        "teil_name": teil_name(teil),
        "instructions": INSTRUCTIONS_PER_TEIL.get(teil, ""),
        "play_limit": PLAY_LIMIT_PER_TEIL.get(teil, 1),
        "audio_segments": audio_segments,
        "questions": flat_questions,
    }


def session_title(teil: int) -> str:
    """Default title for a generated single-Teil A2 Hören Quiz row (legacy)."""
    return f"German A2 Hören — {teil_name(teil)}"


def full_exam_title() -> str:
    """Default title for a full 4-Teil A2 exam Quiz row."""
    return "German A2 Hören — Vollständige Prüfung"


# ── Full exam: all 4 Teile bundled into one Quiz ──────────────────────────────


def generate_full_exam(
    audio_dir: Path,
    *,
    provider_name: str = "edge_tts",
    audio_url_prefix: str = "/static/horen",
    progress=None,
) -> dict:
    """Generate a complete 4-Teil A2 Hören exam matching the real Goethe-Zertifikat
    A2 format. Returns a manifest with each Teil as a section AND a flat
    `questions` array spanning all Teile so `calculate_quiz_score` works
    unchanged.

    Performance: all 4 Teile are generated in parallel via a thread pool.
    Generation is I/O-bound (Gemini HTTP + Edge TTS WebSocket + ffmpeg
    subprocesses release the GIL during waits) so threads give us the full
    speedup. End-to-end time stays within Cloudflare's 100s timeout.

    Args:
        audio_dir: where to write the MP3s.
        provider_name: TTS provider key (default "edge_tts").
        audio_url_prefix: URL prefix for the StaticFiles mount.
        progress: optional callable `progress(stage, current, total)` invoked
                  once per Teil completion.

    Returns:
        Manifest dict shaped as:
          { kind: "full_exam",
            teile: [ {teil, teil_name, instructions, play_limit,
                      audio_segments, questions}, ...×4 ],
            questions: [...flat across all Teile, each carrying its `teil`...] }
    """
    teile = (1, 2, 3, 4)

    def _gen_one(t: int) -> tuple[int, dict]:
        return t, generate_session(
            t,
            audio_dir,
            provider_name=provider_name,
            audio_url_prefix=audio_url_prefix,
        )

    sections_by_teil: dict[int, dict] = {}
    completed = 0
    with ThreadPoolExecutor(max_workers=len(teile)) as pool:
        futures = [pool.submit(_gen_one, t) for t in teile]
        for fut in futures:
            t, section = fut.result()
            sections_by_teil[t] = section
            completed += 1
            if progress:
                progress("teil", completed, len(teile))
            logger.info("A2 Hören exam: Teil %d done (%d/%d)", t, completed, len(teile))

    teile_payloads: list[dict] = []
    flat_questions: list[dict] = []
    for t in teile:
        section = sections_by_teil[t]
        teile_payloads.append(section)
        for q in section["questions"]:
            flat_questions.append({**q, "teil": t})

    return {
        "kind": "full_exam",
        "teile": teile_payloads,
        "questions": flat_questions,
    }
