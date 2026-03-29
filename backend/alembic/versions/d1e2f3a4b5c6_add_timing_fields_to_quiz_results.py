"""add timing fields to quiz_results

Revision ID: d1e2f3a4b5c6
Revises: c9d8e7f6a5b4
Create Date: 2026-03-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, None] = 'c9d8e7f6a5b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('quiz_results', sa.Column('started_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('quiz_results', sa.Column('ended_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('quiz_results', sa.Column('time_remaining_seconds', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('quiz_results', 'time_remaining_seconds')
    op.drop_column('quiz_results', 'ended_at')
    op.drop_column('quiz_results', 'started_at')
