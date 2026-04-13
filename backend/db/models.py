# models.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, DateTime, String, Integer, ForeignKey,
    TIMESTAMP, Numeric, Boolean, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from db.database import Base


def generate_uuid():
    return uuid.uuid4()


# --------------------------------
# 0. Subject Model
# --------------------------------
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    color = Column(String(7), nullable=True)  # hex color e.g. "#3B82F6"
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    owner = relationship("User", back_populates="subjects")
    sources = relationship("QuizSource", back_populates="subject")
    quizzes = relationship("Quiz", back_populates="subject", foreign_keys="Quiz.subject_id")


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
    created_at = Column(TIMESTAMP(timezone=True),default=datetime.utcnow,nullable=False)

    user = relationship("User", back_populates="subscription")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False, server_default="false", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_pro = Column(Boolean, default=False) # True only after Stripe payment
    is_verified = Column(Boolean, default=False, server_default="false", nullable=False)
    trial_ends_at = Column(DateTime, nullable=True) # The "Manual" gate
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    subjects = relationship("Subject", back_populates="owner", cascade="all, delete-orphan")
    quiz_sources = relationship("QuizSource", back_populates="owner", cascade="all, delete-orphan")
    quiz_results = relationship("QuizResult", back_populates="user", cascade="all, delete-orphan")


class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    token = Column(String, primary_key=True, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    token_hash = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User")


class OAuthState(Base):
    __tablename__ = "oauth_states"
    state = Column(String, primary_key=True, index=True)
    redirect_uri = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class EmailVerificationToken(Base):
    __tablename__ = "email_verification_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")


class HandoffCode(Base):
    __tablename__ = "handoff_codes"
    code = Column(String, primary_key=True, index=True)
    token = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    used = Column(Boolean, default=False, nullable=False)


# --------------------------------
# 2. Quiz Source & Content Models
# --------------------------------
class QuizSource(Base):
    __tablename__ = "quiz_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    name = Column(String(255), nullable=True)   # User-defined display name e.g. "Chapter 1"
    topics = Column(JSONB, nullable=True)        # AI-identified topics, set on first quiz generation
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(String)
    upload_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    start_page = Column(Integer, nullable=True)
    end_page = Column(Integer, nullable=True)
    owner = relationship("User", back_populates="quiz_sources")
    subject = relationship("Subject", back_populates="sources")
    quizzes = relationship("Quiz", back_populates="source", cascade="all, delete-orphan", foreign_keys="Quiz.source_id")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("quiz_sources.id", ondelete="CASCADE"), nullable=True, index=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True, index=True)
    quiz_type = Column(String, nullable=True, default="single_choice")
    title = Column(String(255), nullable=False)
    time_limit = Column(Integer, nullable=True)
    num_questions = Column(Integer, nullable=False)
    content = Column(JSONB, nullable=False)
    topics = Column(JSONB, nullable=True)
    generation_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    source = relationship("QuizSource", back_populates="quizzes", foreign_keys=[source_id])
    subject = relationship("Subject", back_populates="quizzes", foreign_keys=[subject_id])
    owner = relationship("User")
    quiz_results = relationship("QuizResult", back_populates="quiz", cascade="all, delete-orphan")

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
    time_taken_seconds = Column(Integer, nullable=True)
    time_remaining_seconds = Column(Integer, nullable=True)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    user_answers = Column(JSONB, nullable=False)
    attempt_date = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    quiz = relationship("Quiz", back_populates="quiz_results")
    user = relationship("User", back_populates="quiz_results")
