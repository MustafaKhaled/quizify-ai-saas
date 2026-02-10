"""ensure topics column exists

Revision ID: f1000bf5fa50
Revises: c36f9ad22cee
Create Date: 2026-02-10 03:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = 'f1000bf5fa50'
down_revision: Union[str, Sequence[str], None] = 'c36f9ad22cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely add topics column only if it doesn't exist yet
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'quizzes' AND column_name = 'topics'
            ) THEN
                ALTER TABLE quizzes ADD COLUMN topics JSONB;
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.drop_column('quizzes', 'topics')
