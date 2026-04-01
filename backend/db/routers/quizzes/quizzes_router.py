from datetime import datetime
from typing import Annotated
import uuid
import streamlit as st
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv

from schemas import QuizResponse, QuizSubmission


load_dotenv()

st.set_page_config(page_title="PDF to Quiz Builder", layout="wide")

from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizResult, User

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
db_dep = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

# ── Static routes MUST come before /{quiz_id} ────────────────────────────────

@router.get("/my_quizzes", response_model=list[QuizResponse])
async def get_my_quizzes(
    db: db_dep,
    current_user: CurrentUser,
):
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.user_id == current_user.id)
        .order_by(Quiz.generation_date.desc())
        .all()
    )
    return quizzes


@router.get("/my_results")
async def get_my_results(
    db: db_dep,
    currentUser: CurrentUser
):
    results = (
        db.query(QuizResult)
        .filter(QuizResult.user_id == currentUser.id)
        .order_by(QuizResult.attempt_date.desc())
        .all()
    )
    return [
        {
            "id": str(r.id),
            "quiz_id": str(r.quiz_id),
            "score_percentage": float(r.score_percentage),
            "is_passed": r.is_passed,
            "attempt_date": r.attempt_date.isoformat() if r.attempt_date else None,
            "user_answers": r.user_answers or [],
            "time_taken_seconds": r.time_taken_seconds,
        }
        for r in results
    ]


@router.get("/performance/by-topic")
async def get_performance_by_topic(
    db: db_dep,
    currentUser: CurrentUser
):
    results = (
        db.query(QuizResult)
        .join(Quiz)
        .filter(QuizResult.user_id == currentUser.id)
        .all()
    )

    topic_stats = {}

    for result in results:
        quiz = result.quiz
        if not quiz.content.get("questions"):
            continue

        for answer in result.user_answers:
            topic = answer.get("topic", "Unknown")
            if topic not in topic_stats:
                topic_stats[topic] = {"total": 0, "correct": 0, "accuracy": 0}
            topic_stats[topic]["total"] += 1
            if answer.get("is_correct"):
                topic_stats[topic]["correct"] += 1

    for topic, stats in topic_stats.items():
        if stats["total"] > 0:
            stats["accuracy"] = round((stats["correct"] / stats["total"]) * 100, 2)

    weak_topics = [
        {"topic": topic, **stats}
        for topic, stats in topic_stats.items()
        if stats["accuracy"] < 70.0 and stats["total"] >= 3
    ]

    return {
        "all_topics": topic_stats,
        "weak_topics": sorted(weak_topics, key=lambda x: x["accuracy"])
    }


@router.post("/submit/{quiz_id}", status_code=201, response_model=dict)
async def submit(
    submission: QuizSubmission,
    db: db_dep,
    currentUser: CurrentUser
):
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    score_pct, breakdown = calculate_quiz_score(
        quiz.content,
        quiz.quiz_type,
        submission.answers
    )

    ended_at = datetime.utcnow()
    started_at = submission.started_at.replace(tzinfo=None) if submission.started_at else None
    time_taken_seconds = int((ended_at - started_at).total_seconds()) if started_at else None
    time_remaining_seconds = None
    if quiz.time_limit and time_taken_seconds is not None:
        total_seconds = quiz.time_limit * 60
        time_remaining_seconds = max(0, total_seconds - time_taken_seconds)

    new_result = QuizResult(
        id=uuid.uuid4(),
        quiz_id=quiz.id,
        user_id=currentUser.id,
        score_percentage=score_pct,
        is_passed=score_pct >= 70.0,
        time_taken_seconds=time_taken_seconds,
        time_remaining_seconds=time_remaining_seconds,
        started_at=started_at,
        ended_at=ended_at,
        user_answers=breakdown,
        attempt_date=ended_at
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return {
        "score": score_pct,
        "is_passed": new_result.is_passed,
        "result_id": new_result.id,
        "breakdown": breakdown
    }


@router.get("/results/{quiz_id}")
async def get_quiz_results(
    quiz_id: uuid.UUID,
    db: db_dep,
    currentUser: CurrentUser
):
    results = (
        db.query(QuizResult)
        .filter(
            QuizResult.quiz_id == quiz_id,
            QuizResult.user_id == currentUser.id
        )
        .order_by(QuizResult.attempt_date.desc())
        .all()
    )
    return results if results else []


@router.get("/result/{result_id}/review")
async def get_result_review(
    result_id: uuid.UUID,
    db: db_dep,
    currentUser: CurrentUser
):
    result = db.query(QuizResult).filter(
        QuizResult.id == result_id,
        QuizResult.user_id == currentUser.id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    quiz = result.quiz
    source_subject_id = quiz.source.subject_id if quiz.source else None

    return {
        "score": float(result.score_percentage),
        "date": result.attempt_date,
        "breakdown": result.user_answers,
        "quiz": {
            "id": str(quiz.id),
            "source_id": str(quiz.source_id) if quiz.source_id else None,
            "subject_id": str(quiz.subject_id) if quiz.subject_id else None,
            "source_subject_id": str(source_subject_id) if source_subject_id else None,
            "title": quiz.title,
        }
    }


# ── Dynamic route LAST ────────────────────────────────────────────────────────

@router.get("/{quiz_id}", response_model=list[QuizResponse])
async def get_quiz(
    db: db_dep,
    _: CurrentUser,
    quiz_id: str,
):
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .order_by(Quiz.generation_date.desc())
        .all()
    )
    return quiz


@router.delete("/{quiz_id}", status_code=204)
async def delete_quiz(
    db: db_dep,
    _: CurrentUser,
    quiz_id: str,
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db.delete(quiz)
    db.commit()


# ── Scoring helper ────────────────────────────────────────────────────────────

def calculate_quiz_score(quiz_content: dict, quiz_type: str, user_answers: list):
    questions = quiz_content.get("questions", [])
    total_questions = len(questions)
    correct_count = 0
    detailed_results = []

    user_map = {a.question_index: a.selected_options for a in user_answers}

    for i, q in enumerate(questions):
        user_choice = user_map.get(i)
        is_correct = False

        if quiz_type == "multiple_select":
            correct_indices = q.get("correct_option_indices", [])
            if isinstance(user_choice, list):
                if set(user_choice) == set(correct_indices):
                    is_correct = True
        else:  # single_choice and true_or_false
            correct_index = q.get("correct_option_index")
            if user_choice == correct_index:
                is_correct = True

        if is_correct:
            correct_count += 1

        detailed_results.append({
            "question_index": i,
            "topic": q.get("topic", "Unknown"),
            "is_correct": is_correct,
            "user_choice": user_choice,
            "correct_answer": q.get("correct_option_indices") if quiz_type == "multiple_select" else q.get("correct_option_index"),
            "explanation": q.get("explanation", "")
        })

    score_pct = (correct_count / total_questions * 100) if total_questions > 0 else 0
    return round(score_pct, 2), detailed_results
