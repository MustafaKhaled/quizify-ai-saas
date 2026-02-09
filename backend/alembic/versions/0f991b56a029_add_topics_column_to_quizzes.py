"""add_topics_column_to_quizzes

Revision ID: 0f991b56a029
Revises: 482579673e3a
Create Date: 2026-02-10 00:02:49.793992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '0f991b56a029'
down_revision: Union[str, Sequence[str], None] = '482579673e3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add topics column to quizzes table
    op.add_column('quizzes', sa.Column('topics', JSONB, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove topics column from quizzes table
    op.drop_column('quizzes', 'topics')
