from pydantic import BaseModel, EmailStr, Field
from uuid import UUID  # Import the class, not just the module
from datetime import datetime
from typing import List, Optional, Union

class UserBase(BaseModel):
    id: UUID  # Use UUID (capitalized)
    email: EmailStr

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    # This MUST match the 'name' in your frontend fields array
    email: EmailStr    
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = Field(None, min_length=8, max_length=72)
    name: str
    is_admin: Optional[bool] = None
    is_pro: Optional[bool] = None
    expiration_date: Optional[datetime] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserAdminResponse(UserResponse):
    created_at: Optional[datetime] = None 
    is_admin: Optional[bool] = None
    is_pro: Optional[bool] = None
    quizzes_count: int = 0
    sources_count: int = 0
    subscription_status: str = "free" # trial, active, canceled, free
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthenticationSuccessResponse(UserAdminResponse):
    access_token: str
    token_type: str = "bearer"
    is_pro: Optional[bool] = None
    trial_ends_at: Optional[datetime] = None


class QuizResponse(BaseModel):
    id: UUID
    source_id: UUID
    title: str
    quiz_type: str
    num_questions: Optional[int]
    time_limit: Optional[int]
    content: dict  # The JSON questions
    generation_date: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read from SQLAlchemy models


class AnswerSubmission(BaseModel):
    question_index: int
    # Can be an int for single_choice or a list of ints for multiple_select
    selected_options: Optional[Union[int, List[int]]] = []

class QuizSubmission(BaseModel):
    quiz_id: UUID
    answers: List[AnswerSubmission]
    time_taken_seconds: Optional[int] = None  # Optional

class CheckoutRequest(BaseModel):
    price_id: str