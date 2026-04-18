from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from db.dependency import get_db, get_current_user, get_token
from db import models
from db.routers.util import build_user_response

import schemas, security
from authlib.integrations.starlette_client import OAuth
from email_service import send_verification_email
import os, secrets as _secrets_mod
from datetime import datetime, timedelta, timezone
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
DASHBOARD_URL = os.getenv("DASHBOARD_URL", FRONTEND_URL)
IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production"
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", None)

# Dependencies
db_dep = Annotated[Session, Depends(get_db)]


ACCESS_TOKEN_MAX_AGE  = 60 * 60 * 24 * 90   # 3 months in seconds
REFRESH_TOKEN_MAX_AGE = 60 * 60 * 24 * 365  # 1 year in seconds


def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
        domain=COOKIE_DOMAIN,
        max_age=ACCESS_TOKEN_MAX_AGE,
        path="/"
    )


def set_refresh_cookie(response: Response, token: str):
    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=IS_PRODUCTION,
        samesite="none" if IS_PRODUCTION else "lax",
        domain=COOKIE_DOMAIN,
        max_age=REFRESH_TOKEN_MAX_AGE,
        path="/auth/refresh"  # only sent to the refresh endpoint
    )


def issue_refresh_token(response: Response, user_id, db: Session):
    raw = security.create_refresh_token()
    token_hash = security.hash_refresh_token(raw)
    expires_at = datetime.now(timezone.utc) + timedelta(days=security.REFRESH_TOKEN_EXPIRE_DAYS)
    db.add(models.RefreshToken(token_hash=token_hash, user_id=user_id, expires_at=expires_at))
    db.commit()
    set_refresh_cookie(response, raw)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.UserCreate, db: db_dep):
    expiration_date = datetime.now(timezone.utc) + timedelta(minutes=3)
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not user_in.password:
        raise HTTPException(
            status_code=400,
            detail="Password is required for standard registration."
        )

    hashed_pwd = security.hash_password(user_in.password[:72])
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        name=user_in.name,
        trial_ends_at=expiration_date,
        is_pro=False,
        is_verified=False,
        is_admin=user_in.is_admin or False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token and send email
    token = _secrets_mod.token_urlsafe(32)
    try:
        db.add(models.EmailVerificationToken(
            user_id=new_user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
        ))
        db.commit()
        print(f"[register] Verification token saved for {new_user.email}")
    except Exception as e:
        print(f"[register] Failed to save verification token: {e}")
        db.rollback()

    try:
        send_verification_email(new_user.email, token)
        print(f"[register] Verification email sent to {new_user.email}")
    except Exception as e:
        print(f"[register] Failed to send verification email: {e}")

    return {
        "message": "Registration successful. Please check your email to verify your account.",
        "requires_verification": True
    }


@router.post("/login", response_model=schemas.AuthenticationSuccessResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: db_dep
):
    from sqlalchemy.orm import joinedload

    user = db.query(models.User).options(joinedload(models.User.subscription)).filter(models.User.email == form_data.username).first()

    if user and not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Looks like you Sign-up with Google, please use Google Login",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in. Check your inbox for the verification link.",
        )

    access_token = security.create_access_token(data={"sub": user.email})
    set_auth_cookie(response, access_token)
    issue_refresh_token(response, user.id, db)

    user_data = build_user_response(user, db)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data
    }


@router.get('/google/login')
async def google_login(request: Request, db: db_dep):
    import secrets
    state = secrets.token_urlsafe(32)
    redirect_uri = f"{BACKEND_URL}/auth/google/callback"

    # Store state in DB so it survives cross-device flows
    db.add(models.OAuthState(state=state, redirect_uri=redirect_uri))
    db.commit()

    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)


