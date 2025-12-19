from logging.config import fileConfig
import sys, os
from sqlalchemy import create_engine
from sqlalchemy import pool
from dotenv import load_dotenv



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
    url = os.environ.get("DATABASE_URL")
    print("Using DATABASE_URL:", url)
    if not url:
        raise Exception("DATABASE_URL not set in environment or Railway")

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()