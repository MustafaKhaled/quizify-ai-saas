"""
Lesen (German Reading) endpoints. Currently scoped to B1, mirrors the Hören
router structure so adding A2/A1 Lesen later is mechanical.

POST /lesen/{slug}/quiz
    Generates a complete 5-Teil Goethe-Zertifikat B1 Lesen exam (passages +
    questions across all 5 Teile), provisions or reuses the user's Subject
    row, and persists as a `Quiz` row with `quiz_type='reading'`.

    The Quiz.content shape is `{kind: "full_lesen_exam", teile: [...×5],
    questions: [...flat across all Teile]}`. Question objects carry a
    `question_type` discriminator: "true_false", "single_choice",
    "letter_matching", or "true_false_ja_nein". The standard scorer reads
    these to pick the right comparison.

    Faster than Hören (no audio render): typical end-to-end ~10–20s on
    Gemini 2.5 Flash with all 5 Teile parallelized.

GET /lesen/{slug}/sessions
    User's existing Lesen Quiz rows, most recent first, with score if taken.

GET /lesen/{slug}/quota
    User's Lesen usage and remaining quota. SEPARATE from the Hören quota
    because Lesen is text-only (no audio) and ~10× cheaper to generate;
    the Hören scarcity logic doesn't apply. Default caps:
      - Pro    → 10 exams per rolling 7 days
      - Trial  → 1 exam total during the trial window
      - Other  → 0
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated, Callable, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path as PathParam
from pydantic import BaseModel
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from agents import get_agent
from agents.deutsch_a2_lesen.services.generation import (
    full_exam_title as a2_lesen_full_exam_title,
    generate_full_exam as a2_lesen_generate_full_exam,
)
from agents.deutsch_b1_lesen.services.generation import (
    full_exam_title as b1_lesen_full_exam_title,
    generate_full_exam as b1_lesen_generate_full_exam,
)
from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizResult, Subject, User

# Per-slug dispatch table — same pattern as Hören. Adding new levels here
# is the only backend change needed; the route handlers stay generic.
LESEN_GENERATORS: dict[str, dict[str, Callable]] = {
    "deutsch_b1_lesen": {
        "generate_full_exam": b1_lesen_generate_full_exam,
        "full_exam_title": b1_lesen_full_exam_title,
        # Real Goethe-Zertifikat exam time limits (in minutes).
        "time_limit_minutes": 65,
    },
    "deutsch_a2_lesen": {
        "generate_full_exam": a2_lesen_generate_full_exam,
        "full_exam_title": a2_lesen_full_exam_title,
        "time_limit_minutes": 30,
    },
}

# Lesen-specific quota — independent of Hören. Lesen is ~10× cheaper to
# generate (Gemini text only, no Edge TTS + ffmpeg pipeline) so the cap is
# more generous, both to avoid making a cheap feature feel artificially
# scarce and to keep the Hören scarcity rationale intact.
LESEN_QUOTA_PRO_PER_WEEK = 10
LESEN_QUOTA_TRIAL_LIFETIME = 1
LESEN_QUOTA_PRO_WINDOW = timedelta(days=7)

# Quiz row marker — distinct from audio_listening so a single SQL filter
# separates Lesen quizzes from Hören for both quota counting and the
# library page.
LESEN_QUIZ_TYPE = "reading"


DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/lesen", tags=["lesen"])


class GenerateLesenRequest(BaseModel):
    # Reserved for forward-compat — currently unused. Keeps the request body
    # symmetrical with Hören and gives us a place to plumb generation knobs
    # (max temperature, focus_teile subset, ...) without changing the URL.
    _unused: Optional[str] = None


def _resolve_lesen_agent(slug: str) -> dict:
    agent = get_agent(slug)
    if not agent or slug not in LESEN_GENERATORS:
        raise HTTPException(status_code=404, detail=f"unknown lesen subject: {slug}")
    return agent


def _user_tier(user: User) -> str:
    """Same tier classification as Hören. 'pro', 'trial', or 'expired'."""
    if user.is_pro:
        return "pro"
    if user.trial_ends_at is not None:
        trial_end = user.trial_ends_at
        if trial_end.tzinfo is None:
            trial_end = trial_end.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < trial_end:
            return "trial"
    return "expired"


def _lesen_quota_status(user: User, db: Session) -> dict:
    """Compute Lesen usage / limit / remaining. Same shape as the Hören
    quota response so the frontend can render both with the same component.
    `period` is "week" for Pro, "trial" for trial users, "none" for expired."""
    tier = _user_tier(user)
    now = datetime.now(timezone.utc)

    if tier == "pro":
        limit = LESEN_QUOTA_PRO_PER_WEEK
        window_start = now - LESEN_QUOTA_PRO_WINDOW
        window_start_naive = window_start.replace(tzinfo=None)
        # Apply quota_reset_at as a floor — trial-era quizzes shouldn't
        # eat into the fresh Pro window after upgrade. Same logic as Hören.
        if user.quota_reset_at is not None and user.quota_reset_at > window_start_naive:
            window_start_naive = user.quota_reset_at

        recent = (
            db.query(Quiz)
            .filter(
                Quiz.user_id == user.id,
                Quiz.quiz_type == LESEN_QUIZ_TYPE,
                Quiz.generation_date >= window_start_naive,
            )
            .order_by(Quiz.generation_date.asc())
            .all()
        )
        used = len(recent)
        period = "week"
        reason = None if used < limit else "weekly_limit_reached"

        next_available_at = None
        if reason is not None and recent:
            oldest = recent[0].generation_date
            if oldest.tzinfo is None:
                oldest = oldest.replace(tzinfo=timezone.utc)
            next_available_at = (oldest + LESEN_QUOTA_PRO_WINDOW).isoformat()

        return {
            "tier": tier,
            "limit": limit,
            "used": used,
            "remaining": max(limit - used, 0),
            "period": period,
            "can_generate": reason is None,
            "reason": reason,
            "next_available_at": next_available_at,
        }

    if tier == "trial":
        limit = LESEN_QUOTA_TRIAL_LIFETIME
        trial_q = db.query(Quiz).filter(
            Quiz.user_id == user.id,
            Quiz.quiz_type == LESEN_QUIZ_TYPE,
        )
        if user.quota_reset_at is not None:
            trial_q = trial_q.filter(Quiz.generation_date >= user.quota_reset_at)
        used = trial_q.count()
        period = "trial"
        reason = None if used < limit else "trial_limit_reached"
        return {
            "tier": tier,
            "limit": limit,
            "used": used,
            "remaining": max(limit - used, 0),
            "period": period,
            "can_generate": reason is None,
            "reason": reason,
            "next_available_at": None,
        }

    return {
        "tier": tier,
        "limit": 0,
        "used": 0,
        "remaining": 0,
        "period": "none",
        "can_generate": False,
        "reason": "subscription_required",
        "next_available_at": None,
    }


def _get_or_create_subject(user: User, db: Session, agent: dict) -> Subject:
    """Same idempotent pattern as the Hören router and predefined router."""
    subject = (
        db.query(Subject)
        .filter(Subject.user_id == user.id, Subject.name == agent["name"])
        .first()
    )
    if subject:
        return subject
    subject = Subject(
        id=uuid.uuid4(),
        user_id=user.id,
        name=agent["name"],
        color=agent["color"],
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.post("/{slug}/quiz", status_code=201)
async def create_lesen_quiz(
    db: DBSession,
    current_user: CurrentUser,
    payload: GenerateLesenRequest = Body(default_factory=GenerateLesenRequest),
    slug: str = PathParam(...),
):
    """Generate a fresh full Lesen exam (all 5 Teile) and persist as a Quiz row."""
    agent = _resolve_lesen_agent(slug)

    quota = _lesen_quota_status(current_user, db)
    if not quota["can_generate"]:
        if quota["reason"] == "weekly_limit_reached":
            next_at = quota.get("next_available_at")
            when = f" Your next exam unlocks at {next_at}." if next_at else ""
            detail = (
                f"You've used all {quota['limit']} Lesen exams in the last 7 days.{when}"
            )
            status_code = 429
        elif quota["reason"] == "trial_limit_reached":
            detail = (
                f"Your trial includes {quota['limit']} Lesen exam. "
                f"Upgrade to Pro for {LESEN_QUOTA_PRO_PER_WEEK} Lesen exams per week."
            )
            status_code = 402
        else:
            detail = "Lesen requires an active subscription. Upgrade to Pro to generate reading exams."
            status_code = 402
        raise HTTPException(status_code=status_code, detail=detail)

    generators = LESEN_GENERATORS[slug]
    generate_full_exam = generators["generate_full_exam"]
    full_exam_title = generators["full_exam_title"]
    time_limit_minutes = generators.get("time_limit_minutes")

    try:
        # Off-thread the (still-blocking) generation so other requests aren't
        # starved while Gemini round-trips. ~10–20s typical with parallelization.
        manifest = await asyncio.to_thread(generate_full_exam)
    except Exception as e:
        logger.exception(
            "Lesen full-exam generation failed for user %s slug=%s",
            current_user.id, slug,
        )
        raise HTTPException(status_code=502, detail=f"generation failed: {type(e).__name__}: {e}")

    if not manifest.get("questions"):
        raise HTTPException(
            status_code=502,
            detail="generation produced 0 questions — the model output may be malformed; try again",
        )

    subject = _get_or_create_subject(current_user, db, agent)

    new_quiz = Quiz(
        id=uuid.uuid4(),
        user_id=current_user.id,
        source_id=None,
        subject_id=subject.id,
        quiz_type=LESEN_QUIZ_TYPE,
        title=full_exam_title(),
        num_questions=len(manifest["questions"]),
        time_limit=time_limit_minutes,
        content=manifest,
        topics={
            "primary_subject": agent["name"],
            "topics": [t.get("teil_name", f"Teil {t.get('teil')}") for t in manifest.get("teile", [])],
        },
        generation_date=datetime.utcnow(),
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return {
        "id": str(new_quiz.id),
        "title": new_quiz.title,
        "num_questions": new_quiz.num_questions,
        "num_teile": len(manifest.get("teile", [])),
    }


@router.get("/{slug}/quota")
async def get_lesen_quota(
    db: DBSession,
    current_user: CurrentUser,
    slug: str = PathParam(...),
):
    """Current user's Lesen usage and remaining quota."""
    _resolve_lesen_agent(slug)
    return _lesen_quota_status(current_user, db)


