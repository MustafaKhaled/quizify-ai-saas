from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from db.routers.util import build_user_response
from schemas import UserAdminResponse, UserDetailResponse, QuizSourceResponse, QuizResponse
from db.dependency import get_current_admin, get_db
from db import models
from sqlalchemy.orm import joinedload
from uuid import UUID
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

    db.delete(user)
    db.commit()


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
    
    # Add quizzes
    quizzes = db.query(models.Quiz).filter(
        models.Quiz.user_id == user_id
    ).all()
    user_data["quizzes"] = [
        {
            "id": q.id,
            "source_id": q.source_id,
            "title": q.title,
            "quiz_type": q.quiz_type,
            "num_questions": q.num_questions,
            "time_limit": q.time_limit,
            "content": q.content,
            "generation_date": q.generation_date
        }
        for q in quizzes
    ]
    
    return user_data


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
    
    db.delete(source)
    db.commit()


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
    
    db.delete(quiz)
    db.commit()
