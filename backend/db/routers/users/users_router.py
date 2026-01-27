# routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.models import User
from schemas import UserAdminResponse, UserResponse, UserUpdate
from db.dependency import get_db, get_current_user
from db.routers.util import build_user_response
from security import hash_password
from pydantic import BaseModel # To define the expected request body


# Define a type alias for cleaner code
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Define the router instance
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserAdminResponse)
def get_my_profile(current_user: CurrentUser, db: DBSession):
    # Access subscription to trigger lazy load if needed
    _ = current_user.subscription
    
    # Build user response with subscription info and counts
    user_data = build_user_response(current_user, db)
    return user_data


@router.patch("/me", response_model=UserResponse)
def update_my_profile(
    user_update: UserUpdate, 
    db: DBSession, 
    current_user: CurrentUser
):
    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user



@router.get("/{email}")
def get_user_by_email_endpoint(email: str, db: DBSession):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



