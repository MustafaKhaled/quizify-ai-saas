"""
End-to-end A2 Lesen generation pipeline.

Mirrors the B1 Lesen generation module structurally with A2-specific
constants. The output manifest follows the same `kind: full_lesen_exam`
shape so both levels can share the frontend play page (which dispatches
on the per-Teil `layout` field rather than the level-specific Teil number).

Key A2 deltas vs B1:
  - 4 Teile, 20 items total (vs 5 Teile, 30 items at B1)
  - Teil 2 is a building/directory + MCQ (no B1 equivalent)
  - Teil 4 ad-matching uses pool of 6 (a–f) with 'X' no-match marker
    (vs B1 Teil 3 with pool of 10 (a–j) and '0' no-match marker)
  - Teil 4 has 5 situations (vs B1 Teil 3 with 7)
"""

from __future__ import annotations

import json
import logging
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

logger = logging.getLogger(__name__)

from agents.deutsch_a2_lesen import (
    DEUTSCH_A2_LESEN_CHAPTERS,
    INSTRUCTIONS,
    get_chapter_by_slug,
    topics_for_teil,
)

GEMINI_TEMPERATURE = 1.1

# Real Goethe-Zertifikat A2 Lesen item counts per Teil (5/5/5/5 = 20 total).
ITEMS_PER_TEIL = {1: 5, 2: 5, 3: 5, 4: 5}

INSTRUCTIONS_PER_TEIL = {
    1: "Lesen Sie den Text und die Aufgaben. Wählen Sie für jede Aufgabe die richtige Antwort.",
    2: "Lesen Sie den Wegweiser und die Aufgaben. Wo finden Sie die gesuchten Dinge? Wählen Sie für jede Aufgabe das richtige Stockwerk.",
    3: "Lesen Sie die E-Mail und die Aufgaben. Wählen Sie für jede Aufgabe die richtige Antwort.",
    4: "Lesen Sie die Anzeigen a–f und die Situationen 1–5. Welche Anzeige passt zu welcher Situation? Schreiben Sie für jede Situation den passenden Buchstaben in das Feld. Für eine Situation gibt es keine passende Anzeige. Schreiben Sie hier 'X'. Sie können jede Anzeige nur einmal verwenden.",
}

# Layout discriminator written into each section. The frontend play page
# dispatches on this so both A2 and B1 (and future levels) reuse the same
# template renderers without per-Teil-number branching.
LAYOUT_PER_TEIL = {
    1: "passage_questions",   # newspaper article + 5 MCQ
    2: "passage_questions",   # directory rendered as pre-line passage + 5 MCQ
    3: "passage_questions",   # email + 5 MCQ
    4: "letter_matching",     # 6 ads + 5 letter inputs
}

# A2-specific letter-matching pool spec used for validation + frontend hints.
A2_LETTER_POOL_LETTERS = list("abcdef")
A2_NO_MATCH_MARKER = "X"


# ── Prompt + Gemini ───────────────────────────────────────────────────────────


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
        (c["slug"] for c in DEUTSCH_A2_LESEN_CHAPTERS if c["slug"].startswith(f"teil_{teil}_")),
        f"teil_{teil}",
    )


def teil_name(teil: int) -> str:
    chapter = get_chapter_by_slug(_teil_chapter_slug(teil))
    return chapter["name"] if chapter else f"Teil {teil}"


def pick_topic_for_teil(teil: int) -> str:
    pool = topics_for_teil(teil)
    return random.choice(pool) if pool else ""


