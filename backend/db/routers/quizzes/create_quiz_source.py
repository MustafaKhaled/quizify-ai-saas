import re
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
    file: Optional[UploadFile] = File(None),
    source_id: Optional[uuid.UUID] = Form(None),
    type: Optional[str] = Form("single_choice"),
    quiz_name: str | None = Form(None),
    num_questions: int = Form(5),
    time_limit: int | None = Form(None)
):
    quiz_type: str = type
    extracted_text = ""
    source_to_use_id = None
    file_display_name = ""

    # Inside your endpoint logic
    if quiz_type == "multiple_select": # Checkbox
        format_instruction = """
        "questions": [
            {
            "question_text": "Question here",
            "options": ["A", "B", "C", "D"],
            "correct_option_indices": [0, 2], # Array for multiple correct answers
            "explanation": "Why"
            }
        ]"""
    else: # Standard Multiple Choice
        format_instruction = """
        "questions": [
            {
            "question_text": "Question here",
            "options": ["A", "B", "C", "D"],
            "correct_option_index": 0,
            "explanation": "Why"
            }
        ]"""

    # 1. BRANCHING LOGIC: EXISTING SOURCE VS NEW UPLOAD
    if source_id:
        # Security: Filter by both ID and currentUser.id
        source = db.query(QuizSource).filter(
            QuizSource.id == source_id, 
            QuizSource.user_id == currentUser.id
        ).first()
        
        if not source:
            raise HTTPException(404, "Source not found or unauthorized access")
        
        extracted_text = source.extracted_text
        source_to_use_id = source.id
        file_display_name = source.file_name

    elif file:
        try:
            file_content = await file.read()
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                extracted_text = "".join(page.get_text() for page in doc)

            if not extracted_text.strip():
                raise HTTPException(400, "PDF contains no selectable text")
            
            # Save brand new source only if file is provided
            new_source = QuizSource(
                id=uuid.uuid4(),
                user_id=currentUser.id,
                file_name=file.filename,
                extracted_text=extracted_text,
                upload_date=datetime.utcnow()
            )
            db.add(new_source)
            db.flush() # Secure the ID for the Quiz foreign key
            
            source_to_use_id = new_source.id
            file_display_name = file.filename
        except Exception as e:
            raise HTTPException(400, f"File processing error: {e}")
    else:
        raise HTTPException(400, "Please provide either a PDF file or a valid source_id")

    # 2. AI GENERATION
    try:
        # Prompt includes specific instruction for better results
        prompt = f"""
Return ONLY valid JSON. Do NOT use markdown or conversational text.
Your goal is to generate educational quiz questions based on the provided text.

Generate exactly {num_questions} for the quiz type {quiz_type}, with format {format_instruction} using the text below:
---
{extracted_text}
---
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash", # Use the current stable flash model
            contents=prompt
        )

        # 3. PARSE AI OUTPUT (Using your helper function)
        quiz_content = extract_json_from_llm(response.text)

        # 4. CREATE & SAVE QUIZ
        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=currentUser.id,
            source_id=source_to_use_id,
            quiz_type=quiz_type,
            title=quiz_name or quiz_content.get("quiz_title", file_display_name),
            num_questions=len(quiz_content.get("questions", [])),
            time_limit=time_limit,
            content=quiz_content,
            generation_date=datetime.utcnow()
        )

        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    except Exception as e:
        db.rollback()
        # Logging here would be helpful: logger.error(f"AI/DB Error: {e}")
        raise HTTPException(500, f"Error generating or saving quiz: {str(e)}")

    

@router.get("/sources")
async def get_quiz_sources(
    db: db_dep,
    current_user: CurrentUser,
):
    sources = (
        db.query(QuizSource)
        .filter(QuizSource.user_id == current_user.id)
        .order_by(QuizSource.upload_date.desc())
        .all()
    )
    return sources
    

@router.delete("/sources/{source_id}", status_code=204)
async def delete_quiz_source(
    db: db_dep,
    _: CurrentUser,
    source_id: str,
):
    source = (
        db.query(QuizSource)
        .filter(QuizSource.id == source_id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=404, detail="Quiz Source not found")

    db.delete(source)
    db.commit()
    return {
        "status": "success",
        "message": f"Source {source_id} and all associated quizzes deleted."
    }


def extract_json_from_llm(text: str) -> dict:
    # Use regex for more robust extraction in case Gemini adds text outside fences
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        clean_text = match.group(1)
    else:
        # Fallback to standard cleaning
        clean_text = text.strip()
        if clean_text.startswith("```"):
            clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text)
            clean_text = re.sub(r"\s*```$", "", clean_text)
    
    try:
        return json.loads(clean_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON: {e}")