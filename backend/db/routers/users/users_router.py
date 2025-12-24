# routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from db.models import User
from schemas import UserAdminResponse, UserResponse, UserUpdate
from db.dependency import get_db, get_current_user
from db.services.user import User as user_service
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

# @router.post("/", status_code=201)
# def create_user_endpoint(user_data: UserCreate, db: DBSession):
    
#     if user_service.get_user_by_email(db, email=user_data.email):
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # 2. Hash the password before sending it to the database function
#     # NOTE: You MUST implement a secure hashing function (e.g., using bcrypt)
#     hashed_password = hash_password(user_data.password) 
    
#     # 3. Call the service function with the hashed password
#     new_user = user_service.create_user(
#         db=db, 
#         email=user_data.email, 
#         hashed_password=user_data.passwor
#     )
    
#     return new_user



@router.get("/me", response_model=UserAdminResponse)
def get_my_profile(current_user: CurrentUser):
    return current_user


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