@router.get("/{slug}/sessions")
async def list_user_sessions(
    db: DBSession,
    current_user: CurrentUser,
    slug: str = PathParam(...),
):
    """User's previous Lesen sessions, most recent first, with score if taken."""
    agent = _resolve_lesen_agent(slug)

    subject = (
        db.query(Subject)
        .filter(Subject.user_id == current_user.id, Subject.name == agent["name"])
        .first()
    )
    if not subject:
        return {"subject_slug": slug, "sessions": []}

    quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.user_id == current_user.id,
            Quiz.subject_id == subject.id,
            Quiz.quiz_type == LESEN_QUIZ_TYPE,
        )
        .order_by(Quiz.generation_date.desc())
        .all()
    )

    quiz_ids = [q.id for q in quizzes]
    latest_results: dict[uuid.UUID, QuizResult] = {}
    if quiz_ids:
        all_results = (
            db.query(QuizResult)
            .filter(QuizResult.quiz_id.in_(quiz_ids), QuizResult.user_id == current_user.id)
            .order_by(QuizResult.attempt_date.desc())
            .all()
        )
        for r in all_results:
            if r.quiz_id not in latest_results:
                latest_results[r.quiz_id] = r

    sessions = []
    for q in quizzes:
        content = q.content or {}
        teile = content.get("teile") or []
        result = latest_results.get(q.id)
        sessions.append({
            "quiz_id": str(q.id),
            "title": q.title,
            "num_teile": len(teile),
            "num_questions": q.num_questions,
            "generated_at": q.generation_date.isoformat() if q.generation_date else None,
            "latest_score": float(result.score_percentage) if result else None,
            "taken_at": result.attempt_date.isoformat() if result and result.attempt_date else None,
        })

    return {"subject_slug": slug, "sessions": sessions}
