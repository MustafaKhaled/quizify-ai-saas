import logging
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from agents import PREDEFINED_AGENTS
from db.routers.util import build_user_response
from schemas import UserAdminResponse, UserDetailResponse, QuizSourceResponse, QuizResponse
from db.dependency import get_current_admin, get_db
from db import models
from uuid import UUID

# Subject names registered as predefined agents. Any Quiz whose subject_id
# resolves to a Subject row with a name in this set is a predefined quiz
# (Hören / Lesen / Grammatik / PMP / CLF-C02). Everything else is a custom
# quiz built from the user's own QuizSource (uploaded PDF). The admin modal
# uses this to gate the per-question submission drill-down — only custom
# quizzes get the "View answers" affordance.
_PREDEFINED_SUBJECT_NAMES: frozenset[str] = frozenset(
    a["name"] for a in PREDEFINED_AGENTS.values()
)

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/admin",
    tags=["Adinmistration"]
)

db_dep = Annotated[Session, Depends(get_db)]
DBSession = Annotated[Session, Depends(get_db)]
CurrentAdmin = Annotated[models.User, Depends(get_current_admin)]

@router.get("/allusers", response_model=list[UserAdminResponse])
async def get_all_users(
    db: db_dep,
    _: CurrentAdmin
):
    users = db.query(models.User).options(joinedload(models.User.subscription)).all()
    return [build_user_response(user, db_session=db) for user in users] 


@router.delete("/user/email/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_email(
    email: str,
    db: db_dep,
    _: CurrentAdmin
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        # Surface the underlying DB error in the server log AND in the response
        # so the admin UI shows something actionable instead of a blind 500.
        logger.exception("Admin delete failed for user email=%s", email)
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete user: {type(e).__name__}: {e}",
        )


