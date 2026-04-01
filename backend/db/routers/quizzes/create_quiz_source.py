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

from db.routers.subscription.subscription_router import verify_pro_access
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
    # _ = Depends(verify_pro_access),  # Temporarily disabled for testing
    file: Optional[UploadFile] = File(None),
    source_id: Optional[uuid.UUID] = Form(None),
    subject_id: Optional[uuid.UUID] = Form(None),
    source_name: Optional[str] = Form(None),
    quiz_type: Optional[str] = Form(None),
    quiz_name: str | None = Form(None),
    start_page: Optional[int] | None = Form(None),
    end_page: Optional[int] | None = Form(None),
    num_questions: int = Form(5),
    time_limit: int | None = Form(None)
):
    quiz_type: str = quiz_type or "single_choice"
    extracted_text = ""
    source_to_use_id = None
    file_display_name = ""

    # Build the question format example based on quiz type
    if quiz_type == "multiple_select":
        question_format = """{
      "question_text": "Question here",
      "topic": "topic1",
      "options": ["A", "B", "C", "D"],
      "correct_option_indices": [0, 2],
      "explanation": "Why"
    }"""
        type_instruction = "Each question must have exactly 4 options and 'correct_option_indices' as a list of integers."
    elif quiz_type == "true_or_false":
        question_format = """{
      "question_text": "A factual statement about the material (evaluatable as true or false)",
      "topic": "topic1",
      "options": ["True", "False"],
      "correct_option_index": 0,
      "explanation": "Why this statement is true or false"
    }"""
        type_instruction = "IMPORTANT: options MUST be exactly [\"True\", \"False\"]. Do NOT use A/B/C/D. correct_option_index is 0 for True, 1 for False. You MUST generate EXACTLY {num_questions} statements — create additional ones from the material if needed.".format(num_questions=num_questions)
    else:  # single_choice
        question_format = """{
      "question_text": "Question here",
      "topic": "topic1",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "explanation": "Why"
    }"""
        type_instruction = "Each question must have exactly 4 options and 'correct_option_index' as a single integer."

    # 1. BRANCHING LOGIC: EXISTING SOURCE VS NEW UPLOAD
    source_obj = None  # Holds reference to source record for topic persistence
    if source_id:
        # Security: Filter by both ID and currentUser.id
        source_obj = db.query(QuizSource).filter(
            QuizSource.id == source_id,
            QuizSource.user_id == currentUser.id
        ).first()

        if not source_obj:
            raise HTTPException(404, "Source not found or unauthorized access")

        extracted_text = source_obj.extracted_text
        source_to_use_id = source_obj.id
        file_display_name = source_obj.file_name

    elif file:
        try:
            file_content = await file.read()
            extracted_text = ""
        
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                total_pages = len(doc)
                
                # 1. Set Defaults for optional ranges
                s = (start_page if start_page is not None else 1)
                e = (end_page if end_page is not None else total_pages)
                
                # 2. Basic Validation
                if s < 1 or e > total_pages or s > e:
                    raise HTTPException(400, f"Invalid page range. PDF has {total_pages} pages.")

                # 3. Targeted Extraction (PyMuPDF uses 0-based indexing)
                for page_num in range(s - 1, e):
                    page = doc.load_page(page_num)
                    extracted_text += page.get_text()

            extracted_text = compress_text(extracted_text)
            if len(extracted_text) < 200:
                raise HTTPException(400, "The selected page range contains no selectable text.")
                # Save brand new source only if file is provided
            new_source = QuizSource(
                id=uuid.uuid4(),
                user_id=currentUser.id,
                subject_id=subject_id,
                name=source_name.strip() if source_name else None,
                file_name=file.filename,
                extracted_text=extracted_text,
                upload_date=datetime.utcnow()
            )
            db.add(new_source)
            db.flush()  # Secure the ID for the Quiz foreign key
            source_obj = new_source  # Track for topic persistence
            source_to_use_id = new_source.id
            file_display_name = file.filename
        except Exception as e:
            raise HTTPException(400, f"File processing error: {e}")
    else:
        raise HTTPException(400, "Please provide either a PDF file or a valid source_id")

    # 2. AI GENERATION
    # Compress text for the prompt (cap tokens, normalize whitespace)
    prompt_text = compress_text(extracted_text)
    if len(prompt_text) < 200:
        raise HTTPException(400, "Not enough text content to generate a quiz.")

    # Use stored topics if the source already has them — ensures consistency across quizzes
    existing_topics = source_obj.topics.get("topics", []) if (source_obj and source_obj.topics) else []
    existing_subject = source_obj.topics.get("primary_subject", "") if (source_obj and source_obj.topics) else ""

    if existing_topics:
        topics_instruction = f"""The topics for this source have already been defined as: {existing_topics}.
You MUST use ONLY these topics — do not invent new ones.
Set "primary_subject" to "{existing_subject}" and "topics" to {existing_topics}."""
    else:
        topics_instruction = """STEP 1: Analyze the provided text and identify:
- The primary subject (e.g., "Biology", "Mathematics", "History")
- 3-5 main topics covered in the text (e.g., "Cell Structure", "Photosynthesis")"""

    try:
        prompt = f"""
Return ONLY valid JSON. Do NOT use markdown or conversational text.

{topics_instruction}

Generate EXACTLY {num_questions} questions of type '{quiz_type}'.
- {type_instruction}
- Each question MUST have a "topic" field set to one of the defined topics.
- Distribute questions evenly across topics.

CRITICAL: You must generate the quiz in the SAME LANGUAGE as the provided text.

Each question follows this structure:
{question_format}

Return this JSON — the "questions" array MUST have EXACTLY {num_questions} objects, no more, no less:
{{
  "primary_subject": "...",
  "topics": ["topic1", "topic2"],
  "questions": [ /* {num_questions} question objects here */ ]
}}

Text to analyze:
---
{prompt_text}
---
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"thinking_config": {"thinking_budget": 0}},
        )

        # 3. PARSE AI OUTPUT (Using your helper function)
        quiz_content = extract_json_from_llm(response.text)

        # 4. ENFORCE QUESTION COUNT
        questions = quiz_content.get("questions", [])
        if len(questions) > num_questions:
            quiz_content["questions"] = questions[:num_questions]
        elif len(questions) < num_questions:
            raise ValueError(f"AI returned {len(questions)} questions instead of {num_questions}. Try again.")

        # 5. CREATE & SAVE QUIZ
        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=currentUser.id,
            source_id=source_to_use_id,
            # subject_id intentionally NOT set here — source-level quizzes inherit
            # subject context via QuizSource.subject_id, not via Quiz.subject_id.
            # Setting both causes duplicates in list_subject_quizzes.
            quiz_type=quiz_type,
            title=quiz_name or quiz_content.get("quiz_title", file_display_name),
            num_questions=len(quiz_content.get("questions", [])),
            time_limit=time_limit,
            content=quiz_content,
            topics={
                "primary_subject": quiz_content.get("primary_subject", "Unknown"),
                "topics": quiz_content.get("topics", [])
            },
            generation_date=datetime.utcnow()
        )

        db.add(new_quiz)

        # Persist topics to source if not set yet (first quiz = source of truth for topics)
        if source_obj and not source_obj.topics:
            source_obj.topics = {
                "primary_subject": quiz_content.get("primary_subject", "Unknown"),
                "topics": quiz_content.get("topics", []),
            }

        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error generating or saving quiz: {str(e)}")

@router.post("/create-focused", response_model=QuizResponse)
async def create_focused_quiz(
    db: db_dep,
    currentUser: CurrentUser,
    source_id: uuid.UUID = Form(...),
    focus_topics: str = Form(...),  # Comma-separated list
    quiz_type: Optional[str] = Form("single_choice"),
    quiz_name: str | None = Form(None),
    num_questions: int = Form(10),
    time_limit: int | None = Form(None)
):
    """Generate a quiz focused on specific topics from an existing source"""

    # Get the source
    source = db.query(QuizSource).filter(
        QuizSource.id == source_id,
        QuizSource.user_id == currentUser.id
    ).first()

    if not source:
        raise HTTPException(404, "Source not found")

    # Parse focus topics
    topics_list = [t.strip() for t in focus_topics.split(",")]

    # Build format based on quiz type
    if quiz_type == "multiple_select":
        focused_question_format = """{
      "question_text": "Question here",
      "topic": "one of the focus topics",
      "options": ["A", "B", "C", "D"],
      "correct_option_indices": [0, 2],
      "explanation": "Why"
    }"""
        focused_type_instruction = "Each question must have exactly 4 options and 'correct_option_indices' as a list of integers."
    elif quiz_type == "true_or_false":
        focused_question_format = """{
      "question_text": "A factual statement about the topic (evaluatable as true or false)",
      "topic": "one of the focus topics",
      "options": ["True", "False"],
      "correct_option_index": 0,
      "explanation": "Why this statement is true or false"
    }"""
        focused_type_instruction = f"IMPORTANT: options MUST be exactly [\"True\", \"False\"]. Do NOT use A/B/C/D. correct_option_index is 0 for True, 1 for False. You MUST generate EXACTLY {num_questions} statements."
    else:
        focused_question_format = """{
      "question_text": "Question here",
      "topic": "one of the focus topics",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "explanation": "Why"
    }"""
        focused_type_instruction = "Each question must have exactly 4 options and 'correct_option_index' as a single integer."

    # Compress source text for prompt
    focused_prompt_text = compress_text(source.extracted_text or "")
    if len(focused_prompt_text) < 200:
        raise HTTPException(400, "Not enough text content in this source to generate a quiz.")

    # Enhanced prompt for focused quiz
    prompt = f"""
