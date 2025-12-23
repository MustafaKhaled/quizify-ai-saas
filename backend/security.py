from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
load_dotenv()
from db.dependency import SECRET_KEY, ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def hash_password(password: str) -> str:
    """
    Turns a plain text password into a secure hash.
    Used during Registration and Profile Updates.
    """
    print(f"DEBUG: Hashing string: '{password}' | Length: {len(password)}")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a login attempt password with the hash in the database.
    Used during Login.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Encodes data into a JWT using PyJWT.
    """
    to_encode = data.copy()
    
    # Calculate expiry
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # PyJWT uses 'exp' claim automatically
    to_encode.update({"exp": expire})
    
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt