"""
German B1 Lesen (Reading) agent package.

Mirrors the Hören package structure. Models the five Teile of the
Goethe-Zertifikat B1 reading section. Generates passage + comprehension
items in JSON. No TTS — Lesen is a pure-text feature; the cost driver
is just Gemini, an order of magnitude cheaper than Hören.
"""

from pathlib import Path

from .config import (
    DEUTSCH_B1_LESEN_SUBJECT_COLOR,
    DEUTSCH_B1_LESEN_SUBJECT_ICON,
    DEUTSCH_B1_LESEN_SUBJECT_NAME,
)
from .knowledge_base.chapters import (
    DEUTSCH_B1_LESEN_CHAPTERS,
    build_corpus_text,
    get_chapter_by_name,
    get_chapter_by_slug,
    topics_for_teil,
)

INSTRUCTIONS = (Path(__file__).parent / "instructions.md").read_text(encoding="utf-8")

__all__ = [
    "INSTRUCTIONS",
    "DEUTSCH_B1_LESEN_SUBJECT_NAME",
    "DEUTSCH_B1_LESEN_SUBJECT_COLOR",
    "DEUTSCH_B1_LESEN_SUBJECT_ICON",
    "DEUTSCH_B1_LESEN_CHAPTERS",
    "get_chapter_by_slug",
    "get_chapter_by_name",
    "build_corpus_text",
    "topics_for_teil",
]
