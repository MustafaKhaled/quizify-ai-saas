from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
load_dotenv()
from db.dependency import SECRET_KEY, ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 90   # 3 months
REFRESH_TOKEN_EXPIRE_DAYS = 365              # 1 year
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


def create_refresh_token() -> str:
    """Generates a secure random refresh token (not a JWT — stored hashed in DB)."""
    import secrets
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()


# ── Unsubscribe tokens ────────────────────────────────────────────────────────
# Long-lived JWTs that identify a user via their email so an unauthenticated
# request from a footer link or List-Unsubscribe header can act on the right
# account. Type-tagged so an access token can't be misused as an unsubscribe
# token and vice versa.

UNSUBSCRIBE_TOKEN_EXPIRE_DAYS = 365  # Footer links live in old emails forever — generous expiry.


def make_unsubscribe_token(email: str) -> str:
    """Sign a JWT that proves the bearer is allowed to (un)subscribe `email`.
    Embedded in every email's footer + List-Unsubscribe header."""
    payload = {
        "sub": email,
        "type": "unsubscribe",
        "exp": datetime.now(timezone.utc) + timedelta(days=UNSUBSCRIBE_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_unsubscribe_token(token: str) -> Optional[str]:
    """Return the email encoded in the token, or None if invalid / expired /
    wrong type. Never raises — callers treat None as 'reject'."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    if payload.get("type") != "unsubscribe":
        return None
    return payload.get("sub")