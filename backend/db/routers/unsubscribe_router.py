"""
Email unsubscribe endpoints — public (no login required), token-authenticated.

The token is a JWT signed with the app's secret key, baked into every email's
footer URL and List-Unsubscribe header. It carries the user's email so we can
flip the gate on the right account without any session.

Endpoints
---------
GET /unsubscribe/info?token=...
    Returns the email + current unsubscribe status. Used by the marketing
    /unsubscribe page to render the confirm UI ("You're unsubscribing X").

POST /unsubscribe?token=...
    Sets users.unsubscribed_at to now. Idempotent. Used by:
      - The marketing-page confirm button.
      - Mailbox providers performing a One-Click POST per RFC 8058
        (List-Unsubscribe-Post: List-Unsubscribe=One-Click).
    Returns 200 with a small JSON body.

POST /unsubscribe/resubscribe?token=...
    Clears users.unsubscribed_at. Lets a user undo the action from the same
    confirmation page after they've unsubscribed.

Transactional emails (verification, password reset) IGNORE this gate —
unsubscribing only suppresses non-essential email (announcements, newsletters,
upcoming digest features).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.dependency import get_db
from db.models import User
from security import verify_unsubscribe_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/unsubscribe", tags=["unsubscribe"])

DBSession = Annotated[Session, Depends(get_db)]


def _resolve_user(token: str, db: Session) -> User:
    """Decode the token and look up the user, or raise 400. The error message
    is intentionally generic — we don't want to leak whether an email exists."""
    email = verify_unsubscribe_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired unsubscribe link.")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired unsubscribe link.")
    return user


@router.get("/info")
async def get_unsubscribe_info(
    db: DBSession,
    token: str = Query(..., description="Unsubscribe JWT from the email footer."),
):
    """Public read of the user's current subscription status. Used by the
    marketing page to show 'You're unsubscribing X@Y' before confirming."""
    user = _resolve_user(token, db)
    return {
        "email": user.email,
        "is_unsubscribed": user.unsubscribed_at is not None,
        "unsubscribed_at": user.unsubscribed_at.isoformat() if user.unsubscribed_at else None,
    }


@router.post("")
async def unsubscribe(
    db: DBSession,
    token: str = Query(..., description="Unsubscribe JWT from the email footer."),
):
    """Mark the user as unsubscribed from non-transactional email. Idempotent:
    re-POSTing on an already-unsubscribed user returns the same 200 without
    overwriting the original timestamp."""
    user = _resolve_user(token, db)
    if user.unsubscribed_at is None:
        user.unsubscribed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.commit()
        logger.info("Unsubscribed user email=%s", user.email)
    return {
        "ok": True,
        "email": user.email,
        "unsubscribed_at": user.unsubscribed_at.isoformat() if user.unsubscribed_at else None,
    }


@router.post("/resubscribe")
async def resubscribe(
    db: DBSession,
    token: str = Query(..., description="Unsubscribe JWT from the email footer."),
):
    """Reverse a previous unsubscribe. Lets the user undo from the same
    confirmation page if they hit the button by mistake."""
    user = _resolve_user(token, db)
    if user.unsubscribed_at is not None:
        user.unsubscribed_at = None
        db.commit()
        logger.info("Resubscribed user email=%s", user.email)
    return {
        "ok": True,
        "email": user.email,
        "is_unsubscribed": False,
    }
