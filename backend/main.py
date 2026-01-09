#main.py
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated 
from db.dependency import get_db
from db.routers.users.users_router import router as user_router
from db.routers.auth.auth_router import router as auth_router
from db.routers.admin.admin_router import router as admin_router
from db.routers.quizzes.create_quiz_source import router as create_quiz_router
from db.routers.quizzes.quizzes_router import router as quizzes_router
from db.routers.subscription.subscription_router import router as subscription_router
from starlette.middleware.sessions import SessionMiddleware


DBSession = Annotated[Session, Depends(get_db)]

# The FastAPI application instance
app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(create_quiz_router)
app.include_router(quizzes_router)
app.include_router(subscription_router)


frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
secret_key = os.getenv("CLIENT_SECRET")
session_secret_key=os.getenv("SESSION_SECRET_KEY")

app.add_middleware(SessionMiddleware, secret_key=session_secret_key)


# A GET endpoint for simple health check (no DB access)
@app.get("/")
def read_root():
    return {"message": "AI Quiz Backend Running", "status": "OK"}

origins = [
    frontend_url,
    backend_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)