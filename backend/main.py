from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated 
from db.dependency import get_db

# Define a type alias for cleaner code
# Note: You need to import Session from sqlalchemy.orm
DBSession = Annotated[Session, Depends(get_db)]

# The FastAPI application instance
app = FastAPI()

# A GET endpoint for simple health check (no DB access)
@app.get("/")
def read_root():
    return {"message": "AI Quiz Backend Running", "status": "OK"}


# A GET endpoint for database health check
@app.get("/health_check")
def db_health_check(db: DBSession):
    # This proves the session is working by executing a trivial query
    try:
        # Use db.execute(text("SELECT 1")) for modern SQLAlchemy (requires import)
        # For simplicity and backward compatibility, we'll keep the string execution for now
        db.execute("SELECT 1") 
        return {"status": "Database connection OK"}
    except Exception as e:
        # Raise an HTTP 500 if the database connection fails
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

# ... other routes ...