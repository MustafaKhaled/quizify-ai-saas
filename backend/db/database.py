from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password123"
POSTGRES_DB = "mydb"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

DATABASE_URL = f"postgresql+psycopg2://mustafa@localhost:5432/mydb"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()