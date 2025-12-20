import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")