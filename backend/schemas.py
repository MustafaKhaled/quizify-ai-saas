from pydantic import BaseModel, EmailStr, Field
from uuid import UUID  # Import the class, not just the module
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    id: UUID  # Use UUID (capitalized)
    email: EmailStr

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    is_admin: Optional[bool] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=72)

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    
    class Config:
        from_attributes = True

class UserAdminResponse(UserResponse):
    created_at: Optional[datetime] = None 
    is_admin: Optional[bool] = None
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthenticationSuccessResponse(UserAdminResponse):
    access_token: str
    token_type: str = "bearer"


class QuizResponse(BaseModel):
    id: UUID
    source_id: UUID
    title: str
    num_questions: Optional[int]
    time_limit: Optional[int]
    content: dict  # The JSON questions
    generation_date: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read from SQLAlchemy models