@router.get("/user/{user_id}", response_model=UserDetailResponse)
async def get_user_details(
    user_id: UUID,
    db: db_dep,
    _: CurrentAdmin
):
    """Get detailed information about a user including their quiz sources and quizzes"""
    user = db.query(models.User).filter(models.User.id == user_id).options(
        joinedload(models.User.subscription),
        joinedload(models.User.quiz_sources),
        joinedload(models.User.quiz_results)
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build base user response
    user_data = build_user_response(user, db_session=db)
    
    # Add quiz sources
    quiz_sources = db.query(models.QuizSource).filter(
        models.QuizSource.user_id == user_id
    ).all()
    user_data["quiz_sources"] = [
        {
            "id": qs.id,
            "file_name": qs.file_name,
            "upload_date": qs.upload_date,
            "start_page": qs.start_page,
            "end_page": qs.end_page
        }
        for qs in quiz_sources
    ]
    
    # Add quizzes — with score aggregates so the admin UI can show
    # latest_score / attempt_count badges without a per-quiz round trip.
    quizzes = db.query(models.Quiz).filter(
        models.Quiz.user_id == user_id
    ).all()
    quiz_ids = [q.id for q in quizzes]

    latest_by_quiz: dict = {}
    counts_by_quiz: dict = {}
    if quiz_ids:
        all_results = (
            db.query(models.QuizResult)
            .filter(models.QuizResult.quiz_id.in_(quiz_ids))
            .order_by(models.QuizResult.attempt_date.desc())
            .all()
        )
        for r in all_results:
            counts_by_quiz[r.quiz_id] = counts_by_quiz.get(r.quiz_id, 0) + 1
            # First seen wins because results are ordered desc by attempt_date.
            if r.quiz_id not in latest_by_quiz:
                latest_by_quiz[r.quiz_id] = r

    # Resolve subject names for every quiz in a single query so we can tag
    # each row as custom or predefined without N+1.
    subject_ids = {q.subject_id for q in quizzes if q.subject_id is not None}
    subject_name_by_id: dict = {}
    if subject_ids:
        subject_rows = (
            db.query(models.Subject.id, models.Subject.name)
            .filter(models.Subject.id.in_(subject_ids))
            .all()
        )
        subject_name_by_id = {sid: name for sid, name in subject_rows}

    def _is_custom(q: models.Quiz) -> bool:
        # A quiz is "custom" when it isn't tied to a predefined agent. Quizzes
        # without a subject_id are necessarily custom (no predefined agent
        # creates a Quiz with subject_id=NULL).
        if q.subject_id is None:
            return True
        name = subject_name_by_id.get(q.subject_id)
        return name not in _PREDEFINED_SUBJECT_NAMES

    user_data["quizzes"] = [
        {
            "id": q.id,
            "source_id": q.source_id,
            "subject_id": q.subject_id,
            "title": q.title,
            "quiz_type": q.quiz_type,
            "num_questions": q.num_questions,
            "time_limit": q.time_limit,
            "content": q.content,
            "generation_date": q.generation_date,
            "is_custom": _is_custom(q),
            "attempt_count": counts_by_quiz.get(q.id, 0),
            "latest_score": (
                float(latest_by_quiz[q.id].score_percentage)
                if q.id in latest_by_quiz else None
            ),
            "latest_attempt_at": (
                latest_by_quiz[q.id].attempt_date.isoformat()
                if q.id in latest_by_quiz and latest_by_quiz[q.id].attempt_date
                else None
            ),
        }
        for q in quizzes
    ]

    return user_data


@router.get("/quizzes/{quiz_id}/results")
async def get_quiz_results(
    quiz_id: UUID,
    db: db_dep,
    _: CurrentAdmin
):
    """Full attempt history for a quiz — every QuizResult row, newest first.
    Used by the customer-details modal when an admin clicks 'View attempts'."""
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    results = (
        db.query(models.QuizResult)
        .filter(models.QuizResult.quiz_id == quiz_id)
        .order_by(models.QuizResult.attempt_date.desc())
        .all()
    )

    return {
        "quiz_id": str(quiz.id),
        "quiz_title": quiz.title,
        "num_questions": quiz.num_questions,
        "attempts": [
            {
                "id": str(r.id),
                "score_percentage": float(r.score_percentage),
                "is_passed": r.is_passed,
                "time_taken_seconds": r.time_taken_seconds,
                "time_remaining_seconds": r.time_remaining_seconds,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "ended_at": r.ended_at.isoformat() if r.ended_at else None,
                "attempt_date": r.attempt_date.isoformat() if r.attempt_date else None,
                "user_answers": r.user_answers,
            }
            for r in results
        ],
    }


@router.delete("/quiz-sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz_source(
    source_id: UUID,
    db: db_dep,
    _: CurrentAdmin
):
    """Delete a quiz source and all associated quizzes"""
    source = db.query(models.QuizSource).filter(models.QuizSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Quiz source not found")

    try:
        db.delete(source)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Admin delete failed for quiz_source id=%s", source_id)
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete quiz source: {type(e).__name__}: {e}",
        )


@router.post("/users/{user_id}/reset-quota")
async def reset_user_quota(
    user_id: UUID,
    db: db_dep,
    _: CurrentAdmin,
):
    """Reset a user's per-feature quota window (Hören + Lesen).

    Sets quota_reset_at = now() so the user gets a full fresh allowance
    immediately. Used for support cases (e.g. user upgraded but webhook
    missed, manual is_pro flip, customer complaint).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.quota_reset_at = datetime.utcnow()
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Admin quota reset failed for user id=%s", user_id)
        raise HTTPException(
            status_code=500,
            detail=f"Could not reset quota: {type(e).__name__}: {e}",
        )

    return {
        "user_id": str(user.id),
        "email": user.email,
        "quota_reset_at": user.quota_reset_at.isoformat(),
    }


@router.delete("/quizzes/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: UUID,
    db: db_dep,
    _: CurrentAdmin
):
    """Delete a quiz"""
    quiz = db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    try:
        db.delete(quiz)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception("Admin delete failed for quiz id=%s", quiz_id)
        raise HTTPException(
            status_code=500,
            detail=f"Could not delete quiz: {type(e).__name__}: {e}",
        )
