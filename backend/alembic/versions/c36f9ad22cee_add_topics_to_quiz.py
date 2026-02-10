"""add topics to quiz

Revision ID: c36f9ad22cee
Revises: 0f991b56a029
Create Date: 2026-02-10 02:15:32.785393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c36f9ad22cee'
down_revision: Union[str, Sequence[str], None] = '0f991b56a029'
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
