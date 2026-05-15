"""
German A2 Hören (Listening) agent package.

Mirrors the B1 Hören package structure. Models the four Teile of the
Goethe-Zertifikat A2 listening section. Adapts the same audio + comprehension
pipeline to A2 vocabulary range: shorter scripts, simpler sentence structures,
everyday topics, and fewer comprehension items per Teil than B1.
"""

from pathlib import Path

from .config import (
    DEUTSCH_A2_HOREN_SUBJECT_COLOR,
    DEUTSCH_A2_HOREN_SUBJECT_ICON,
    DEUTSCH_A2_HOREN_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_A2_HOREN_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
    topics_for_teil,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_A2_HOREN_SUBJECT_NAME",
    "DEUTSCH_A2_HOREN_SUBJECT_COLOR",
    "DEUTSCH_A2_HOREN_SUBJECT_ICON",
    "DEUTSCH_A2_HOREN_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
    "topics_for_teil",
]
