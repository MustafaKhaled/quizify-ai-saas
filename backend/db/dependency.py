from typing import Generator
from sqlalchemy.orm import Session
from .database import SessionLocal # Import the SessionLocal class

# This is the function that will be injected into your routes
def get_db() -> Generator[Session, None, None]:
    """
    Provides a new SQLAlchemy session for each request,
    and ensures it's closed afterwards.
    """
    db = SessionLocal()
    try:
        # 'yield' makes this function a generator dependency
        yield db 
    except Exception:
        # Rollback the session if any unhandled error occurs
        db.rollback()
        raise
    finally:
        # Always close the session after the request is complete
        db.close()