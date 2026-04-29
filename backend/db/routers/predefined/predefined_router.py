"""
Predefined-subject endpoints.

Currently exposes the PMP subject only. The pattern is generalizable: each
predefined subject has a stable name, a corpus module, and a quiz endpoint
that grounds Gemini flash-lite generation in chunks from that corpus
(light-RAG: in-memory chapter selection, no embeddings).

Generation strategy:
- Focused mode (focus_chapters set): single Gemini call. The chapter slice is
  small enough that the full request fits under Flash-Lite's ~8K output cap.
- Full mode (no focus): chunked per-chapter calls run concurrently. Each call
  emits a few questions for one chapter, with chapter-matched exemplars,
  staying well under the output cap and improving per-chapter style anchoring.
"""

import asyncio
import json
import os
import re
import uuid
from datetime import datetime
from typing import Annotated, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, HTTPException
from google import genai
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agents.pmp import (
    INSTRUCTIONS,
    PMP_CHAPTERS,
    PMP_SUBJECT_COLOR,
    PMP_SUBJECT_NAME,
    build_corpus_text,
    format_exemplars,
    get_chapter_by_slug,
    get_exemplars,
)
from db.dependency import get_current_user, get_db
from db.models import Quiz, Subject, User
from db.routers.subscription.subscription_router import verify_pro_access
from schemas import QuizResponse, SubjectResponse

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/predefined", tags=["predefined"])

# Generation caps (mirrored on the frontend modal).
# Focused fits in one Gemini call; full coverage is chunked across chapters.
MAX_FOCUSED_QUESTIONS = 30
MAX_FULL_QUESTIONS = 60


# ── helpers ──────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> dict:
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    clean = match.group(1) if match else text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON: {e}")


