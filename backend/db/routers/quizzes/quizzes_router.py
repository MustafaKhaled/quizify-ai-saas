from typing import Annotated
import streamlit as st
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
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