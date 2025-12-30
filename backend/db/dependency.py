from typing import Generator
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import status
from db.models import User
import jwt
from .database import SessionLocal # Import the SessionLocal class
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
# This is the function that will be injected into your routes
def get_db() -> Generator[Session, None, None]:
    """
    Provides a new SQLAlchemy session for each request,
    and ensures it's closed afterwards.
    """
    db = SessionLocal()
    try:
        # 'yield' makes this function a generator dependency
        yield db 
    except Exception:
        # Rollback the session if any unhandled error occurs
        db.rollback()
        raise
    finally:
        # Always close the session after the request is complete
        db.close()

# 1. Config

# 2. Token extraction setup
# This tells FastAPI to look for the "Authorization: Bearer <token>" header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decodes the token, validates it, and fetches the user from the DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    # Fetch user from DB to ensure they still exist and token is valid
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    An extension of get_current_user that checks for admin status.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="The user does not have enough privileges"
        )
    return current_user