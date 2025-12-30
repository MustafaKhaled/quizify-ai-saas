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
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="subscription")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    # Relationships with Cascade Delete
    # If a User is deleted, everything below is wiped automatically
    subscription = relationship(
        "Subscription", 
        back_populates="user", 
        uselist=False, 
        cascade="all, delete-orphan"
    )
    quiz_sources = relationship(
        "QuizSource", 
        back_populates="owner", 
        cascade="all, delete-orphan"
    )
    # Changed back_populates to quiz_results to match the QuizResult class
    quiz_results = relationship(
        "QuizResult", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )


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
    # If a Source (PDF) is deleted, all quizzes generated from it are deleted
    quizzes = relationship(
        "Quiz", 
        back_populates="source", 
        cascade="all, delete-orphan"
    )


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("quiz_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    
    quiz_type = Column(String, nullable=True, default="single_choice")
    title = Column(String(255), nullable=False)
    time_limit = Column(Integer, nullable=True) # in minutes
    num_questions = Column(Integer, nullable=False)
    content = Column(JSONB, nullable=False) 
    generation_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    source = relationship("QuizSource", back_populates="quizzes")
    owner = relationship("User")
    
    # If a Quiz is deleted, all historical results for it are wiped
    quiz_results = relationship(
        "QuizResult", 
        back_populates="quiz", 
        cascade="all, delete-orphan"
    )

# -------------------------------
# 3. Assessment / Results Models
# ----------------