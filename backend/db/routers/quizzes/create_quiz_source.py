from typing import Annotated
import uuid
import fitz  # PyMuPDF
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException

from db.dependency import get_current_user, get_db
from db.models import QuizSource, User

DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
db_dep = Annotated[Session, Depends(get_db)]

# Define the router instance
router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)

@router.post("/create/")
async def handle_quiz_upload_and_storage(
    db: db_dep,
    file: UploadFile = File(...),              # This is correctly a file
    user_id: uuid.UUID = Form(...),            # Added Form(...)
    quiz_name: str = Form(None),               # Added Form(...)
    num_questions: int = Form(5)
):
    """
    Step 1: Extract Text from the Uploaded File
    Step 2: Save metadata and text to the DB
    """
    
    # 1. READ & EXTRACT (The Prior Step)
    try:
        # Read file into memory buffer
        file_content = await file.read()
        
        # Open PDF from memory (no disk usage)
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            extracted_text = ""
            for page in doc:
                extracted_text += page.get_text()
        
        if not extracted_text.strip():
            raise ValueError("The PDF appears to be empty or contains only images.")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {str(e)}")

    # 2. SAVE TO DATABASE (Your original logic)
    # We use the filename as a backup if quiz_name isn't provided
    final_title = quiz_name or file.filename
    
    source = QuizSource(
        id=uuid.uuid4(),
        user_id=user_id,
        file_name=final_title,
        extracted_text=extracted_text,
        upload_date=datetime.utcnow()
    )
    
    db.add(source)
    try:
        db.commit()
        db.refresh(source)
    except Exception as e:
        db.rollback()
        raise e
        
    return source