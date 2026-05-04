"""
Exam-bank retrieval helpers.

Generic over `subject_slug` so adding new predefined subjects (CFA, AWS, etc.)
doesn't require a new module — the same get_exemplars/format_exemplars work
for every subject.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import PredefinedExamQuestion


def get_exemplars(
    db: Session,
    subject_slug: str,
    chapter_slugs: list[str] | None = None,
    k: int = 3,
) -> list[PredefinedExamQuestion]:
    """Return up to k random exam questions, optionally filtered by chapter_slug."""
    if k <= 0:
        return []
    query = db.query(PredefinedExamQuestion).filter(
        PredefinedExamQuestion.subject_slug == subject_slug
    )
    if chapter_slugs:
        query = query.filter(PredefinedExamQuestion.chapter_slug.in_(chapter_slugs))
    return query.order_by(func.random()).limit(k).all()


def format_exemplars(exemplars: list[PredefinedExamQuestion]) -> str:
    """Render exemplars as a prompt-friendly text block. Empty string if none."""
    if not exemplars:
        return ""
    parts = []
    for i, q in enumerate(exemplars, 1):
        opts = "\n".join(f"  {chr(65 + j)}. {o}" for j, o in enumerate(q.options or []))
        parts.append(
            f"Example {i} — chapter: {q.chapter_slug}\n"
            f"Q: {q.stem}\n"
            f"{opts}\n"
            f"Explanation: {q.explanation}"
        )
    return "\n\n".join(parts)
