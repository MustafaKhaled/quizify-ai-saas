#main.py
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated 
from db.dependency import get_db
from db.routers.users.users_router import router as user_router
from db.routers.auth.auth_router import router as auth_router
from db.routers.admin.admin_router import router as admin_router
from db.routers.quizzes.create_quiz_source import router as create_quiz_router
from db.routers.quizzes.quizzes_router import router as quizzes_router

# Define a type alias for cleaner code
# Note: You need to import Session from sqlalchemy.orm



DBSession = Annotated[Session, Depends(get_db)]

# The FastAPI application instance
app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(create_quiz_router)
app.include_router(quizzes_router)


# A GET endpoint for simple health check (no DB access)
@app.get("/")
def read_root():
    return {"message": "AI Quiz Backend Running", "status": "OK"}