# CLF-C02 exam bank seed

Real third-party AWS Cloud Practitioner practice questions used as **style anchors**
for AI generation (3 sampled per request via `predefined_exam_questions`). Gemini
mirrors their tone and distractor pattern but does NOT copy them verbatim.

## Schema (per row)

```jsonc
{
  "id": "clf-c02_001",                       // optional, free-form, for human reference
  "chapter_slug": "cloud_concepts",           // MUST match a slug in chapters.py
  "stem": "Which AWS service…",
  "quiz_type": "single_choice",               // single_choice | multiple_select | true_or_false
  "options": ["A", "B", "C", "D"],            // exactly 4 for MCQ; ["True", "False"] for TF
  "correct_index": 1,                          // for single_choice / true_or_false
  "correct_option_indices": [0, 2],            // for multiple_select only
  "explanation": "Why the correct option is correct.",
  "source": "Whizlabs CLF-C02 free practice (Q12)",
  "difficulty": "easy"                         // easy | medium | hard (default: medium)
}
```

## Copyright

**Do not commit verbatim AWS official-sample questions** (those from
docs.aws.amazon.com or the official PDF). Use third-party prep sources:
Tutorials Dojo, Whizlabs, Stéphane Maarek (Udemy), AnalystPrep — and rephrase
where possible. AWS practice exams are tolerant of style emulation but strict
about direct copying.

## Ingest

```bash
# Validate without writing
python -m agents.clf_c02.knowledge_base.ingest --dry-run

# Upsert into predefined_exam_questions (tagged subject_slug='clf_c02')
python -m agents.clf_c02.knowledge_base.ingest
```

`content_hash = sha256(stem + source)` is the upsert key — re-running after edits
updates rows in place rather than duplicating.
