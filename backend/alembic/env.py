from logging.config import fileConfig
import sys, os
from sqlalchemy import create_engine
from sqlalchemy import pool
from dotenv import load_dotenv

from db.database import Base
# IMPORTANT: You must import the models so they register themselves on Base.metadata
from db.models import User, Subscription, QuizSource, Quiz, QuizResult

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, ".env"))
from alembic import context
from db.database import Base 
import db.models


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = os.environ.get("DATABASE_URL") 
    if not url:
        url = "postgresql://user:pass@host/dbname" 
        
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Use the URL from the environment
    url = os.environ.get("DATABASE_URL")
    
    # Railway/SQLAlchemy 1.4+ fix
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # This ensures Alembic detects changes to column types/lengths
            compare_type=True 
        )

        with context.begin_transaction():
            context.run_migrations()
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()