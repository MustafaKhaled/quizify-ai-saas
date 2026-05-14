"""
Hören (German B1 Listening) endpoints.

POST /horen/{slug}/quiz
    Generates a complete 4-Teil Goethe-Zertifikat B1 Hören exam (scripts +
    audio + manifest), provisions or reuses the user's "German B1 — Hören"
    Subject row, and persists the exam as a `Quiz` row with
    `quiz_type='audio_listening'`. Audio files are written to
    backend/uploads/horen/ with UUID names and served via the /static/horen/
    StaticFiles mount.

    The Quiz.content shape is `{kind: "full_exam", teile: [...×4],
    questions: [...flat across all Teile]}`. The flat `questions` list (each
    carrying its own `audio_url`) is what `calculate_quiz_score` reads, so
    the existing /quizzes/submit/{quiz_id} endpoint works unchanged.

GET /horen/{slug}/sessions
    Returns the user's existing Hören Quiz rows (most recent first), with
    their score if they've taken them. Drives the library page.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Path as PathParam
from pydantic import BaseModel
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from agents import get_agent
from agents.deutsch_b1_horen.services.generation import (
    full_exam_title,
    generate_full_exam,
)
from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizResult, Subject, User

# Hören quota — independent of the generic /quizzes trial counter because
# full Hören exams are the expensive feature (4 Gemini calls + audio render
# per exam) and warrant their own per-feature cap.
#
# Pro uses a ROLLING 7-day window (not a calendar week) so signup date
# doesn't disadvantage anyone — every user gets their full allowance
# regardless of when they joined. Each exam "expires" out of the count
# 7 days after it was generated.
#
#   Pro    → 5 exams per rolling 7 days
#   Trial  → 1 exam total during the trial window (feature sampling)
#   Other  → 0 (subscription expired or never paid)
HOREN_QUOTA_PRO_PER_WEEK = 5
HOREN_QUOTA_TRIAL_LIFETIME = 1
HOREN_QUOTA_PRO_WINDOW = timedelta(days=7)

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/horen", tags=["horen"])

# Where on disk we write generated audio. The StaticFiles mount in main.py
# serves this directory under /static/horen.
HOREN_AUDIO_DIR = Path(__file__).parent.parent.parent.parent / "uploads" / "horen"
AUDIO_URL_PREFIX = "/static/horen"


class GenerateHorenRequest(BaseModel):
    provider: Optional[str] = "edge_tts"


def _resolve_horen_agent(slug: str) -> dict:
    agent = get_agent(slug)
    if not agent or slug != "deutsch_b1_horen":
        raise HTTPException(status_code=404, detail=f"unknown horen subject: {slug}")
    return agent


def _user_tier(user: User) -> str:
    """Classify the user for quota purposes. Returns 'pro', 'trial', or 'expired'."""
    if user.is_pro:
        return "pro"
    if user.trial_ends_at is not None:
        # Normalize to UTC-aware for comparison (column is naive UTC).
        trial_end = user.trial_ends_at
        if trial_end.tzinfo is None:
            trial_end = trial_end.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) < trial_end:
            return "trial"
    return "expired"


def _horen_quota_status(user: User, db: Session) -> dict:
    """Compute Hören usage / limit / remaining for the current user.

    Returns a dict the frontend can render directly:
      { tier, limit, used, remaining, period, can_generate, reason,
        next_available_at }
    Where `period` is "week" for Pro (rolling 7 days) and "trial" for trial users.
    `next_available_at` is set only when the Pro user is over the cap: it's the
    timestamp when the oldest exam in the current window falls out, freeing up
    one slot. The frontend can render this as "next exam available in N hours".
    """
    tier = _user_tier(user)
    now = datetime.now(timezone.utc)

    if tier == "pro":
        limit = HOREN_QUOTA_PRO_PER_WEEK
        # Rolling 7-day window — anything generated within the last 7 days counts.
        window_start = now - HOREN_QUOTA_PRO_WINDOW
        # The Quiz.generation_date column is naive UTC, so compare against a
        # naive UTC value to keep SQLAlchemy from complaining.
        window_start_naive = window_start.replace(tzinfo=None)

        recent = (
            db.query(Quiz)
            .filter(
                Quiz.user_id == user.id,
                Quiz.quiz_type == "audio_listening",
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
            # When the oldest exam in the window falls out (7 days after it was
            # generated), one slot frees up. That's the next-available moment.
            oldest = recent[0].generation_date
            if oldest.tzinfo is None:
                oldest = oldest.replace(tzinfo=timezone.utc)
            next_available_at = (oldest + HOREN_QUOTA_PRO_WINDOW).isoformat()

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
        limit = HOREN_QUOTA_TRIAL_LIFETIME
        # Lifetime-within-trial — count all audio_listening quizzes ever.
        used = (
            db.query(Quiz)
            .filter(
                Quiz.user_id == user.id,
                Quiz.quiz_type == "audio_listening",
            )
            .count()
        )
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

    # Expired / no subscription — Hören is fully gated behind Pro.
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
    """Same idempotent pattern as the main predefined_router."""
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
async def create_horen_quiz(
    db: DBSession,
    current_user: CurrentUser,
    payload: GenerateHorenRequest = Body(default_factory=GenerateHorenRequest),
    slug: str = PathParam(...),
):
    """Generate a fresh full Hören exam (all 4 Teile) and persist it as a Quiz row.

    Synchronous: the caller waits ~2 minutes while scripts are generated and
    audio is rendered for each of the 4 Teile. The frontend shows a progress
    overlay explaining the wait — it's the cost of producing exam-realistic
    listening material on demand.
    """
    agent = _resolve_horen_agent(slug)

    # Quota check BEFORE generation — don't burn Gemini calls and audio render
    # time on a request we're going to reject anyway.
    quota = _horen_quota_status(current_user, db)
    if not quota["can_generate"]:
        if quota["reason"] == "weekly_limit_reached":
            next_at = quota.get("next_available_at")
            when = f" Your next exam unlocks at {next_at}." if next_at else ""
            detail = (
                f"You've used all {quota['limit']} Hören exams in the last 7 days.{when}"
            )
            status_code = 429
        elif quota["reason"] == "trial_limit_reached":
            detail = (
                f"Your trial includes {quota['limit']} Hören exam. "
                f"Upgrade to Pro for {HOREN_QUOTA_PRO_PER_WEEK} Hören exams per week."
            )
            status_code = 402
        else:  # subscription_required
            detail = "Hören requires an active subscription. Upgrade to Pro to generate listening exams."
            status_code = 402
        raise HTTPException(status_code=status_code, detail=detail)

    # Run the (slow, blocking) generation pipeline off the event loop so other
    # requests aren't starved while Gemini + TTS + ffmpeg do their work.
    try:
        manifest = await asyncio.to_thread(
            generate_full_exam,
            HOREN_AUDIO_DIR,
            provider_name=payload.provider or "edge_tts",
            audio_url_prefix=AUDIO_URL_PREFIX,
        )
    except Exception as e:
        # Log the full traceback so it's visible in the uvicorn terminal —
        # otherwise the exception gets buried in the 502 response body and
        # is invisible unless the caller inspects the network response.
        logger.exception("Hören full-exam generation failed for user %s", current_user.id)
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
        quiz_type="audio_listening",
        title=full_exam_title(),
        num_questions=len(manifest["questions"]),
        time_limit=None,  # Hören exams are self-paced; per-Teil play_limit gates pacing
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
async def get_horen_quota(
    db: DBSession,
    current_user: CurrentUser,
    slug: str = PathParam(...),
):
    """Current user's Hören usage and remaining quota for this period.
    The library page hits this on mount to show the 'X of 10 left this month'
    badge and to know whether to disable the Generate button."""
    _resolve_horen_agent(slug)
    return _horen_quota_status(current_user, db)


@router.get("/{slug}/sessions")
async def list_user_sessions(
    db: DBSession,
    current_user: CurrentUser,
    slug: str = PathParam(...),
):
    """User's previous Hören sessions, most recent first, with score if taken.
    Drives the library page on /horen/<slug>."""
    agent = _resolve_horen_agent(slug)

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
            Quiz.quiz_type == "audio_listening",
        )
        .order_by(Quiz.generation_date.desc())
        .all()
    )

    # Most recent QuizResult per quiz (some quizzes may have none).
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
        kind = content.get("kind")
        teile = content.get("teile") or []
        # Full-exam shape: report counts; legacy single-Teil shape: report the Teil.
        if kind == "full_exam":
            num_teile = len(teile)
            teil_label = None
        else:
            num_teile = 1 if content.get("questions") else 0
            teil_label = content.get("teil_name") or content.get("teil")
        result = latest_results.get(q.id)
        sessions.append({
            "quiz_id": str(q.id),
            "title": q.title,
            "kind": kind or "single_teil",
            "num_teile": num_teile,
            "teil_label": teil_label,
            "num_questions": q.num_questions,
            "generated_at": q.generation_date.isoformat() if q.generation_date else None,
            "latest_score": float(result.score_percentage) if result else None,
            "taken_at": result.attempt_date.isoformat() if result and result.attempt_date else None,
        })

    return {"subject_slug": slug, "sessions": sessions}
