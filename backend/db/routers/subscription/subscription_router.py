from typing import Annotated
import os
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
import stripe
from schemas import CheckoutRequest
from db.dependency import get_current_user, get_db
from db.models import User, Subscription, QuizSource, Quiz, QuizResult
import uuid
from datetime import datetime

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


@router.post("/create-checkout-session")
async def create_checkout(
    payload: CheckoutRequest,
    db: db_dep, 
    current_user: User = Depends(get_current_user)
):
    print(payload.price_id)
    try:
        # Create the session
        session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{'price': payload.price_id, 'quantity': 1}],
            mode='subscription',
            # Stripe replaces {CHECKOUT_SESSION_ID} automatically
            success_url="https://exam-sim.com/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://exam-sim.com/pricing",
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
        print(f"💰 Payment succeeded for {session.customer_details.email}")
        # TODO: Update your database here!

    return {"status": "success"}