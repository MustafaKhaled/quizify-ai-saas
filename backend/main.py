#main.py
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Annotated
from db.dependency import get_db
from db.routers.users.users_router import router as user_router
from db.routers.auth.auth_router import router as auth_router
from db.routers.admin.admin_router import router as admin_router
from db.routers.quizzes.create_quiz_source import router as create_quiz_router
from db.routers.quizzes.quizzes_router import router as quizzes_router
from db.routers.subjects.subjects_router import router as subjects_router
from db.routers.subscription.subscription_router import router as subscription_router
from db.routers.predefined.predefined_router import router as predefined_router
from db.routers.predefined.horen_router import router as horen_router
from db.routers.recommendations.recommendations_router import router as recommendations_router
from starlette.middleware.sessions import SessionMiddleware


DBSession = Annotated[Session, Depends(get_db)]

# The FastAPI application instance
app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(create_quiz_router)
app.include_router(quizzes_router)
app.include_router(subjects_router)
app.include_router(subscription_router)
app.include_router(predefined_router)
app.include_router(horen_router)
app.include_router(recommendations_router)

# Serve B1 Hören audio files. New on-demand quizzes write here with UUID
# filenames; the directory is bootstrapped at startup so the StaticFiles
# mount succeeds even before the first generation.
HOREN_AUDIO_DIR = Path(__file__).parent / "uploads" / "horen"
HOREN_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static/horen", StaticFiles(directory=str(HOREN_AUDIO_DIR)), name="horen_audio")


frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
dashboard_url = os.getenv("DASHBOARD_URL", "http://localhost:3001")
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
    dashboard_url,
    backend_url
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)