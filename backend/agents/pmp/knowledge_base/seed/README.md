# PMP Exam Bank — Seed Data

Source-of-truth file for the PMP exam bank. The `ingest.py` script reads
`exam_bank.json` and upserts rows into the `pmp_exam_questions` table.

## Schema

Each entry in `exam_bank.json` must match this shape:

```json
{
  "chapter_slug": "risk",
  "stem": "A key stakeholder raises a new requirement mid-sprint...",
  "quiz_type": "single_choice",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 2,
  "explanation": "The correct answer is C because the project manager should first...",
  "source": "PMI 2021 sample exam",
  "difficulty": "medium"
}
```

## Field Reference

| Field | Required | Notes |
|---|---|---|
| `chapter_slug` | yes | Must match a slug in `chapters.py` (e.g. `integration`, `scope`, `risk`). |
| `stem` | yes | The question prompt. |
| `quiz_type` | yes | One of: `single_choice`, `multiple_select`, `true_or_false`. |
| `options` | yes | Exactly 4 strings for MCQ, exactly `["True", "False"]` for T/F. |
| `correct_index` | single/tf | Integer index into `options`. |
| `correct_option_indices` | multi-select | List of integers (use instead of `correct_index`). |
| `explanation` | yes | Why the correct answer is right. Used for review. |
| `source` | yes | Human-readable attribution (publication, year, author). |
| `difficulty` | optional | `easy` \| `medium` \| `hard`. Defaults to `medium`. |

## Copyright Note

Don't commit verbatim PMI-copyrighted questions. For real PMI exam Qs, either:
- Paraphrase substantially before committing, or
- Store them in the DB directly via a separate admin-only loader that doesn't go
  into version control.

Exemplar-mode generation doesn't require verbatim questions — style/structure is
what the model needs.

## Running the Ingest

```bash
cd backend
python -m agents.pmp.knowledge_base.ingest
```

With a dry-run flag (validate without writing):

```bash
python -m agents.pmp.knowledge_base.ingest --dry-run
```
