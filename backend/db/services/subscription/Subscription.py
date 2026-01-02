from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.dependency import get_current_user
from db.models import User, Subscription, QuizSource, Quiz, QuizResult
import uuid
from datetime import datetime

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