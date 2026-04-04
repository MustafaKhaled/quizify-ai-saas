import re
import os
import json
import uuid
from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from google import genai

from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizResult, QuizSource, Subject, User
from db.routers.subscription.subscription_router import verify_pro_access
from schemas import (
    QuizResponse,
    SubjectCreate,
    SubjectDetailResponse,
    SubjectResponse,
    SubjectUpdate,
)

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
db_dep = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/subjects", tags=["subjects"])


# ── helpers ──────────────────────────────────────────────────────────────────

def _get_subject_or_404(subject_id: uuid.UUID, user_id, db: Session) -> Subject:
    subject = db.query(Subject).filter(
        Subject.id == subject_id,
        Subject.user_id == user_id,
    ).first()
    if not subject:
        raise HTTPException(404, "Subject not found")
    return subject


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


# ── CRUD ─────────────────────────────────────────────────────────────────────

@router.post("", response_model=SubjectResponse, status_code=201)
async def create_subject(
    db: db_dep,
    current_user: CurrentUser,
    payload: SubjectCreate,
):
    subject = Subject(
        id=uuid.uuid4(),
        user_id=current_user.id,
        name=payload.name.strip(),
        color=payload.color,
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("", response_model=list[SubjectDetailResponse])
async def list_subjects(db: db_dep, current_user: CurrentUser):
    subjects = (
        db.query(Subject)
        .filter(Subject.user_id == current_user.id)
        .order_by(Subject.created_at.desc())
        .all()
    )
    result = []
    for s in subjects:
        source_count = db.query(QuizSource).filter(QuizSource.subject_id == s.id).count()
        quiz_count = db.query(Quiz).filter(Quiz.subject_id == s.id).count()
        # source-level quizzes
        source_ids = [src.id for src in db.query(QuizSource.id).filter(QuizSource.subject_id == s.id)]
        if source_ids:
            quiz_count += db.query(Quiz).filter(Quiz.source_id.in_(source_ids)).count()
        result.append(SubjectDetailResponse(
            id=s.id,
            name=s.name,
            color=s.color,
            created_at=s.created_at,
            source_count=source_count,
            quiz_count=quiz_count,
        ))
    return result


@router.get("/{subject_id}", response_model=SubjectDetailResponse)
async def get_subject(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
):
    s = _get_subject_or_404(subject_id, current_user.id, db)
    source_count = db.query(QuizSource).filter(QuizSource.subject_id == s.id).count()
    source_ids = [src.id for src in db.query(QuizSource.id).filter(QuizSource.subject_id == s.id)]
    quiz_count = db.query(Quiz).filter(Quiz.subject_id == s.id).count()
    if source_ids:
        quiz_count += db.query(Quiz).filter(Quiz.source_id.in_(source_ids)).count()
    return SubjectDetailResponse(
        id=s.id,
        name=s.name,
        color=s.color,
        created_at=s.created_at,
        source_count=source_count,
        quiz_count=quiz_count,
    )


@router.patch("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
    payload: SubjectUpdate,
):
    s = _get_subject_or_404(subject_id, current_user.id, db)
    if payload.name is not None:
        s.name = payload.name.strip()
    if payload.color is not None:
        s.color = payload.color
    db.commit()
    db.refresh(s)
    return s


@router.delete("/{subject_id}", status_code=204)
async def delete_subject(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
):
    s = _get_subject_or_404(subject_id, current_user.id, db)
    db.delete(s)
    db.commit()


# ── Sources & Quizzes within a subject ───────────────────────────────────────

@router.get("/{subject_id}/sources")
async def list_subject_sources(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
):
    _get_subject_or_404(subject_id, current_user.id, db)
    sources = (
        db.query(QuizSource)
        .filter(
            QuizSource.subject_id == subject_id,
            QuizSource.user_id == current_user.id,
        )
        .order_by(QuizSource.upload_date.desc())
        .all()
    )
    return sources


@router.get("/{subject_id}/quizzes")
async def list_subject_quizzes(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
):
    _get_subject_or_404(subject_id, current_user.id, db)

    # Subject-wide quizzes only (source_id must be NULL)
    subject_quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.subject_id == subject_id,
            Quiz.source_id.is_(None),
            Quiz.user_id == current_user.id,
        )
        .all()
    )

    # Source-level quizzes belonging to this subject's sources
    source_ids = [
        src.id
        for src in db.query(QuizSource.id).filter(
            QuizSource.subject_id == subject_id,
            QuizSource.user_id == current_user.id,
        )
    ]
    source_quizzes = []
    if source_ids:
        source_quizzes = (
            db.query(Quiz)
            .filter(Quiz.source_id.in_(source_ids), Quiz.user_id == current_user.id)
            .order_by(Quiz.generation_date.desc())
            .all()
        )

    all_quizzes = subject_quizzes + source_quizzes

    # Fetch latest result (score + id) per quiz in one query
    quiz_ids = [q.id for q in all_quizzes]
    latest_scores: dict[str, float] = {}
    latest_result_ids: dict[str, str] = {}
    if quiz_ids:
        results = (
            db.query(QuizResult)
            .filter(
                QuizResult.quiz_id.in_(quiz_ids),
                QuizResult.user_id == current_user.id,
            )
            .order_by(QuizResult.attempt_date.desc())
            .all()
        )
        for r in results:
            key = str(r.quiz_id)
            if key not in latest_scores:
                latest_scores[key] = float(r.score_percentage)
                latest_result_ids[key] = str(r.id)

    return [
        {
            "id": str(q.id),
            "source_id": str(q.source_id) if q.source_id else None,
            "subject_id": str(q.subject_id) if q.subject_id else None,
            "title": q.title,
            "quiz_type": q.quiz_type,
            "num_questions": q.num_questions,
            "time_limit": q.time_limit,
            "generation_date": q.generation_date.isoformat() if q.generation_date else None,
            "latest_score": latest_scores.get(str(q.id)),
            "latest_result_id": latest_result_ids.get(str(q.id)),
        }
        for q in all_quizzes
    ]