@router.get('/google/callback')
async def google_callback(request: Request, db: db_dep):
    from datetime import timedelta
    state = request.query_params.get('state')

    # Validate state against DB
    oauth_state = db.query(models.OAuthState).filter(
        models.OAuthState.state == state
    ).first()

    if not oauth_state:
        raise HTTPException(status_code=400, detail="Invalid or expired OAuth state")

    # Expire states older than 10 minutes
    age = datetime.now(timezone.utc) - oauth_state.created_at.replace(tzinfo=timezone.utc)
    if age > timedelta(minutes=10):
        db.delete(oauth_state)
        db.commit()
        raise HTTPException(status_code=400, detail="OAuth state expired")

    redirect_uri = oauth_state.redirect_uri
    db.delete(oauth_state)
    db.commit()

    # Exchange code for token manually — bypasses authlib's session-based state check
    # since we already validated state against the DB above
    import httpx
    code = request.query_params.get('code')
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            'https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code',
            }
        )
    token_data = token_response.json()
    if 'error' in token_data:
        raise HTTPException(status_code=400, detail=token_data.get('error_description', 'Token exchange failed'))

    import jwt as pyjwt
    id_token = token_data.get('id_token')
    user_info = pyjwt.decode(id_token, options={"verify_signature": False})

    email = user_info.get('email')
    name = user_info.get('name') or user_info.get('given_name', '')

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        user = models.User(email=email, name=name, is_verified=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if not user.is_verified:
            user.is_verified = True
        if not user.name and name:
            user.name = name
        db.commit()

    my_token = security.create_access_token(data={"sub": email})

    # Use a handoff code so the dashboard can exchange it via a credentialed fetch,
    # which correctly sets the cookie (redirect Set-Cookie is unreliable cross-port)
    import secrets as _secrets
    code = _secrets.token_urlsafe(32)
    db.add(models.HandoffCode(code=code, token=my_token))
    db.commit()

    return RedirectResponse(url=f"{DASHBOARD_URL}?code={code}")


@router.get("/verify-email")
async def verify_email(token: str, response: Response, db: db_dep):
    """Verify user email via the token sent in the activation link."""
    record = db.query(models.EmailVerificationToken).filter(
        models.EmailVerificationToken.token == token
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid verification link")

    if record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="Verification link has expired. Please request a new one.")

    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.delete(record)
    db.commit()

    # Auto-login after verification
    access_token = security.create_access_token(data={"sub": user.email})
    set_auth_cookie(response, access_token)
    issue_refresh_token(response, user.id, db)

    return RedirectResponse(url=f"{DASHBOARD_URL}/dashboard?verified=true", status_code=302)


@router.get("/verify", response_model=schemas.UserAdminResponse)
async def verify_token(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    return current_user


@router.post("/resend-verification")
async def resend_verification(payload: dict, db: db_dep):
    """Resend verification email to a user who hasn't verified yet."""
    email = (payload or {}).get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # Don't reveal whether the email exists
        return {"message": "If that email is registered, a verification link has been sent."}

    if user.is_verified:
        return {"message": "Email is already verified. You can log in."}

    # Delete old tokens for this user
    db.query(models.EmailVerificationToken).filter(
        models.EmailVerificationToken.user_id == user.id
    ).delete()

    token = _secrets_mod.token_urlsafe(32)
    db.add(models.EmailVerificationToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    ))
    db.commit()

    try:
        send_verification_email(user.email, token)
    except Exception as e:
        print(f"Failed to resend verification email: {e}")

    return {"message": "If that email is registered, a verification link has been sent."}


@router.post("/exchange")
def exchange_handoff_code(payload: dict, response: Response, db: Session = Depends(get_db)):
    """Exchange a one-time handoff code for an auth cookie. Used after Google OAuth redirect."""
    from datetime import timedelta
    code = payload.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    record = db.query(models.HandoffCode).filter(
        models.HandoffCode.code == code,
        models.HandoffCode.used == False
    ).first()

    if not record:
        raise HTTPException(status_code=400, detail="Invalid or already used code")

    age = datetime.now(timezone.utc) - record.created_at.replace(tzinfo=timezone.utc)
    if age > timedelta(seconds=60):
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="Code expired")

    token = record.token
    record.used = True
    db.commit()

    # Decode the access token to find the user for refresh token issuance
    import jwt as pyjwt
    payload = pyjwt.decode(token, options={"verify_signature": False})
    email = payload.get("sub")
    user = db.query(models.User).filter(models.User.email == email).first()

    set_auth_cookie(response, token)
    if user:
        issue_refresh_token(response, user.id, db)
    return {"ok": True}


@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    raw_token = request.cookies.get("refresh_token")
    if not raw_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    token_hash = security.hash_refresh_token(raw_token)
    record = db.query(models.RefreshToken).filter(
        models.RefreshToken.token_hash == token_hash,
        models.RefreshToken.revoked == False
    ).first()

    if not record:
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

    if record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = security.create_access_token(data={"sub": user.email})
    set_auth_cookie(response, access_token)
    return {"ok": True}


@router.post("/logout")
def logout(request: Request, response: Response, token: str = Depends(get_token), db: Session = Depends(get_db)):
    # Blacklist access token
    db.add(models.BlacklistedToken(token=token))

    # Revoke refresh token if present
    raw_refresh = request.cookies.get("refresh_token")
    if raw_refresh:
        token_hash = security.hash_refresh_token(raw_refresh)
        record = db.query(models.RefreshToken).filter(
            models.RefreshToken.token_hash == token_hash
        ).first()
        if record:
            record.revoked = True

    db.commit()
    response.delete_cookie(key="auth_token", path="/", domain=COOKIE_DOMAIN)
    response.delete_cookie(key="refresh_token", path="/auth/refresh", domain=COOKIE_DOMAIN)
    return {"message": "Logged out successfully"}
