from typing import Annotated, Optional
import uuid
import streamlit as st
import fitz  # PyMuPDF
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from dotenv import load_dotenv
from google import genai

from schemas import QuizResponse
1
import os
import json
# --- 1. CONFIGURATION AND API SETUP (from Step 2) ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="PDF to Quiz Builder", layout="wide")

try:
    # Initialize the Gemini Client
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🚨 Error: Gemini API client could not be initialized. Please check your GEMINI_API_KEY in the .env file.")
    st.stop()
from db.dependency import get_current_user, get_db
from db.models import Quiz, QuizSource, User

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
db_dep = Annotated[Session, Depends(get_db)]

# Define the router instance
router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

@router.post("/create", response_model=QuizResponse)
async def create_quiz_from_file(
    db: db_dep,
    currentUser: CurrentUser,
    file: UploadFile = File(...),
    quiz_name: str | None = Form(None),
    num_questions: int = Form(5),
    time_limit: int | None = Form(None)
):
    # 1. READ PDF
    try:
        file_content = await file.read()
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            extracted_text = "".join(page.get_text() for page in doc)

        if not extracted_text.strip():
            raise HTTPException(400, "PDF contains no selectable text")
    except Exception as e:
        raise HTTPException(400, f"File processing error: {e}")

    try:
        # 2. VERIFY USER EXISTS
        user = db.query(User).filter(User.id == currentUser.id).first()
        if not user:
            raise HTTPException(404, "User not found")

        # 3. SAVE SOURCE
        source = QuizSource(
            id=uuid.uuid4(),
            user_id=currentUser.id,
            file_name=file.filename,
            extracted_text=extracted_text,
            upload_date=datetime.utcnow()
        )
        db.add(source)
        db.flush()

        # 4. GEMINI PROMPT
        prompt = f"""
Return ONLY valid JSON. Do NOT use markdown.

{{
  "quiz_title": "Short title",
  "questions": [
    {{
      "question_text": "Question?",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "explanation": "Why"
    }}
  ]
}}

Generate exactly {num_questions} questions from the text below:

---
{extracted_text}
---
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # 5. PARSE AI OUTPUT
        quiz_content = extract_json_from_llm(response.text)

        # 6. CREATE QUIZ
        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=currentUser.id,
            source_id=source.id,
            title=quiz_name or quiz_content["quiz_title"],
            num_questions=len(quiz_content["questions"]),
            time_limit=time_limit,
            content=quiz_content,
            generation_date=datetime.utcnow()
        )

        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)

        return new_quiz

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Database error: {e}")


def extract_json_from_llm(text: str) -> dict:
    text = text.strip()

    # Remove ```json fences
    if text.startswith("```"):
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    return json.loads(text)