def _get_or_create_pmp_subject(user: User, db: Session) -> Subject:
    """Find the user's PMP subject; create it if missing. Idempotent per user."""
    subject = (
        db.query(Subject)
        .filter(Subject.user_id == user.id, Subject.name == PMP_SUBJECT_NAME)
        .first()
    )
    if subject:
        return subject
    subject = Subject(
        id=uuid.uuid4(),
        user_id=user.id,
        name=PMP_SUBJECT_NAME,
        color=PMP_SUBJECT_COLOR,
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


def _build_type_strings(quiz_type: str, n: int) -> tuple[str, str]:
    """Per-quiz-type schema snippet and instruction line."""
    if quiz_type == "multiple_select":
        question_format = """{
      "question_text": "Question here",
      "topic": "<one of the allowed topic names>",
      "options": ["A", "B", "C", "D"],
      "correct_option_indices": [0, 2],
      "explanation": "Why"
    }"""
        type_instruction = (
            "Each question must have exactly 4 options and "
            "'correct_option_indices' as a list of integers."
        )
    elif quiz_type == "true_or_false":
        question_format = """{
      "question_text": "A factual PMP statement (evaluatable as true or false)",
      "topic": "<one of the allowed topic names>",
      "options": ["True", "False"],
      "correct_option_index": 0,
      "explanation": "Why this statement is true or false"
    }"""
        type_instruction = (
            f'IMPORTANT: options MUST be exactly ["True", "False"]. '
            f"correct_option_index is 0 for True, 1 for False. "
            f"You MUST generate EXACTLY {n} statements."
        )
    else:
        question_format = """{
      "question_text": "Question here",
      "topic": "<one of the allowed topic names>",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "explanation": "Why"
    }"""
        type_instruction = (
            "Each question must have exactly 4 options and "
            "'correct_option_index' as a single integer."
        )
    return question_format, type_instruction


def _build_style_block(exemplars) -> str:
    if not exemplars:
        return ""
    return (
        "## Style Reference\n"
        "Real PMP exam questions, included for STYLE inspiration only. "
        "Do NOT copy them — generate NEW questions matching their tone, "
        "complexity, and distractor pattern.\n\n"
        f"{format_exemplars(exemplars)}\n\n---\n\n"
    )


async def _call_gemini(prompt: str) -> dict:
    """Run a Gemini Flash-Lite call off the event loop and parse the JSON body."""
    response = await asyncio.to_thread(
        client.models.generate_content,
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config={"thinking_config": {"thinking_budget": 0}},
    )
    return _extract_json(response.text)


async def _generate_single(
    db: Session,
    quiz_type: str,
    num_questions: int,
    allowed_topics: list[str],
    focus_names: list[str],
    focus_chapters: list[str],
) -> dict:
    """One Gemini call with the full focused prompt."""
    question_format, type_instruction = _build_type_strings(quiz_type, num_questions)
    corpus_text = build_corpus_text(focus_chapters)
    exemplars = get_exemplars(db, focus_chapters, k=3)
    style_block = _build_style_block(exemplars)

    focus_clause = (
        f"Focus ONLY on these chapters: {', '.join(focus_names)}."
        if focus_names
        else "Cover the chapters as evenly as possible."
    )

    prompt = f"""
{INSTRUCTIONS}

---

## This Request

Generate EXACTLY {num_questions} questions of type '{quiz_type}'.
- {type_instruction}
- Allowed topics: {allowed_topics}
- {focus_clause}

Each question follows this structure:
{question_format}

Return this JSON — the "questions" array MUST have EXACTLY {num_questions} objects:
{{
  "primary_subject": "PMP",
  "topics": {allowed_topics},
  "questions": [ /* {num_questions} question objects here */ ]
}}

{style_block}## Corpus
---
{corpus_text}
---
"""
    quiz_content = await _call_gemini(prompt)
    questions = quiz_content.get("questions", [])
    if len(questions) > num_questions:
        quiz_content["questions"] = questions[:num_questions]
    elif len(questions) < num_questions:
        raise ValueError(
            f"AI returned {len(questions)} questions instead of {num_questions}. Try again."
        )
    return quiz_content


async def _generate_chunked(
    db: Session,
    quiz_type: str,
    num_questions: int,
) -> dict:
    """
    Generate per-chapter and merge, fanned out concurrently.

    Each chapter's prompt is small (one chapter + 2 chapter-matched exemplars),
    so output token usage stays comfortably under Flash-Lite's cap regardless
    of total quiz size.
    """
    n_ch = len(PMP_CHAPTERS)
    base = num_questions // n_ch
    extra = num_questions % n_ch

    async def gen_for_chapter(i: int, chapter: dict) -> list[dict]:
        chunk_n = base + (1 if i < extra else 0)
        if chunk_n == 0:
            return []
        question_format, type_instruction = _build_type_strings(quiz_type, chunk_n)
        chunk_corpus = build_corpus_text([chapter["slug"]])
        chunk_exemplars = get_exemplars(db, [chapter["slug"]], k=2)
        chunk_style = _build_style_block(chunk_exemplars)
        chapter_name = chapter["name"]

        prompt = f"""
{INSTRUCTIONS}

---

## This Request

Generate EXACTLY {chunk_n} questions of type '{quiz_type}' for the PMP chapter "{chapter_name}".
- {type_instruction}
- Every question must have topic == "{chapter_name}".

Each question follows this structure:
{question_format}

Return this JSON — the "questions" array MUST have EXACTLY {chunk_n} objects:
{{
  "primary_subject": "PMP",
  "topics": ["{chapter_name}"],
  "questions": [ /* {chunk_n} question objects here */ ]
}}

{chunk_style}## Corpus
---
{chunk_corpus}
---
"""
        chunk_content = await _call_gemini(prompt)
        chunk_questions = chunk_content.get("questions", [])
        if len(chunk_questions) > chunk_n:
            chunk_questions = chunk_questions[:chunk_n]
        elif len(chunk_questions) < chunk_n:
            raise ValueError(
                f"Chapter '{chapter_name}': AI returned "
                f"{len(chunk_questions)} questions instead of {chunk_n}."
            )
        return chunk_questions

    results = await asyncio.gather(
        *(gen_for_chapter(i, ch) for i, ch in enumerate(PMP_CHAPTERS))
    )
    all_questions = [q for chunk in results for q in chunk]

    return {
        "primary_subject": "PMP",
        "topics": [c["name"] for c in PMP_CHAPTERS],
        "questions": all_questions,
    }


# ── PMP endpoints ────────────────────────────────────────────────────────────

@router.get("/pmp/chapters")
async def list_pmp_chapters():
    """Public: chapter metadata used by the frontend for chapter pickers."""
    return [
        {"slug": c["slug"], "name": c["name"], "summary": c["summary"]}
        for c in PMP_CHAPTERS
    ]


@router.post("/pmp/provision", response_model=SubjectResponse)
async def provision_pmp_subject(db: DBSession, current_user: CurrentUser):
    """Idempotent: returns the user's PMP subject, creating it on first call."""
    subject = _get_or_create_pmp_subject(current_user, db)
    return subject


class PMPQuizRequest(BaseModel):
    quiz_name: Optional[str] = None
    quiz_type: Optional[str] = "single_choice"
    num_questions: int = 10
    time_limit: Optional[int] = None
    focus_chapters: Optional[list[str]] = None  # chapter slugs


@router.post("/pmp/quiz", response_model=QuizResponse, status_code=201)
async def create_pmp_quiz(
    db: DBSession,
    current_user: CurrentUser,
    payload: PMPQuizRequest = Body(...),
    _pro=Depends(verify_pro_access),
):
    """Generate a PMP quiz grounded in the predefined corpus + exam-bank exemplars."""
    quiz_type = payload.quiz_type or "single_choice"

    if payload.focus_chapters:
        num_questions = min(max(payload.num_questions, 1), MAX_FOCUSED_QUESTIONS)
    else:
        num_questions = min(max(payload.num_questions, 1), MAX_FULL_QUESTIONS)

    focus_names: list[str] = []
    if payload.focus_chapters:
        for slug in payload.focus_chapters:
            ch = get_chapter_by_slug(slug)
            if ch:
                focus_names.append(ch["name"])
    allowed_topics = focus_names if focus_names else [c["name"] for c in PMP_CHAPTERS]

    subject = _get_or_create_pmp_subject(current_user, db)

    try:
        if payload.focus_chapters:
            quiz_content = await _generate_single(
                db,
                quiz_type,
                num_questions,
                allowed_topics,
                focus_names,
                payload.focus_chapters,
            )
        else:
            quiz_content = await _generate_chunked(db, quiz_type, num_questions)

        default_title = (
            f"PMP — {', '.join(focus_names[:2])}"
            if focus_names
            else "PMP — Full Practice Quiz"
        )

        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=current_user.id,
            source_id=None,
            subject_id=subject.id,
            quiz_type=quiz_type,
            title=payload.quiz_name or default_title,
            num_questions=len(quiz_content.get("questions", [])),
            time_limit=payload.time_limit,
            content=quiz_content,
            topics={
                "primary_subject": "PMP",
                "topics": allowed_topics,
            },
            generation_date=datetime.utcnow(),
        )
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error generating PMP quiz: {str(e)}")
