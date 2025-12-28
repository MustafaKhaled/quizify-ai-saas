from typing import Annotated
import streamlit as st
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from dotenv import load_dotenv

from schemas import QuizResponse


load_dotenv()

st.set_page_config(page_title="PDF to Quiz Builder", layout="wide")

from db.dependency import get_current_user, get_db
from db.models import Quiz, User

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
