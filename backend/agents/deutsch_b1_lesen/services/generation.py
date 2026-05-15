"""
End-to-end B1 Lesen generation pipeline.

Mirrors the Hören generation module structurally, but simpler: Lesen has no
audio step. The pipeline is just Gemini → JSON per Teil → flatten into a
manifest dict ready to drop into Quiz.content.

The output of `generate_full_exam` is:

  { kind: "full_lesen_exam",
    teile: [ {teil, teil_name, instructions, passage / passages / ad_pool /
              comments, questions}, ...×5 ],
    questions: [...flat across all Teile, each carrying its `teil` and
                `question_type` so the scorer + UI can dispatch...] }

Question types in the flat array:
  - "true_false"           — Teil 1 (Richtig / Falsch)
  - "single_choice"        — Teil 2 (a/b/c MCQ on one of two articles)
                             and Teil 5 (a/b/c MCQ on an institutional doc)
  - "letter_matching"      — Teil 3 (input a letter a–j or "0")
  - "true_false_ja_nein"   — Teil 4 (Ja / Nein per author)

The first three are scored by the standard `calculate_quiz_score` path with
the small extension that letter_matching compares strings instead of indices.
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

from agents.deutsch_b1_lesen import (
    DEUTSCH_B1_LESEN_CHAPTERS,
    INSTRUCTIONS,
    get_chapter_by_slug,
    topics_for_teil,
)

# Bumped above the default for prosody/wording variety within an assigned
# topic. Topic variety itself comes from random selection from TOPICS_BY_TEIL.
GEMINI_TEMPERATURE = 1.1

# Real Goethe-Zertifikat B1 Lesen item counts per Teil. The scorer counts
# questions in the flat list, so these are also the per-Teil contribution
# to the total (30 items).
ITEMS_PER_TEIL = {1: 6, 2: 6, 3: 7, 4: 7, 5: 4}

INSTRUCTIONS_PER_TEIL = {
    1: "Lesen Sie den Text. Sind die Aussagen richtig oder falsch?",
    2: "Lesen Sie die Texte und die Aufgaben. Wählen Sie für jede Aufgabe die richtige Antwort.",
    3: "Lesen Sie die Anzeigen a–j und die Situationen 1–7. Welche Anzeige passt zu welcher Situation? Schreiben Sie für jede Situation den passenden Buchstaben in das Feld. Für eine Situation gibt es keine passende Anzeige. Schreiben Sie hier '0'. Sie können jede Anzeige nur einmal verwenden.",
    4: "Lesen Sie das Forum und die Aufgaben. Findet die jeweilige Person, dass die Aktion gut ist? Antworten Sie mit Ja oder Nein.",
    5: "Lesen Sie den Text und die Aufgaben. Wählen Sie für jede Aufgabe die richtige Antwort.",
}


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
        (c["slug"] for c in DEUTSCH_B1_LESEN_CHAPTERS if c["slug"].startswith(f"teil_{teil}_")),
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


# ── Teil-3 specific composition validation ────────────────────────────────────
# Teil 3 has hard rules the model can violate: 10 ads (a–j), 7 questions,
# exactly one "0", remaining 6 letters unique. If validation fails we retry
# the call once (model temp varies) before accepting whatever comes back.

TEIL3_REQUIRED_LETTERS = list("abcdefghij")


def _teil3_violations(payload: dict) -> list[str]:
    """Return a list of human-readable violations of Teil 3 composition rules.
    Empty list = the payload is valid."""
    violations: list[str] = []
    pool = payload.get("ad_pool") or {}
    ads = pool.get("ads") or []
    letters = [a.get("letter") for a in ads]
    if sorted(letters) != TEIL3_REQUIRED_LETTERS:
        violations.append(f"ad_pool.ads must have exactly letters a–j, got {letters}")

    questions = payload.get("questions") or []
    if len(questions) != 7:
        violations.append(f"expected 7 questions, got {len(questions)}")

    correct_letters = [(q.get("correct_letter") or "").lower() for q in questions]
    zero_count = sum(1 for c in correct_letters if c == "0")
    if zero_count != 1:
        violations.append(f"expected exactly one correct_letter == '0', got {zero_count}")

    non_zero = [c for c in correct_letters if c != "0"]
    if len(non_zero) != len(set(non_zero)):
        violations.append(f"correct_letter values (excluding '0') must be unique, got {non_zero}")

    invalid = [c for c in non_zero if c not in TEIL3_REQUIRED_LETTERS]
    if invalid:
        violations.append(f"correct_letter values must be a–j or '0', got invalid {invalid}")

    return violations


def _generate_teil3_with_validation(client) -> dict:
    """Generate a Teil 3 payload, retrying once if the model violates the
    composition rules. After two attempts we accept the imperfect payload
    rather than 502 — better to ship a quiz with a small flaw than fail
    the whole exam."""
    last_payload: dict | None = None
    for attempt in (1, 2):
        payload = generate_one_teil(3, client)
        violations = _teil3_violations(payload)
        if not violations:
            return payload
        logger.warning(
            "Lesen Teil 3 attempt %d had composition violations: %s",
            attempt, violations,
        )
        last_payload = payload
    # Both attempts had issues — return the second one and let the user see it.
    return last_payload  # type: ignore[return-value]


# ── Flatten per-Teil payloads to scoring-friendly question dicts ──────────────


def _flatten_questions(payload: dict, teil: int) -> list[dict]:
    """Convert a Teil's payload into a flat list of questions matching the
    Quiz.content shape used by `calculate_quiz_score`."""
    topic = teil_name(teil)
    out: list[dict] = []

    if teil == 1:
        # Richtig/Falsch ×6 over a single passage
        for q in payload.get("questions") or []:
            answer = (q.get("answer") or "").lower()
            answer_idx = 0 if answer.startswith("richt") else 1
            out.append({
                "question_type": "true_false",
                "topic": topic,
                "stem": q.get("stem", ""),
                "options": ["Richtig", "Falsch"],
                "correct_option_index": answer_idx,
                "explanation": q.get("explanation", ""),
            })
        return out

    if teil == 2:
        # MCQ ×6 (3 over each of two passages)
        for q in payload.get("questions") or []:
            out.append({
                "question_type": "single_choice",
                "topic": topic,
                "passage_id": q.get("passage_id"),
                "stem": q.get("stem", ""),
                "options": q.get("options", []),
                "correct_option_index": q.get("correct_index", 0),
                "explanation": q.get("explanation", ""),
            })
        return out

    if teil == 3:
        # Letter matching ×7 over a shared 10-ad pool
        pool_id = (payload.get("ad_pool") or {}).get("pool_id") or "t3_pool"
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

    if teil == 4:
        # Ja/Nein ×7 reader comments
        for q in payload.get("questions") or []:
            answer = (q.get("answer") or "").lower()
            answer_idx = 0 if answer.startswith("ja") else 1
            out.append({
                "question_type": "true_false_ja_nein",
                "topic": topic,
                "comment_id": q.get("comment_id"),
                "stem": q.get("stem", ""),
                "options": ["Ja", "Nein"],
                "correct_option_index": answer_idx,
                "explanation": q.get("explanation", ""),
            })
        return out

    if teil == 5:
        # MCQ ×4 over an institutional document
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

    return out


# Layout discriminator written into each section so the frontend dispatches on
# layout rather than the level-specific Teil number. A2 reuses the same layouts
# in different Teil positions (A2 Teil 4 = letter_matching, B1 Teil 3 = letter_matching).
LAYOUT_PER_TEIL = {
    1: "passage_questions",      # one passage + N R/F questions
    2: "two_passages_questions", # two passages + N MCQ each
    3: "letter_matching",        # ad pool + N letter inputs
    4: "comments_questions",     # one prompt + N comments + Ja/Nein per comment
    5: "passage_questions",      # one passage + N MCQ
}


def _enrich_ad_pool(pool: dict) -> dict:
    """Annotate the ad pool with the valid letter set + the no-match marker.
    The frontend reads these to validate input and label the empty-match option;
    keeping them in the manifest means the play page works for any level (B1
    uses a–j with '0' for no-match; A2 uses a–f with 'X')."""
    ads = pool.get("ads") or []
    letters = [str(a.get("letter", "")).lower() for a in ads if a.get("letter")]
    return {
        **pool,
        "valid_letters": letters,
        "no_match_marker": "0",
    }


def _section_payload(payload: dict, teil: int, flat_questions: list[dict]) -> dict:
    """Build the per-Teil section to embed in manifest['teile']. Includes
    the source material (passage / passages / ad_pool / comments) the runner
    needs to render alongside the questions, plus the questions themselves."""
    base = {
        "teil": teil,
        "teil_name": teil_name(teil),
        "layout": LAYOUT_PER_TEIL.get(teil, "passage_questions"),
        "instructions": INSTRUCTIONS_PER_TEIL.get(teil, ""),
        "questions": flat_questions,
    }
    if teil == 1:
        base["passage_title"] = payload.get("passage_title", "")
        base["passage"] = payload.get("passage", "")
        base["context"] = payload.get("context", "")
    elif teil == 2:
        base["passages"] = payload.get("passages") or []
    elif teil == 3:
        base["ad_pool"] = _enrich_ad_pool(payload.get("ad_pool") or {})
        base["context"] = payload.get("context", "")
    elif teil == 4:
        base["prompt_de"] = payload.get("prompt_de", "")
        base["comments"] = payload.get("comments") or []
        base["context"] = payload.get("context", "")
    elif teil == 5:
        base["passage_title"] = payload.get("passage_title", "")
        base["passage"] = payload.get("passage", "")
        base["context"] = payload.get("context", "")
    return base


# ── Full exam: all 5 Teile bundled ────────────────────────────────────────────


def full_exam_title() -> str:
    return "German B1 Lesen — Vollständige Prüfung"


def generate_full_exam(*, progress=None) -> dict:
    """Generate a complete 5-Teil B1 Lesen exam. All 5 Teile run in parallel
    via a thread pool — Gemini HTTP releases the GIL during waits so threads
    give us the full speedup. End-to-end ~10–20s on Gemini 2.5 Flash.

    Args:
        progress: optional callable `progress(stage, current, total)` invoked
                  once per Teil completion (order is non-deterministic).

    Returns:
        Manifest dict shaped as:
          { kind: "full_lesen_exam",
            teile: [ ...×5 ],
            questions: [...flat across all Teile, each carrying its `teil`...] }
    """
    teile = (1, 2, 3, 4, 5)
    client = _gemini_client()

    def _gen_one(t: int) -> tuple[int, dict]:
        if t == 3:
            return t, _generate_teil3_with_validation(client)
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
            logger.info("Lesen exam: Teil %d done (%d/%d)", t, completed, len(teile))

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
