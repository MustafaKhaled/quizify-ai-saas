"""add quota_reset_at to users

Used as a floor when computing per-feature quota windows (Hören, Lesen).
Stripe webhook sets this to now() when a user upgrades to Pro so that
quizzes generated during the trial don't eat into the fresh rolling
7-day Pro allowance.

Revision ID: f8e9d0c1b2a3
Revises: e7d8c9b0a1f2
Create Date: 2026-05-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f8e9d0c1b2a3'
down_revision: Union[str, Sequence[str], None] = 'e7d8c9b0a1f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('quota_reset_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('users', 'quota_reset_at')
