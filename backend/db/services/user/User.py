#service/user/User.py
from sqlalchemy.orm import Session
from db.models import User
import uuid
from datetime import datetime


def create_user(db: Session, email: str, hashed_password: str, is_admin: bool = False) -> User:
    db_user = User(id=uuid.uuid4(), email=email, hashed_password=hashed_password, is_admin=is_admin, created_at=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()