Return ONLY valid JSON. Do NOT use markdown or conversational text.

Generate EXACTLY {num_questions} questions of type '{quiz_type}' focused ONLY on these topics: {', '.join(topics_list)}

- {focused_type_instruction}
- Each question MUST have a "topic" field set to one of the listed topics.
- Distribute evenly across topics.

CRITICAL: Generate the quiz in the SAME LANGUAGE as the provided text.

Each question follows this structure:
{focused_question_format}

Return this JSON — the "questions" array MUST have EXACTLY {num_questions} objects, no more, no less:
{{
  "primary_subject": "...",
  "topics": {topics_list},
  "questions": [ /* {num_questions} question objects here */ ]
}}

Text to use:
---
{focused_prompt_text}
---
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"thinking_config": {"thinking_budget": 0}},
        )

        quiz_content = extract_json_from_llm(response.text)

        questions = quiz_content.get("questions", [])
        if len(questions) > num_questions:
            quiz_content["questions"] = questions[:num_questions]
        elif len(questions) < num_questions:
            raise ValueError(f"AI returned {len(questions)} questions instead of {num_questions}. Try again.")

        new_quiz = Quiz(
            id=uuid.uuid4(),
            user_id=currentUser.id,
            source_id=source_id,
            quiz_type=quiz_type,
            title=quiz_name or f"Focused Quiz - {', '.join(topics_list[:2])}",
            num_questions=len(quiz_content.get("questions", [])),
            time_limit=time_limit,
            content=quiz_content,
            topics={
                "primary_subject": quiz_content.get("primary_subject", "Unknown"),
                "topics": quiz_content.get("topics", [])
            },
            generation_date=datetime.utcnow()
        )

        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error generating focused quiz: {str(e)}")



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


def compress_text(text: str, max_chars: int = 40_000) -> str:
    """Normalize whitespace and cap text length to reduce token usage."""
    # Collapse runs of whitespace/newlines to at most 2 newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars]
    return text


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