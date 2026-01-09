from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from db.dependency import get_db
from db import models
import schemas, security
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

FRONTEND_URL = os.getenv("FRONTEND_URL")
BACKEND_URL = os.getenv("BACKEND_URL")

# Dependencies
db_dep = Annotated[Session, Depends(get_db)]

@router.post("/register", response_model=schemas.AuthenticationSuccessResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.UserCreate, db: db_dep):
    expiration_date = datetime.utcnow() + timedelta(minutes=5),
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not user_in.password:
        raise HTTPException(
            status_code=400, 
            detail="Password is required for standard registration."
        )

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

    if user and not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Looks like you Sign-up with Google, please use Google Login",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
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


@router.get('/google/login')
async def google_login(request: Request):
    # This URL is where Google sends the user back after login
    redirect_uri = f"{BACKEND_URL}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/google/callback')
async def google_callback(request: Request, db: db_dep):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get('userinfo')
    
    user = db.query(models.User).filter(models.User.email == user_info['email']).first()
    
    if not user:
        # 2. SIGN UP: Create new user if they don't exist
        user = models.User(
            email=user_info['email'],
            name=user_info['name']
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    my_token = security.create_access_token(data={"sub": user_info['email']})
    
    # 3. Redirect back to Nuxt with the token in the URL
    return RedirectResponse(url=f"{FRONTEND_URL}/auth/callback?token={my_token}")