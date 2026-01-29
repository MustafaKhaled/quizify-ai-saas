from datetime import datetime, timedelta, timezone
from db.models import User

def get_subscription_status(user: User) -> dict:
    now = datetime.now(timezone.utc) - timedelta(hours=1)  # Small buffer to avoid edge cases
    
    # 2. Force user.created_at to UTC
    # If it's already aware, convert it. If naive, assume UTC.
    if user.created_at.tzinfo is None:
        created_at_utc = user.created_at.replace(tzinfo=timezone.utc)
    else:
        created_at_utc = user.created_at.astimezone(timezone.utc)
        
    trial_limit = created_at_utc + timedelta(minutes=3)

    print("Current time (UTC):", now)   
    print("User created at (UTC):", created_at_utc)
    print("Trial ends at (UTC):", trial_limit)

    # 2. Logic Branch 1: User is currently PRO (Paid)
    if user.is_pro:
        # Check if the subscription record exists to get the specific type
        sub_record = user.subscription
        ends_at = sub_record.ends_at if sub_record else None
        
        # Determine if monthly or yearly
        is_yearly = sub_record and "year" in (sub_record.status or "").lower()
        
        # Check if the paid time has actually run out
        if ends_at and now > ends_at:
            status = "expired_yearly" if is_yearly else "expired_monthly"
            is_eligible = False
            label = "Subscription Expired"
        else:
            status = "active_yearly" if is_yearly else "active_monthly"
            is_eligible = True
            label = "Pro Yearly" if is_yearly else "Pro Monthly"

        return {
            "status": status,
            "label": label,
            "is_eligible": is_eligible,
            "ends_at": ends_at,
            "trial_ends": trial_limit
        }

    # 3. Logic Branch 2: User is NOT Pro (Check Trial)
    if now < trial_limit:
        diff = trial_limit - now
        total_seconds = int(diff.total_seconds())
        
        return {
            "status": "trial_active",
            "label": f"Trial ({total_seconds // 60}m {total_seconds % 60}s left)",
            "is_eligible": True,
            "ends_at": None,      # No subscription end date yet
            "trial_ends": trial_limit
        }

    # 4. Logic Branch 3: Trial has ended, never paid
    return {
        "status": "trial_expired",
        "label": "Trial Expired",
        "is_eligible": False,
        "ends_at": None,
        "trial_ends": trial_limit
    }

def build_user_response(user: User, db_session=None) -> dict:
    # Get the detailed subscription status
    sub_data = get_subscription_status(user)
    
    quizzes_count = 0
    sources_count = 0
    if db_session:
        from db.models import Quiz, QuizSource
        quizzes_count = db_session.query(Quiz).filter(Quiz.user_id == user.id).count()
        sources_count = db_session.query(QuizSource).filter(QuizSource.user_id == user.id).count()
    
    # Create subscription info object with trial_ends_at and status_label moved inside
    subscription_info = {
        "status": sub_data["status"],
        "label": sub_data["label"],
        "is_eligible": sub_data["is_eligible"],
        "ends_at": sub_data.get("ends_at"),
        "trial_ends_at": sub_data.get("trial_ends"),
        "status_label": sub_data["label"]  # Use label as status_label
    }
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at,
        "is_admin": user.is_admin,
        "is_pro": user.is_pro,
        "quizzes_count": quizzes_count,
        "sources_count": sources_count,
        "subscription": subscription_info
    }