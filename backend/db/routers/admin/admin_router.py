from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from schemas import UserAdminResponse
from db.dependency import get_current_admin, get_db
from db import models
router = APIRouter(
    prefix="/admin",
    tags=["Adinmistration"]
)

db_dep = Annotated[Session, Depends(get_db)]
DBSession = Annotated[Session, Depends(get_db)]
CurrentAdmin = Annotated[models.User, Depends(get_current_admin)]

@router.get("/allusers", response_model=list[UserAdminResponse])
async def get_all_users(
    db: db_dep,
    _: CurrentAdmin
):
    users = db.query(models.User).all()
    return users


@router.delete("/user/email/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_email(
    email: str,
    db: db_dep,
    _: CurrentAdmin
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()



