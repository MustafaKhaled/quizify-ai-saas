from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from db.dependency import get_db
from db import models
import schemas, security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Dependencies
db_dep = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=schemas.AuthenticationSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.UserCreate, db: db_dep):
    expiration_date = datetime.utcnow() + timedelta(minutes=5),
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_pwd = security.hash_password(user_in.password[:72])
    new_user = models.User( 
        email=user_in.email,
        hashed_password=hashed_pwd,
        name = user_in.name,
        trial_ends_at=expiration_date,
        is_pro=False,
        is_admin=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate token
    access_token = security.create_access_token(data={"sub": new_user.email})
    
    return {
        **new_user.__dict__,
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=schemas.AuthenticationSuccessResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: db_dep
):
    # 1. Find the user
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Verify password
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Create token
    access_token = security.create_access_token(data={"sub": user.email})
    
    return {**user.__dict__, "access_token": access_token, "token_type": "bearer"}