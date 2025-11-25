from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime

DATABASE_URL = "postgresql+psycopg2://user:password@host:port/dbname"

# 1. Create the SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# 2. Define the Base Class
# All your ORM models will inherit from this Base
Base = declarative_base()

# 3. Create a Session Local class
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from .database import Base # Import the Base class you defined
import uuid
from datetime import datetime

# --- Utility Functions ---
# Helper to get the default UUID
def generate_uuid():
    return uuid.uuid4()

# --- 1. Authentication Models ---

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    stripe_customer_id = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False) # e.g., 'active', 'trialing'
    ends_at = Column(TIMESTAMP)
    
    # Define relationship back to User (one-to-one)
    user = relationship("User", back_populates="subscription")


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    quiz_sources = relationship("QuizSource", back_populates="owner")
    quiz_results = relationship("QuizResult", back_populates="user")


# --- 2. Quiz Content and Source Models ---

class QuizSource(Base):
    __tablename__ = "quiz_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    storage_path = Column(String, nullable=False) # Cloud Storage URL/Path
    file_name = Column(String(255), nullable=False)
    extracted_text = Column(String) # Stores the raw text
    upload_date = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="quiz_sources")
    quizzes = relationship("Quiz", back_populates="source")


class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    source_id = Column(UUID(as_uuid=True), ForeignKey("quiz_sources.id", ondelete="CASCADE"), nullable=False)
    num_questions = Column(Integer, nullable=False)
    content = Column(JSONB, nullable=False) # The structured JSON output from Gemini
    generation_date = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    source = relationship("QuizSource", back_populates="quizzes")
    quiz_results = relationship("QuizResult", back_populates="quiz")


# --- 3. Assessment and History Models ---

class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score_percentage = Column(Numeric(5, 2), nullable=False) # e.g., 85.50
    is_passed = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer)
    user_answers = Column(JSONB, nullable=False) # The user's selections
    attempt_date = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    quiz = relationship("Quiz", back_populates="quiz_results")
    user = relationship("User", back_populates="quiz_results")