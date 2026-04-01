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

class SubscriptionInfo(BaseModel):
    status: str          # trial, active_monthly, active_yearly, expired
    label: str           # "Pro Monthly", "Trial (5d left)"
    is_eligible: bool    # Quick boolean for the UI to enable/disable AI buttons
    ends_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    status_label: Optional[str] = None

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
    subscription: Optional[SubscriptionInfo] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthenticationSuccessResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserAdminResponse


class SubjectCreate(BaseModel):
    name: str
    color: Optional[str] = None

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class SubjectResponse(BaseModel):
    id: UUID
    name: str
    color: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SubjectDetailResponse(SubjectResponse):
    source_count: int = 0
    quiz_count: int = 0


class QuizResponse(BaseModel):
    id: UUID
    source_id: Optional[UUID] = None
    subject_id: Optional[UUID] = None
    title: str
    quiz_type: str
    num_questions: Optional[int]
    time_limit: Optional[int]
    content: dict
    topics: Optional[dict] = None
    generation_date: datetime

    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    question_index: int
    # Can be an int for single_choice or a list of ints for multiple_select
    selected_options: Optional[Union[int, List[int]]] = []

class QuizSubmission(BaseModel):
    quiz_id: UUID
    answers: List[AnswerSubmission]
    started_at: Optional[datetime] = None  # ISO timestamp from frontend when quiz page loaded

class CheckoutRequest(BaseModel):
    price_id: str

class QuizSourceResponse(BaseModel):
    id: UUID
    file_name: str
    upload_date: datetime
    start_page: Optional[int] = None
    end_page: Optional[int] = None

    class Config:
        from_attributes = True

class UserDetailResponse(UserAdminResponse):
    quiz_sources: List[QuizSourceResponse] = []
    quizzes: List[QuizResponse] = []

    class Config:
        from_attributes = True