# ── Subject-wide quiz generation ─────────────────────────────────────────────

@router.post("/{subject_id}/quiz", response_model=QuizResponse, status_code=201)
async def create_subject_quiz(
    subject_id: uuid.UUID,
    db: db_dep,
    current_user: CurrentUser,
    _pro=Depends(verify_pro_access),
    quiz_type: Optional[str] = Form("single_choice"),
    quiz_name: Optional[str] = Form(None),
    num_questions: int = Form(10),
    time_limit: Optional[int] = Form(None),
):
    num_questions = min(num_questions, 30)
    subject = _get_subject_or_404(subject_id, current_user.id, db)

    sources = (
        db.query(QuizSource)
        .filter(
            QuizSource.subject_id == subject_id,
            QuizSource.user_id == current_user.id,
        )
        .all()
    )

    if not sources:
        raise HTTPException(400, "This subject has no sources. Upload at least one PDF first.")

    # Concatenate all source texts with section markers, then compress
    MAX_CHARS_PER_SOURCE = 20_000
    combined_text = ""
    for src in sources:
        src_text = re.sub(r'\n{3,}', '\n\n', (src.extracted_text or "").strip())
        src_text = re.sub(r'[ \t]{2,}', ' ', src_text)
        combined_text += f"\n\n--- Source: {src.file_name} ---\n\n"
        combined_text += src_text[:MAX_CHARS_PER_SOURCE]

    combined_text = combined_text.strip()
    if len(combined_text) < 200:
        raise HTTPException(400, "No extractable text found in this subject's sources.")

    # Build prompt (same structure as /quizzes/create)
    quiz_type = quiz_type or "single_choice"
    if quiz_type == "multiple_select":
        subject_question_format = """{
      "question_text": "Question here",
      "topic": "topic1",
      "options": ["A", "B", "C", "D"],
      "correct_option_indices": [0, 2],
      "explanation": "Why"
    }"""
        subject_type_instruction = "Each question must have exactly 4 options and 'correct_option_indices' as a list of integers."
    elif quiz_type == "true_or_false":
        subject_question_format = """{
      "question_text": "A factual statement about the material (evaluatable as true or false)",
      "topic": "topic1",
      "options": ["True", "False"],
      "correct_option_index": 0,
      "explanation": "Why this statement is true or false"
    }"""
        subject_type_instruction = f"IMPORTANT: options MUST be exactly [\"True\", \"False\"]. Do NOT use A/B/C/D. correct_option_index is 0 for True, 1 for False. You MUST generate EXACTLY {num_questions} statements."
    else:
        subject_question_format = """{
      "question_text": "Question here",
      "topic": "topic1",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "explanation": "Why"
    }"""
        subject_type_instruction = "Each question must have exactly 4 options and 'correct_option_index' as a single integer."

    prompt = f"""
Return ONLY valid JSON. Do NOT use markdown or conversational text.

STEP 1: Identify the primary subject and 3-5 main topics across all provided sources.

STEP 2: Generate EXACTLY {num_questions} questions of type '{quiz_type}'.
- {subject_type_instruction}
- Each question MUST have a "topic" field.
- Distribute evenly across ALL identified topics.

CRITICAL: Generate the quiz in the SAME LANGUAGE as the provided text.

Each question follows this structure:
{subject_question_format}

Return this JSON — the "questions" array MUST have EXACTLY {num_questions} objects, no more, no less:
{{
  "primary_subject": "...",
  "topics": ["topic1", "topic2", "topic3"],
  "questions": [ /* {num_questions} question objects here */ ]
}}

Text to analyze:
---
{combined_text}
---
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config={"thinking_config": {"thinking_budget": 0}},
        )
        quiz_content = _extract_json(response.text)

        questions = quiz_content.get("questions", [])
        if len(questions) > num_questions:
            quiz_content["questions"] = questions[:num_questions]
        elif len(questions) < num_questions:
            raise ValueError(f"AI returned {len(questions)} questions instead of {num_questions}. Try again.")

        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=current_user.id,
            source_id=None,
            subject_id=subject_id,
            quiz_type=quiz_type,
            title=quiz_name or f"{subject.name} — Full Subject Quiz",
            num_questions=len(quiz_content.get("questions", [])),
            time_limit=time_limit,
            content=quiz_content,
            topics={
                "primary_subject": quiz_content.get("primary_subject", subject.name),
                "topics": quiz_content.get("topics", []),
            },
            generation_date=datetime.utcnow(),
        )

        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error generating subject quiz: {str(e)}")
