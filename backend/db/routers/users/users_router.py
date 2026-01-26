# routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.routers.util import get_detailed_status
from db.models import User
from schemas import UserAdminResponse, UserResponse, UserUpdate
from db.dependency import get_db, get_current_user
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
def get_my_profile(current_user: CurrentUser):
    # 1. Calculate the real-time status (Trial vs Pro vs Expired)
    sub_state = get_detailed_status(current_user)

    # 2. Build the response object to match UserAdminResponse
    return {
        # Spread the database fields (id, email, name, etc.)
        **current_user.__dict__,
        
        # Inject the calculated fields required by the schema
        "status_label": sub_state["label"],
        "subscription": sub_state,
        
        # Ensure counts are present (use getattr or a query if preferred)
        "quizzes_count": getattr(current_user, 'quizzes_count', 0),
        "sources_count": getattr(current_user, 'sources_count', 0)
    }


@router.patch("/me", response_model=UserResponse)
def update_my_profile(
    user_update: UserUpdate, 
    db: DBSession, 
    current_user: CurrentUser
):
    if user_update.name:
        current_user.name = user_update.name
    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)

    # 2. Fuse Subscription Data
    status_slug, status_label = get_detailed_status(current_user)
    
    # Add the calculated info to the response object
    current_user.subscription = {
        "status": status_slug,
        "label": status_label,
        "is_eligible": status_slug in ["trial", "active_monthly", "active_yearly"],
        "ends_at": current_user.subscription_end or current_user.trial_ends_at
    }

    return current_user



@router.get("/{email}")
def get_user_by_email_endpoint(email: str, db: DBSession):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



