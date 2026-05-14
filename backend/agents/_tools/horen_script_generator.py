"""
Offline B1 Hören script generator (Phase 1a — text only, no TTS).

Generates sample audio scripts using Gemini and writes them to JSON for human
review. Lets you validate B1 vocabulary / register / comprehension grounding
without spending TTS credits. The new API endpoint
(`POST /horen/{slug}/quiz`) uses the same generation logic via
`agents.deutsch_b1_horen.services.generation`.

Usage:
    # Default: 3 Teil-1 sample scripts → seed/draft_horen_scripts.json
    python -m agents._tools.horen_script_generator

    # Generate 5 Teil-3 (two-speaker dialogue) samples
    python -m agents._tools.horen_script_generator --teil 3 --n 5

    # Custom output path
    python -m agents._tools.horen_script_generator --teil 1 --n 3 --output ~/horen_review.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from agents.deutsch_b1_horen.services.generation import (
    generate_one_script,
    teil_name,
)

load_dotenv()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate B1 Hören sample scripts (text only, Phase 1a)."
    )
    parser.add_argument(
        "--teil",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Which Teil to generate (1=short monologues, 2=presentation, 3=dialogue, 4=panel).",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=3,
        help="Number of sample scripts to generate (default 3).",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Output JSON path. Default: agents/deutsch_b1_horen/knowledge_base/seed/draft_horen_scripts.json",
    )
    args = parser.parse_args()

    out_path = Path(args.output) if args.output else (
        Path(__file__).parent.parent
        / "deutsch_b1_horen"
        / "knowledge_base"
        / "seed"
        / "draft_horen_scripts.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating {args.n} sample script(s) for {teil_name(args.teil)}…", flush=True)

    new_items: list[dict] = []
    failed = 0
    for i in range(args.n):
        print(f"  [{i + 1}/{args.n}] calling Gemini…", flush=True)
        try:
            item = generate_one_script(args.teil)
        except json.JSONDecodeError as e:
            print(f"    JSON parse failed: {e}", file=sys.stderr)
            failed += 1
            continue
        except Exception as e:
            print(f"    Gemini call failed: {e}", file=sys.stderr)
            failed += 1
            continue

        item["_generated_at"] = date.today().isoformat()
        item["_review_status"] = "pending"
        new_items.append(item)

    existing: list = []
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text())
            if not isinstance(existing, list):
                print(f"WARNING: {out_path} not a list; resetting", file=sys.stderr)
                existing = []
        except json.JSONDecodeError:
            print(f"WARNING: {out_path} unreadable JSON; resetting", file=sys.stderr)

    combined = existing + new_items
    out_path.write_text(json.dumps(combined, indent=2, ensure_ascii=False))

    print()
    print(f"Generated {len(new_items)} script(s) in this run ({failed} failed).")
    print(f"File now contains {len(combined)} total scripts at:")
    print(f"  {out_path}")
    print()
    print("Next steps:")
    print("  1. Open the JSON file and read each 'script' field aloud.")
    print("  2. If quality is acceptable, render audio with horen_audio_generator.")
    print("  3. Or skip this entirely and use the new /horen/<slug>/quiz endpoint")
    print("     which generates scripts + audio + persists as a Quiz in one shot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
