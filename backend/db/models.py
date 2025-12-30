# models.py

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, ForeignKey,
    TIMESTAMP, Numeric, Boolean
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from db.database import Base


def generate_uuid():
    return uuid.uuid4()


# -------------------------
# 1. Authentication Models
# -------------------------
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    stripe_customer_id = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False)
    ends_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), nullable= True)

    user = relationship("User", back_populates="subscription")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    Column(Boolean, default=False, server_default="false", nullable=False)  # Admin flag
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    quiz_sources = relationship("QuizSource", back_populates="owner", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")


# --------------------------------
# 2. Quiz Source & Content Models
# --------------------------------
class QuizSource(Base):
    __tablename__ = "quiz_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(String)
    upload_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="quiz_sources")
    quizzes = relationship("Quiz", back_populates="source")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    # Direct link to user for faster queries
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("quiz_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    quiz_type = Column(String, nullable=True, default="single_choice")
    # New Fields
    title = Column(String(255), nullable=False) # The Quiz Name
    time_limit = Column(Integer, nullable=True) # Optional timer in minutes
    
    num_questions = Column(Integer, nullable=False)
    content = Column(JSONB, nullable=False) # Stores the Gemini output
    generation_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    source = relationship("QuizSource", back_populates="quizzes")
    owner = relationship("User") # Direct relationship to User
    quiz_results = relationship("QuizResult", back_populates="quiz")

# -------------------------------
# 3. Assessment / Results Models
# -------------------------------
class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score_percentage = Column(Numeric(5, 2), nullable=False)
    is_passed = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer)
    user_answers = Column(JSONB, nullable=False)
    attempt_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    quiz = relationship("Quiz", back_populates="quiz_results")
    user = relationship("User", back_populates="quiz_results")
