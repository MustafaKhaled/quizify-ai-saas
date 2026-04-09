from typing import Annotated
import os
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
import stripe
from db.database import SessionLocal
from schemas import CheckoutRequest
from db.dependency import get_current_user, get_db
from db.models import User, Subscription
from datetime import datetime
from dateutil.relativedelta import relativedelta

router = APIRouter(
    prefix="/subscription",
    tags=["subscription"]
)

db_dep = Annotated[Session, Depends(get_db)]

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


def verify_pro_access(current_user: User = Depends(get_current_user)):
    now = datetime.utcnow()
    
    # Priority 1: Check if they are a paid subscriber
    if current_user.is_pro:
        return True
        
    # Priority 2: Check if trial is still active
    if current_user.trial_ends_at and now < current_user.trial_ends_at:
        return True
        
    # If both fail, raise an error
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Pro access required. Your trial has expired."
    )


DASHBOARD_URL = os.getenv("DASHBOARD_URL", "http://localhost:3000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3001")


@router.post("/create-checkout-session")
async def create_checkout(
    payload: CheckoutRequest,
    _: db_dep,
    current_user: User = Depends(get_current_user)
):
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    try:
        session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{'price': payload.price_id, 'quantity': 1}],
            mode='subscription',
            success_url=f"{DASHBOARD_URL}/dashboard?subscription=success&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/pricing",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/verify-session")
async def verify_session(
    payload: dict,
    db: db_dep,
    current_user: User = Depends(get_current_user),
):
    """Synchronously verify a Stripe Checkout Session after redirect.

    Avoids race with the async webhook so the UI can immediately reflect
    Pro status without polling.
    """
    session_id = (payload or {}).get("session_id")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid session: {e}")

    # Make sure this session actually belongs to the caller.
    session_email = (session.get("customer_details") or {}).get("email")
    if session_email and session_email.lower() != (current_user.email or "").lower():
        raise HTTPException(status_code=403, detail="Session does not belong to current user")

    if session.get("payment_status") != "paid":
        return {"is_pro": bool(current_user.is_pro), "status": session.get("payment_status")}

    stripe_sub_id = session.get("subscription")
    stripe_customer_id = session.get("customer")

    current_user.is_pro = True
    if stripe_sub_id:
        current_user.stripe_subscription_id = stripe_sub_id
    if stripe_customer_id:
        current_user.stripe_customer_id = stripe_customer_id

    ends_at = None
    try:
        if stripe_sub_id:
            sub = stripe.Subscription.retrieve(stripe_sub_id)
            if sub.get("current_period_end"):
                ends_at = datetime.fromtimestamp(sub["current_period_end"])
    except Exception as e:
        print(f"verify_session: failed to fetch subscription: {e}")
    if not ends_at:
        ends_at = datetime.utcnow() + relativedelta(months=1)

    sub_record = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if sub_record:
        sub_record.ends_at = ends_at
        sub_record.status = "active"
        if stripe_customer_id:
            sub_record.stripe_customer_id = stripe_customer_id
    else:
        db.add(Subscription(
            user_id=current_user.id,
            stripe_customer_id=stripe_customer_id,
            status="active",
            ends_at=ends_at,
            created_at=datetime.utcnow(),
        ))

    db.commit()
    return {"is_pro": True, "ends_at": ends_at.isoformat()}


@router.post("/stripe-webhook")
async def handle_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    
    try:
        # Verify the event came from Stripe
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return {"error": str(e)}

    # Check for successful payments
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"Payment succeeded for {session.customer_details.email}")
        
        # Get user identifier (using email or metadata)
        customer_email = session.get("customer_details", {}).get("email")
        stripe_sub_id = session.get("subscription")  # e.g., sub_1Qjs...
        stripe_customer_id = session.get("customer")  # e.g., cus_Pjs...

        # Open a database session
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == customer_email).first()
            
            if user:
                # Update User Status
                user.is_pro = True
                user.stripe_subscription_id = stripe_sub_id
                user.stripe_customer_id = stripe_customer_id
                
                # Get subscription details from Stripe to calculate end date
                try:
                    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
                    subscription = stripe.Subscription.retrieve(stripe_sub_id)
                    
                    # Calculate ends_at: current time + subscription period (typically 1 month)
                    # Use the current_period_end from Stripe if available
                    if subscription.get('current_period_end'):
                        ends_at = datetime.fromtimestamp(subscription['current_period_end'])
                    else:
                        # Fallback: add 1 month from now
                        ends_at = datetime.utcnow() + relativedelta(months=1)
                    
                    # Update or create Subscription record
                    subscription_record = db.query(Subscription).filter(
                        Subscription.user_id == user.id
                    ).first()
                    
                    if subscription_record:
                        subscription_record.ends_at = ends_at
                        subscription_record.status = subscription.get('status', 'active')
                        subscription_record.stripe_customer_id = stripe_customer_id
                    else:
                        # Create new subscription record if it doesn't exist
                        subscription_record = Subscription(
                            user_id=user.id,
                            stripe_customer_id=stripe_customer_id,
                            status=subscription.get('status', 'active'),
                            ends_at=ends_at,
                            created_at=datetime.utcnow()
                        )
                        db.add(subscription_record)
                    
                except Exception as stripe_error:
                    print(f"Error fetching Stripe subscription: {stripe_error}")
                
                db.commit()
                print(f"Database Updated: {customer_email} is now a Pro member. Subscription ends at {ends_at}.")
            else:
                print(f"Webhook Error: User with email {customer_email} not found.")

    return {"status": "success"}