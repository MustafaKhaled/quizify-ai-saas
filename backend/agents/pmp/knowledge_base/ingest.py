"""
PMP exam bank ingest script.

Reads `seed/exam_bank.json`, validates each row, and upserts into the
`pmp_exam_questions` table.

Status: skeleton. The DB model and Alembic migration are TODO — this script
currently validates the seed file and prints what would be inserted. Wire in
the SQLAlchemy upsert once the schema is in place.

Usage:
    python -m agents.pmp.knowledge_base.ingest
    python -m agents.pmp.knowledge_base.ingest --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

from .chapters import PMP_CHAPTERS

SEED_PATH = Path(__file__).parent / "seed" / "exam_bank.json"
VALID_QUIZ_TYPES = {"single_choice", "multiple_select", "true_or_false"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
CHAPTER_SLUGS = {c["slug"] for c in PMP_CHAPTERS}


class ValidationError(Exception):
    pass


def validate_row(row: dict, index: int) -> None:
    def fail(msg: str) -> None:
        raise ValidationError(f"row {index}: {msg}")

    for required in ("chapter_slug", "stem", "quiz_type", "options", "explanation", "source"):
        if required not in row:
            fail(f"missing required field '{required}'")

    if row["chapter_slug"] not in CHAPTER_SLUGS:
        fail(f"unknown chapter_slug '{row['chapter_slug']}' (valid: {sorted(CHAPTER_SLUGS)})")

    if row["quiz_type"] not in VALID_QUIZ_TYPES:
        fail(f"invalid quiz_type '{row['quiz_type']}' (valid: {sorted(VALID_QUIZ_TYPES)})")

    options = row["options"]
    if not isinstance(options, list) or not all(isinstance(o, str) for o in options):
        fail("'options' must be a list of strings")

    if row["quiz_type"] == "true_or_false":
        if options != ["True", "False"]:
            fail("true_or_false requires options == ['True', 'False']")
    elif len(options) != 4:
        fail(f"{row['quiz_type']} requires exactly 4 options, got {len(options)}")

    if row["quiz_type"] == "multiple_select":
        indices = row.get("correct_option_indices")
        if not isinstance(indices, list) or not indices:
            fail("multiple_select requires 'correct_option_indices' (non-empty list of ints)")
        if not all(isinstance(i, int) and 0 <= i < len(options) for i in indices):
            fail("'correct_option_indices' contains out-of-range value")
    else:
        idx = row.get("correct_index")
        if not isinstance(idx, int) or not (0 <= idx < len(options)):
            fail("'correct_index' must be an int within options range")

    difficulty = row.get("difficulty", "medium")
    if difficulty not in VALID_DIFFICULTIES:
        fail(f"invalid difficulty '{difficulty}'")


def load_seed() -> list[dict]:
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"seed file not found: {SEED_PATH}")
    with SEED_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("seed file must contain a JSON array at the top level")
    return data


def _content_hash(stem: str, source: str) -> str:
    """Stable hash over normalized stem+source; serves as the upsert key."""
    normalized = f"{stem.strip().lower()}|{source.strip().lower()}"
    return sha256(normalized.encode("utf-8")).hexdigest()


def upsert_to_db(rows: list[dict]) -> int:
    """
    Upsert each row into pmp_exam_questions, keyed by content_hash(stem, source).
    Returns the number of rows processed (inserted + updated).
    """
    # Deferred imports so --dry-run works without DATABASE_URL.
    from sqlalchemy.dialects.postgresql import insert as pg_insert

    from db.database import SessionLocal
    from db.models import PMPExamQuestion

    session = SessionLocal()
    try:
        processed = 0
        for row in rows:
            payload = {
                "content_hash": _content_hash(row["stem"], row["source"]),
                "chapter_slug": row["chapter_slug"],
                "stem": row["stem"],
                "quiz_type": row["quiz_type"],
                "options": row["options"],
                "correct_index": row.get("correct_index"),
                "correct_option_indices": row.get("correct_option_indices"),
                "explanation": row["explanation"],
                "source": row["source"],
                "difficulty": row.get("difficulty", "medium"),
            }
            stmt = pg_insert(PMPExamQuestion).values(**payload)
            stmt = stmt.on_conflict_do_update(
                index_elements=["content_hash"],
                set_={
                    "chapter_slug": stmt.excluded.chapter_slug,
                    "stem": stmt.excluded.stem,
                    "quiz_type": stmt.excluded.quiz_type,
                    "options": stmt.excluded.options,
                    "correct_index": stmt.excluded.correct_index,
                    "correct_option_indices": stmt.excluded.correct_option_indices,
                    "explanation": stmt.excluded.explanation,
                    "difficulty": stmt.excluded.difficulty,
                },
            )
            session.execute(stmt)
            processed += 1
        session.commit()
        return processed
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest PMP exam bank seed data.")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing to DB.")
    args = parser.parse_args()

    try:
        rows = load_seed()
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR loading seed: {e}", file=sys.stderr)
        return 1

    for i, row in enumerate(rows):
        try:
            validate_row(row, i)
        except ValidationError as e:
            print(f"VALIDATION FAILED: {e}", file=sys.stderr)
            return 1

    print(f"Validated {len(rows)} rows.")

    if args.dry_run:
        print("Dry run complete — no DB writes.")
        return 0

    if not rows:
        print("No rows to ingest. Add questions to seed/exam_bank.json first.")
        return 0

    processed = upsert_to_db(rows)
    print(f"Upserted {processed} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
