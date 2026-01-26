from datetime import datetime, timezone

from db.models import User

def get_detailed_status(user):
    now = datetime.now(timezone.utc)
    
    # Logic for Pro
    if user.is_pro and user.subscription_end:
        return {
            "status": "active",
            "label": "Pro Plan",
            "is_eligible": True,
            "ends_at": user.subscription_end  # We call it ends_at for the schema
        }

    # Logic for Trial
    if user.trial_ends_at and user.trial_ends_at > now:
        return {
            "status": "trial",
            "label": "Trial Active",
            "is_eligible": True,
            "ends_at": user.trial_ends_at  # Map trial_ends_at to ends_at
        }

    return {
        "status": "expired",
        "label": "Expired",
        "is_eligible": False,
        "ends_at": None
    }