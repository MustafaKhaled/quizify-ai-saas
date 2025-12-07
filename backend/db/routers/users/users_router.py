# routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated # Required for dependency injection annotation
from ...dependency import get_db # Assuming this is the correct path/file
from ...services.user import User as user_service
from pydantic import BaseModel # To define the expected request body

# Define the Pydantic model for incoming data
class UserCreate(BaseModel):
    email: str
    password: str

# Define a type alias for cleaner code
DBSession = Annotated[Session, Depends(get_db)]

# Define the router instance
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=201)
# 1. Inject the Pydantic model (data) and the Session dependency (db)
def create_user_endpoint(user_data: UserCreate, db: DBSession):
    
    # Check if user exists (Good practice to put this validation here or in the service)
    if user_service.get_user_by_email(db, email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password before sending it to the database function
    # NOTE: You MUST implement a secure hashing function (e.g., using bcrypt)
    hashed_password = hash_password(user_data.password) 
    
    # 3. Call the service function with the hashed password
    new_user = user_service.create_user(
        db=db, 
        email=user_data.email, 
        hashed_password=hashed_password
    )
    
    return new_user
@router.get("/")
def get_all_users_endpoint(db: DBSession):
    return user_service.get_all_users(db)


@router.get("/{email}")
def get_user_by_email_endpoint(email: str, db: DBSession):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Dummy function for the example - replace with real hashing logic
def hash_password(password: str) -> str:
    return f"HASHED_{password}"

