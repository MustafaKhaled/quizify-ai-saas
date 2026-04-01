"""add subjects table and update foreign keys

Revision ID: e2f3a4b5c6d7
Revises: d1e2f3a4b5c6
Create Date: 2026-03-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'e2f3a4b5c6d7'
down_revision: Union[str, None] = 'd1e2f3a4b5c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create subjects table
    op.create_table(
        'subjects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('color', sa.String(7), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_subjects_user_id', 'subjects', ['user_id'])

    # 2. Add subject_id to quiz_sources
    op.add_column('quiz_sources',
        sa.Column('subject_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True))
    op.create_index('ix_quiz_sources_subject_id', 'quiz_sources', ['subject_id'])

    # 3. Make quizzes.source_id nullable (needed for subject-wide quizzes)
    op.alter_column('quizzes', 'source_id',
                    existing_type=postgresql.UUID(as_uuid=True),
                    nullable=True)

    # 4. Add subject_id to quizzes
    op.add_column('quizzes',
        sa.Column('subject_id', postgresql.UUID(as_uuid=True),
                  sa.ForeignKey('subjects.id', ondelete='SET NULL'), nullable=True))
    op.create_index('ix_quizzes_subject_id', 'quizzes', ['subject_id'])


def downgrade() -> None:
    op.drop_index('ix_quizzes_subject_id', table_name='quizzes')
    op.drop_column('quizzes', 'subject_id')

    op.alter_column('quizzes', 'source_id',
                    existing_type=postgresql.UUID(as_uuid=True),
                    nullable=False)

    op.drop_index('ix_quiz_sources_subject_id', table_name='quiz_sources')
    op.drop_column('quiz_sources', 'subject_id')

    op.drop_index('ix_subjects_user_id', table_name='subjects')
    op.drop_table('subjects')
