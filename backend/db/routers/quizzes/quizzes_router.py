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

# Define the router instance
router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

@router.get("/my_quizzes", response_model=list[QuizResponse])
async def get_my_quizzes(
    db: db_dep,
    current_user: CurrentUser,
):
    print("Fetching quizzes for user:", current_user.id)
    quizzes = (
        db.query(Quiz)
        .filter(Quiz.user_id == current_user.id)
        .order_by(Quiz.generation_date.desc())
        .all()
    )

    return quizzes

@router.get("/{quiz_id}", response_model=list[QuizResponse])
async def get_my_quizzes(
    db: db_dep,
    _: CurrentUser,
    quiz_id: str,
):
    print("Fetching quiz:", id)
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
    quiz = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id)
        .first()
    )
    if not quiz:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(quiz)
    db.commit()
    return quiz

@router.post("/submit/{quiz_id}", status_code=201, response_model=dict)
async def submit(
    submission: QuizSubmission,
    db: db_dep,
    currentUser: CurrentUser
):
# 1. Fetch Quiz and verify existence
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # 2. Score the quiz based on its defined type
    score_pct, breakdown = calculate_quiz_score(
        quiz.content, 
        quiz.quiz_type, # This comes from your DB column
        submission.answers
    )

    # 3. Create the Result record
    new_result = QuizResult(
        id=uuid.uuid4(),
        quiz_id=quiz.id,
        user_id=currentUser.id,
        score_percentage=score_pct,
        is_passed=score_pct >= 70.0,  # Hardcoded 70% pass mark
        time_taken_seconds=submission.time_taken_seconds,
        user_answers=breakdown,        # Detailed JSON breakdown for review
        attempt_date=datetime.utcnow()
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
import uuid

@router.get("/my_results")
async def get_my_results(
    db: db_dep,
    currentUser: CurrentUser
):
    """Get all quiz results for the current user"""
    results = (
        db.query(QuizResult)
        .filter(QuizResult.user_id == currentUser.id)
        .order_by(QuizResult.attempt_date.desc())
        .all()
    )

    return results

@router.get("/performance/by-topic")
async def get_performance_by_topic(
    db: db_dep,
    currentUser: CurrentUser
):
    """Analyze user's performance across all topics"""
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
                topic_stats[topic] = {
                    "total": 0,
                    "correct": 0,
                    "accuracy": 0
                }

            topic_stats[topic]["total"] += 1
            if answer.get("is_correct"):
                topic_stats[topic]["correct"] += 1

    # Calculate accuracy percentages
    for topic, stats in topic_stats.items():
        if stats["total"] > 0:
            stats["accuracy"] = round((stats["correct"] / stats["total"]) * 100, 2)

    # Identify weak topics (below 70% accuracy)
    weak_topics = [
        {"topic": topic, **stats}
        for topic, stats in topic_stats.items()
        if stats["accuracy"] < 70.0 and stats["total"] >= 3  # At least 3 questions
    ]

    return {
        "all_topics": topic_stats,
        "weak_topics": sorted(weak_topics, key=lambda x: x["accuracy"])
    }

@router.get("/results/{quiz_id}") # Removed response_model=list[QuizResult] to avoid recursion
async def get_quiz_results(
    quiz_id: uuid.UUID,
    db: db_dep,
    currentUser: CurrentUser
):
    results = (
        db.query(QuizResult)
        .filter(
            QuizResult.quiz_id == quiz_id,
            QuizResult.user_id == currentUser.id  # IMPORTANT: Security filter
        )
        .order_by(QuizResult.attempt_date.desc())
        .all()
    )

    if not results:
        # It's better to return an empty list than a 404
        # so the frontend knows the user just hasn't attempted it yet.
        return []

    return results

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

    # We return the stored breakdown from the database plus quiz info for navigation
    return {
        "score": result.score_percentage,
        "date": result.attempt_date,
        "breakdown": result.user_answers,  # This is the JSONB we saved earlier
        "quiz": {
            "id": result.quiz.id,
            "source_id": result.quiz.source_id,
            "title": result.quiz.title
        }
    }

def calculate_quiz_score(quiz_content: dict, quiz_type: str, user_answers: list):
    questions = quiz_content.get("questions", [])
    total_questions = len(questions)
    correct_count = 0
    detailed_results = []

    # Map user answers by question index for quick lookup
    # Expecting: {0: 1} or {0: [1, 3]}
    user_map = {a.question_index: a.selected_options for a in user_answers}

    for i, q in enumerate(questions):
        user_choice = user_map.get(i)
        is_correct = False

        if quiz_type == "multiple_select":
            # STRICT LOGIC: Selected must match correct exactly
            correct_indices = q.get("correct_option_indices", [])
            if isinstance(user_choice, list):
                # Using sets to ignore order, but compare exact values
                if set(user_choice) == set(correct_indices):
                    is_correct = True
        
        else: # single_choice
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
