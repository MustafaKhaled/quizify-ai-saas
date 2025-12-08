import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    # This exception should catch the failure before SQLAlchemy does
    raise Exception("DATABASE_URL environment variable is missing!")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()