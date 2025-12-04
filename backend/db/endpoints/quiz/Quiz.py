from sqlalchemy.orm import Session
from models import  QuizSource, Quiz, QuizResult
import uuid
from datetime import datetime

def create_quiz_source(db: Session, user_id: uuid.UUID, storage_path: str, file_name: str, extracted_text: str):
    source = QuizSource(
        id=uuid.uuid4(),
        user_id=user_id,
        storage_path=storage_path,
        file_name=file_name,
        extracted_text=extracted_text,
        upload_date=datetime.utcnow()
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source

# -------------------
# Quizzes
# -------------------
def create_quiz(db: Session, source_id: uuid.UUID, num_questions: int, content: dict):
    quiz = Quiz(
        id=uuid.uuid4(),
        source_id=source_id,
        num_questions=num_questions,
        content=content,
        generation_date=datetime.utcnow()
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz

# -------------------
# Quiz Results
# -------------------
def create_quiz_result(db: Session, quiz_id: uuid.UUID, user_id: uuid.UUID, score_percentage: float, is_passed: bool, user_answers: dict, time_taken_seconds: int | None = None):
    result = QuizResult(
        id=uuid.uuid4(),
        quiz_id=quiz_id,
        user_id=user_id,
        score_percentage=score_percentage,
        is_passed=is_passed,
        user_answers=user_answers,
        time_taken_seconds=time_taken_seconds,
        attempt_date=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result