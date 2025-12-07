from sqlalchemy.orm import Session
from models import User, Subscription, QuizSource, Quiz, QuizResult
import uuid
from datetime import datetime

def create_subscription(db: Session, user_id: uuid.UUID, stripe_customer_id: str, status: str):
    subscription = Subscription(
        id=uuid.uuid4(),
        user_id=user_id,
        stripe_customer_id=stripe_customer_id,
        status=status,
        ends_at=None
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription