from datetime import datetime, timezone
from db.models import User

def get_subscription_status(user: User) -> dict:
    """
    Calculate subscription status and info based on user's current state.
    Returns a dict with subscription_status, subscription info, and status_label.
    """
    now = datetime.now(timezone.utc)
    
    # Normalize trial_ends_at to timezone-aware if it exists
    trial_ends = None
    if user.trial_ends_at:
        if user.trial_ends_at.tzinfo is None:
            # Assume UTC if timezone-naive
            trial_ends = user.trial_ends_at.replace(tzinfo=timezone.utc)
        else:
            trial_ends = user.trial_ends_at
    
    # Check if user has an active paid subscription
    if user.is_pro:
        # Try to access subscription relationship (will lazy load if needed)
        try:
            sub = user.subscription if hasattr(user, 'subscription') else None
        except:
            sub = None
            
        if sub:
            sub_ends_at = None
            if sub.ends_at:
                if sub.ends_at.tzinfo is None:
                    sub_ends_at = sub.ends_at.replace(tzinfo=timezone.utc)
                else:
                    sub_ends_at = sub.ends_at
            
            if sub_ends_at and sub_ends_at > now:
                # Determine if monthly or yearly based on subscription status
                status = "active_yearly" if "year" in sub.status.lower() else "active_monthly"
                subscription_status = "active"
                label = f"Pro {'Yearly' if 'year' in sub.status.lower() else 'Monthly'}"
                ends_at = sub_ends_at
            else:
                status = "expired"
                subscription_status = "canceled"
                label = "Expired"
                ends_at = sub_ends_at
        else:
            # User is pro but no subscription record - assume active
            status = "active_monthly"
            subscription_status = "active"
            label = "Pro Active"
            ends_at = None
    else:
        # Check trial status
        if trial_ends and trial_ends > now:
            status = "trial"
            subscription_status = "trial"
            days_left = (trial_ends - now).days
            label = f"Trial ({days_left}d left)" if days_left > 0 else "Trial (Expiring soon)"
            ends_at = trial_ends
        else:
            # No active subscription or trial
            status = "expired"
            subscription_status = "free"
            label = "Free"
            ends_at = None
    
    is_eligible = status in ["trial", "active_monthly", "active_yearly"]
    
    return {
        "subscription_status": subscription_status,
        "subscription": {
            "status": status,
            "label": label,
            "is_eligible": is_eligible,
            "ends_at": ends_at
        },
        "status_label": label
    }

def build_user_response(user: User, db_session=None) -> dict:
    """
    Build a complete user response with subscription info and counts.
    """
    # Get subscription info
    sub_info = get_subscription_status(user)
    
    # Get counts if db_session is provided
    quizzes_count = 0
    sources_count = 0
    if db_session:
        from db.models import Quiz, QuizSource
        quizzes_count = db_session.query(Quiz).filter(Quiz.user_id == user.id).count()
        sources_count = db_session.query(QuizSource).filter(QuizSource.user_id == user.id).count()
    
    # Normalize trial_ends_at to timezone-aware if it exists
    trial_ends_at = None
    if user.trial_ends_at:
        if user.trial_ends_at.tzinfo is None:
            trial_ends_at = user.trial_ends_at.replace(tzinfo=timezone.utc)
        else:
            trial_ends_at = user.trial_ends_at
    
    # Build response
    response = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at,
        "is_admin": user.is_admin,
        "is_pro": user.is_pro,
        "quizzes_count": quizzes_count,
        "sources_count": sources_count,
        "subscription_status": sub_info["subscription_status"],
        "subscription": sub_info["subscription"],
        "status_label": sub_info["status_label"],
        "trial_ends_at": trial_ends_at
    }
    
    return response
