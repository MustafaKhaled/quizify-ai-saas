"""
AWS Certified Cloud Practitioner (CLF-C02) agent package.

Exposes the stable identity (instructions, subject metadata) and the
knowledge-base helpers (chapter lookup, corpus text). Routers import from this
package via `agents/__init__.py`'s registry.
"""

from pathlib import Path

from .config import (
    CLF_C02_SUBJECT_COLOR,
    CLF_C02_SUBJECT_ICON,
    CLF_C02_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    CLF_C02_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "CLF_C02_SUBJECT_NAME",
    "CLF_C02_SUBJECT_COLOR",
    "CLF_C02_SUBJECT_ICON",
    "CLF_C02_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
]
