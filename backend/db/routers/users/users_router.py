# routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import stripe, os
from dateutil.relativedelta import relativedelta
from db.models import User, Subscription
from schemas import UserAdminResponse, UserResponse, UserUpdate
from db.dependency import get_db, get_current_user
from db.routers.util import build_user_response
from security import hash_password
from pydantic import BaseModel # To define the expected request body


# Define a type alias for cleaner code
DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# Define the router instance
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=UserAdminResponse)
def get_my_profile(current_user: CurrentUser, db: DBSession, sync: bool = Query(False)):
    # Access subscription to trigger lazy load if needed
    _ = current_user.subscription

    # When sync=true, look up the user's subscription on Stripe by email.
    # Used after checkout redirect to avoid racing the async webhook.
    if sync:
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        try:
            # Find the customer by email on Stripe
            customers = stripe.Customer.list(email=current_user.email, limit=1)
            if customers.data:
                customer = customers.data[0]
                # Get their active subscriptions
                subs = stripe.Subscription.list(customer=customer.id, status="active", limit=1)
                if subs.data:
                    sub = subs.data[0]
                    current_user.is_pro = True
                    current_user.stripe_subscription_id = sub.id
                    current_user.stripe_customer_id = customer.id
                    ends_at = (
                        datetime.fromtimestamp(sub["current_period_end"])
                        if sub.get("current_period_end")
                        else datetime.utcnow() + relativedelta(months=1)
                    )
                    sub_record = db.query(Subscription).filter(
                        Subscription.user_id == current_user.id
                    ).first()
                    if sub_record:
                        sub_record.ends_at = ends_at
                        sub_record.status = sub.get("status", "active")
                        sub_record.stripe_customer_id = customer.id
                    else:
                        db.add(Subscription(
                            user_id=current_user.id,
                            stripe_customer_id=customer.id,
                            status=sub.get("status", "active"),
                            ends_at=ends_at,
                            created_at=datetime.utcnow(),
                        ))
                    db.commit()
                    db.refresh(current_user)
        except Exception as e:
            import traceback
            print(f"Stripe sync failed: {e}")
            traceback.print_exc()

    # Build user response with subscription info and counts
    user_data = build_user_response(current_user, db)
    return user_data


@router.patch("/me", response_model=UserResponse)
def update_my_profile(
    user_update: UserUpdate, 
    db: DBSession, 
    current_user: CurrentUser
):
    if user_update.password:
        current_user.hashed_password = hash_password(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user



@router.get("/{email}")
def get_user_by_email_endpoint(email: str, db: DBSession):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



