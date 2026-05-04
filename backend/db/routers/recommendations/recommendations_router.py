"""
Recommendation endpoints driven by the user's quiz history.

Behavior signal: every QuizResult.user_answers item carries a `topic` and
`is_correct` flag. We aggregate per-topic stats across all of a user's
results and surface the topics with the lowest accuracy as practice targets.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from agents import PREDEFINED_AGENTS
from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizResult, QuizSource, Subject, User


def _resolve_predefined_origin(topic: str) -> tuple[str | None, str | None]:
    """If `topic` matches a chapter name in any registered agent, return (slug, chapter_slug)."""
    for agent in PREDEFINED_AGENTS.values():
        for ch in agent["chapters"]:
            if ch["name"] == topic:
                return agent["slug"], ch["slug"]
    return None, None

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def _aggregate_topic_stats(results: list[QuizResult]) -> dict:
    """topic -> {total, correct, quiz_ids: set}"""
    stats: dict[str, dict] = {}
    for r in results:
        for ans in (r.user_answers or []):
            topic = (ans.get("topic") or "Unknown").strip()
            if not topic:
                continue
            entry = stats.setdefault(
                topic, {"total": 0, "correct": 0, "quiz_ids": set()}
            )
            entry["total"] += 1
            if ans.get("is_correct"):
                entry["correct"] += 1
            entry["quiz_ids"].add(str(r.quiz_id))
    return stats


@router.get("/weak-topics")
async def get_weak_topics(
    db: DBSession,
    current_user: CurrentUser,
    min_attempts: int = 2,
    accuracy_threshold: float = 0.7,
    limit: int = 5,
):
    """
    Return the user's weakest topics across all quiz history.

    A topic is "weak" when it has at least `min_attempts` answered questions
    and accuracy below `accuracy_threshold`. Results are sorted by accuracy
    ascending (worst first) and capped to `limit`.

    Each result includes:
      - topic, total, correct, accuracy
      - origin: "pmp" if the topic matches a PMP chapter, else "user"
      - subject_id / subject_name when the topic appears in a quiz tied to a subject
      - source_id / source_name when the topic appears in a quiz tied to a source
      - chapter_slug for PMP topics (so the frontend can deep-link to a focused PMP quiz)
    """
    results = (
        db.query(QuizResult).filter(QuizResult.user_id == current_user.id).all()
    )
    stats = _aggregate_topic_stats(results)

    # Pre-load quiz/source/subject lookups in two queries to avoid N+1
    all_quiz_ids = {qid for entry in stats.values() for qid in entry["quiz_ids"]}
    quizzes = (
        db.query(Quiz).filter(Quiz.id.in_(all_quiz_ids)).all() if all_quiz_ids else []
    )
    quiz_lookup = {str(q.id): q for q in quizzes}
    source_ids = {str(q.source_id) for q in quizzes if q.source_id}
    sources = (
        db.query(QuizSource).filter(QuizSource.id.in_(source_ids)).all()
        if source_ids
        else []
    )
    source_lookup = {str(s.id): s for s in sources}
    subject_ids = {str(q.subject_id) for q in quizzes if q.subject_id} | {
        str(s.subject_id) for s in sources if s.subject_id
    }
    subjects = (
        db.query(Subject).filter(Subject.id.in_(subject_ids)).all()
        if subject_ids
        else []
    )
    subject_lookup = {str(s.id): s for s in subjects}

    out = []
    for topic, entry in stats.items():
        if entry["total"] < min_attempts:
            continue
        accuracy = entry["correct"] / entry["total"]
        if accuracy >= accuracy_threshold:
            continue

        # Pick a representative quiz for context (the most recent)
        representative_quiz = None
        for qid in entry["quiz_ids"]:
            q = quiz_lookup.get(qid)
            if q and (
                representative_quiz is None
                or (q.generation_date or 0) > (representative_quiz.generation_date or 0)
            ):
                representative_quiz = q

        subject_id = None
        subject_name = None
        source_id = None
        source_name = None
        if representative_quiz:
            if representative_quiz.subject_id:
                subj = subject_lookup.get(str(representative_quiz.subject_id))
                if subj:
                    subject_id = str(subj.id)
                    subject_name = subj.name
            if representative_quiz.source_id:
                src = source_lookup.get(str(representative_quiz.source_id))
                if src:
                    source_id = str(src.id)
                    source_name = src.name or src.file_name
                    if not subject_id and src.subject_id:
                        subj = subject_lookup.get(str(src.subject_id))
                        if subj:
                            subject_id = str(subj.id)
                            subject_name = subj.name

        # Predefined-subject origin detection — match by chapter name across all agents
        origin_slug, chapter_slug = _resolve_predefined_origin(topic)
        origin = origin_slug if origin_slug else "user"

        out.append({
            "topic": topic,
            "total": entry["total"],
            "correct": entry["correct"],
            "accuracy": round(accuracy * 100, 1),
            "origin": origin,
            "chapter_slug": chapter_slug,
            "subject_id": subject_id,
            "subject_name": subject_name,
            "source_id": source_id,
            "source_name": source_name,
        })

    out.sort(key=lambda x: x["accuracy"])
    return out[:limit]
