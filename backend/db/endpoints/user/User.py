from sqlalchemy.orm import Session
from models import User
import uuid
from datetime import datetime


def create_user(db: Session, email: str, hashed_password: str) -> User:
    db_user = User(id=uuid.uuid4(), email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()