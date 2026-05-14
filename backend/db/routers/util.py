from datetime import datetime, timedelta, timezone
from db.models import User
from db.routers.subscription.subscription_router import TRIAL_QUIZ_LIMIT

def get_subscription_status(user: User) -> dict:
    now = datetime.now(timezone.utc)

    # The trial deadline is whatever `trial_ends_at` was set to at signup
    # (auth_router writes it as `now + TRIAL_DURATION_DAYS`). Fall back to
    # `created_at + TRIAL_DURATION_DAYS` for older rows where trial_ends_at
    # was never populated (e.g. pre-OAuth-fix accounts).
    TRIAL_FALLBACK_DAYS = 7
    if user.trial_ends_at is not None:
        trial_limit = user.trial_ends_at
    else:
        trial_limit = user.created_at + timedelta(days=TRIAL_FALLBACK_DAYS)

    # Normalize both sides to UTC-aware so the subtraction is meaningful.
    if trial_limit.tzinfo is None:
        trial_limit = trial_limit.replace(tzinfo=timezone.utc)

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
        import math
        diff = trial_limit - now
        total_seconds = int(diff.total_seconds())
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        if total_seconds >= 86400:
            # Ceiling on days so a fresh 7-day signup reads "7 days left"
            # instead of "6 days left" due to microsecond rounding between
            # writing trial_ends_at at signup and reading it back.
            days_display = math.ceil(total_seconds / 86400)
            label_remainder = f"{days_display} day{'s' if days_display != 1 else ''} left"
        elif total_seconds >= 3600:
            label_remainder = f"{hours}h left"
        else:
            label_remainder = f"{max(minutes, 1)}m left"

        return {
            "status": "trial_active",
            "label": f"Trial ({label_remainder})",
            "is_eligible": True,
            "ends_at": None,
            "trial_ends": trial_limit,
            "trial_quiz_limit": TRIAL_QUIZ_LIMIT
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
        "status_label": sub_data["label"],
        "trial_quiz_limit": sub_data.get("trial_quiz_limit"),
    }
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at,
        "is_admin": user.is_admin,
        "is_pro": user.is_pro,
        "is_verified": user.is_verified,
        "has_password": bool(user.hashed_password),
        "quizzes_count": quizzes_count,
        "sources_count": sources_count,
        "subscription": subscription_info
    }