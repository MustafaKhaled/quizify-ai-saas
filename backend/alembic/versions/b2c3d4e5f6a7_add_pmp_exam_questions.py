"""add pmp_exam_questions table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-04-23

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'pmp_exam_questions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('content_hash', sa.String(length=64), nullable=False),
        sa.Column('chapter_slug', sa.String(length=64), nullable=False),
        sa.Column('stem', sa.String(), nullable=False),
        sa.Column('quiz_type', sa.String(length=32), nullable=False, server_default='single_choice'),
        sa.Column('options', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('correct_index', sa.Integer(), nullable=True),
        sa.Column('correct_option_indices', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('explanation', sa.String(), nullable=False),
        sa.Column('source', sa.String(length=255), nullable=False),
        sa.Column('difficulty', sa.String(length=16), nullable=False, server_default='medium'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('content_hash', name='uq_pmp_exam_questions_content_hash'),
    )
    op.create_index('ix_pmp_exam_questions_content_hash', 'pmp_exam_questions', ['content_hash'], unique=True)
    op.create_index('ix_pmp_exam_questions_chapter_slug', 'pmp_exam_questions', ['chapter_slug'])


def downgrade() -> None:
    op.drop_index('ix_pmp_exam_questions_chapter_slug', table_name='pmp_exam_questions')
    op.drop_index('ix_pmp_exam_questions_content_hash', table_name='pmp_exam_questions')
    op.drop_table('pmp_exam_questions')