def build_script_prompt(teil: int, chosen_topic: Optional[str] = None) -> str:
    chapter = get_chapter_by_slug(_teil_chapter_slug(teil))
    if not chapter:
        raise ValueError(f"unknown teil {teil}")

    if chosen_topic:
        topic_block = f"""## Assigned Topic for THIS Generation

Write the item about exactly this scenario — do NOT pick a different topic:

  **{chosen_topic}**

The format spec below mentions a topic catalog as guidance. For THIS request,
the topic is fixed above. Use the format spec for length, structure, and
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
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    from google import genai
    return genai.Client(api_key=api_key)


def generate_one_teil(teil: int, client=None, *, chosen_topic: Optional[str] = None) -> dict:
    """Single Gemini call returning one parsed Teil JSON."""
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


# ── Teil-4 (matching) composition validation ──────────────────────────────────
# A2 specs: 6 ads (a–f), 5 questions, exactly one 'X', non-X letters unique.


def _teil4_violations(payload: dict) -> list[str]:
    violations: list[str] = []
    pool = payload.get("ad_pool") or {}
    ads = pool.get("ads") or []
    letters = [a.get("letter") for a in ads]
    if sorted(letters) != A2_LETTER_POOL_LETTERS:
        violations.append(f"ad_pool.ads must have exactly letters a–f, got {letters}")

    questions = payload.get("questions") or []
    if len(questions) != 5:
        violations.append(f"expected 5 questions, got {len(questions)}")

    correct_letters = [(q.get("correct_letter") or "").lower() for q in questions]
    no_match_lower = A2_NO_MATCH_MARKER.lower()
    no_match_count = sum(1 for c in correct_letters if c == no_match_lower)
    if no_match_count != 1:
        violations.append(f"expected exactly one correct_letter == '{A2_NO_MATCH_MARKER}', got {no_match_count}")

    non_match = [c for c in correct_letters if c != no_match_lower]
    if len(non_match) != len(set(non_match)):
        violations.append(f"correct_letter values (excluding '{A2_NO_MATCH_MARKER}') must be unique, got {non_match}")

    invalid = [c for c in non_match if c not in A2_LETTER_POOL_LETTERS]
    if invalid:
        violations.append(f"correct_letter values must be a–f or '{A2_NO_MATCH_MARKER}', got invalid {invalid}")

    return violations


def _generate_teil4_with_validation(client) -> dict:
    last_payload: dict | None = None
    for attempt in (1, 2):
        payload = generate_one_teil(4, client)
        violations = _teil4_violations(payload)
        if not violations:
            return payload
        logger.warning(
            "A2 Lesen Teil 4 attempt %d had composition violations: %s",
            attempt, violations,
        )
        last_payload = payload
    return last_payload  # type: ignore[return-value]


# ── Flatten per-Teil payloads ────────────────────────────────────────────────


def _flatten_questions(payload: dict, teil: int) -> list[dict]:
    """Convert a Teil's payload into a flat list of questions for scoring."""
    topic = teil_name(teil)
    out: list[dict] = []

    if teil in (1, 2, 3):
        # All three reuse the same MCQ shape — newspaper article (T1),
        # directory (T2), email (T3). Question ordering follows the source.
        for q in payload.get("questions") or []:
            out.append({
                "question_type": "single_choice",
                "topic": topic,
                "stem": q.get("stem", ""),
                "options": q.get("options", []),
                "correct_option_index": q.get("correct_index", 0),
                "explanation": q.get("explanation", ""),
            })
        return out

    if teil == 4:
        # Letter-matching ×5 over a 6-ad pool with 'X' for no-match.
        pool_id = (payload.get("ad_pool") or {}).get("pool_id") or "t4_pool"
        for q in payload.get("questions") or []:
            correct = (q.get("correct_letter") or "").lower().strip()
            out.append({
                "question_type": "letter_matching",
                "topic": topic,
                "pool_id": pool_id,
                "stem": q.get("stem", ""),
                "correct_letter": correct,
                "explanation": q.get("explanation", ""),
            })
        return out

    return out


def _enrich_ad_pool(pool: dict) -> dict:
    """Annotate the ad pool with the valid letter set + the no-match marker.
    The frontend reads these to validate input. A2 uses a–f with 'X' as
    no-match (vs B1 with a–j and '0')."""
    ads = pool.get("ads") or []
    letters = [str(a.get("letter", "")).lower() for a in ads if a.get("letter")]
    return {
        **pool,
        "valid_letters": letters,
        "no_match_marker": A2_NO_MATCH_MARKER,
    }


def _section_payload(payload: dict, teil: int, flat_questions: list[dict]) -> dict:
    """Build the per-Teil section to embed in manifest['teile']."""
    base = {
        "teil": teil,
        "teil_name": teil_name(teil),
        "layout": LAYOUT_PER_TEIL.get(teil, "passage_questions"),
        "instructions": INSTRUCTIONS_PER_TEIL.get(teil, ""),
        "questions": flat_questions,
    }
    if teil in (1, 2, 3):
        base["passage_title"] = payload.get("passage_title", "")
        base["passage"] = payload.get("passage", "")
        base["context"] = payload.get("context", "")
    elif teil == 4:
        base["ad_pool"] = _enrich_ad_pool(payload.get("ad_pool") or {})
        base["context"] = payload.get("context", "")
    return base


# ── Full exam: all 4 Teile bundled ────────────────────────────────────────────


def full_exam_title() -> str:
    return "German A2 Lesen — Vollständige Prüfung"


def generate_full_exam(*, progress=None) -> dict:
    """Generate a complete 4-Teil A2 Lesen exam in parallel."""
    teile = (1, 2, 3, 4)
    client = _gemini_client()

    def _gen_one(t: int) -> tuple[int, dict]:
        if t == 4:
            return t, _generate_teil4_with_validation(client)
        return t, generate_one_teil(t, client)

    payloads_by_teil: dict[int, dict] = {}
    completed = 0
    with ThreadPoolExecutor(max_workers=len(teile)) as pool:
        futures = [pool.submit(_gen_one, t) for t in teile]
        for fut in futures:
            t, payload = fut.result()
            payloads_by_teil[t] = payload
            completed += 1
            if progress:
                progress("teil", completed, len(teile))
            logger.info("A2 Lesen exam: Teil %d done (%d/%d)", t, completed, len(teile))

    teile_payloads: list[dict] = []
    flat_questions: list[dict] = []
    for t in teile:
        payload = payloads_by_teil[t]
        per_teil_questions = _flatten_questions(payload, t)
        section = _section_payload(payload, t, per_teil_questions)
        teile_payloads.append(section)
        for q in per_teil_questions:
            flat_questions.append({**q, "teil": t})

    return {
        "kind": "full_lesen_exam",
        "teile": teile_payloads,
        "questions": flat_questions,
    }
