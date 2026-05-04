"""
Predefined-subject agent registry.

Each predefined subject (PMP, AWS Cloud Practitioner, ...) lives under its own
package in this folder. The registry below makes them discoverable by slug so
the predefined router and frontend don't need to hardcode subject names.

Adding a new subject:
  1. Create `agents/<slug>/` mirroring the PMP layout (config, instructions.md,
     knowledge_base/{chapters.py, retrieval.py, ingest.py, seed/}).
  2. Each agent module must expose: SUBJECT_NAME, SUBJECT_COLOR, SUBJECT_ICON,
     INSTRUCTIONS, CHAPTERS, get_chapter_by_slug, build_corpus_text.
  3. Register the slug in PREDEFINED_AGENTS below.
"""

from typing import Optional

from agents import clf_c02 as _clf_c02
from agents import deutsch_a1 as _deutsch_a1
from agents import deutsch_a2 as _deutsch_a2
from agents import pmp as _pmp


PREDEFINED_AGENTS: dict[str, dict] = {
    "pmp": {
        "slug": "pmp",
        "name": _pmp.PMP_SUBJECT_NAME,
        "color": _pmp.PMP_SUBJECT_COLOR,
        "icon": _pmp.PMP_SUBJECT_ICON,
        "instructions": _pmp.INSTRUCTIONS,
        "chapters": _pmp.PMP_CHAPTERS,
        "get_chapter_by_slug": _pmp.get_chapter_by_slug,
        "build_corpus_text": _pmp.build_corpus_text,
    },
    "clf_c02": {
        "slug": "clf_c02",
        "name": _clf_c02.CLF_C02_SUBJECT_NAME,
        "color": _clf_c02.CLF_C02_SUBJECT_COLOR,
        "icon": _clf_c02.CLF_C02_SUBJECT_ICON,
        "instructions": _clf_c02.INSTRUCTIONS,
        "chapters": _clf_c02.CLF_C02_CHAPTERS,
        "get_chapter_by_slug": _clf_c02.get_chapter_by_slug,
        "build_corpus_text": _clf_c02.build_corpus_text,
    },
    "deutsch_a1": {
        "slug": "deutsch_a1",
        "name": _deutsch_a1.DEUTSCH_A1_SUBJECT_NAME,
        "color": _deutsch_a1.DEUTSCH_A1_SUBJECT_COLOR,
        "icon": _deutsch_a1.DEUTSCH_A1_SUBJECT_ICON,
        "instructions": _deutsch_a1.INSTRUCTIONS,
        "chapters": _deutsch_a1.DEUTSCH_A1_CHAPTERS,
        "get_chapter_by_slug": _deutsch_a1.get_chapter_by_slug,
        "build_corpus_text": _deutsch_a1.build_corpus_text,
    },
    "deutsch_a2": {
        "slug": "deutsch_a2",
        "name": _deutsch_a2.DEUTSCH_A2_SUBJECT_NAME,
        "color": _deutsch_a2.DEUTSCH_A2_SUBJECT_COLOR,
        "icon": _deutsch_a2.DEUTSCH_A2_SUBJECT_ICON,
        "instructions": _deutsch_a2.INSTRUCTIONS,
        "chapters": _deutsch_a2.DEUTSCH_A2_CHAPTERS,
        "get_chapter_by_slug": _deutsch_a2.get_chapter_by_slug,
        "build_corpus_text": _deutsch_a2.build_corpus_text,
    },
}


def get_agent(slug: str) -> Optional[dict]:
    """Return the agent registration for a slug, or None if unknown."""
    return PREDEFINED_AGENTS.get(slug)


def list_agents() -> list[dict]:
    """Public-safe metadata for every registered agent (no callables)."""
    return [
        {"slug": a["slug"], "name": a["name"], "color": a["color"], "icon": a["icon"]}
        for a in PREDEFINED_AGENTS.values()
    ]
