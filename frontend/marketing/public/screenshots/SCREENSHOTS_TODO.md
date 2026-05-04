# Marketing Screenshots — Replace These

The marketing homepage references three product screenshots. Each is currently a
branded SVG placeholder so the page never breaks, but you should swap them for
real captures of the dashboard before launch. Keep the same aspect ratio (16:9)
and ideally export at 1600×900 for crisp display on retina.

## Files to capture and drop in

| File | Section | What to capture |
|---|---|---|
| `dashboard.svg` → `dashboard.png` | "Smarter Study Tools" | Logged-in dashboard showing the stat cards (subscription, recent activity, weak topics) and the predefined-subject row. |
| `quiz-runner.svg` → `quiz-runner.png` | "Master Every Subject" | A quiz mid-question — visible timer, progress bar, four answer options, one selected. Use a German A2 question (e.g., on `dativ`) to match the placeholder. |
| `results.svg` → `results.png` | "Premium Exam Prep" | Quiz-results page — score ring, per-topic breakdown bars, "Focus next on" suggestions. |

## How the swap works

The image references in `content/0.index.yml` use `image: /screenshots/<file>`. To swap:

1. Save the new screenshot as PNG with the matching base name (e.g., `dashboard.png`).
2. Update `image:` in `0.index.yml` to point at the `.png` instead of the `.svg`.
3. Delete the old `.svg` (optional — keeps the folder clean).

The `ImagePlaceholder` component renders the new image on top of its dashed
fallback, so even if you only swap two of the three, the third still looks
intentional rather than broken.

## Capturing tips

- Use a clean test account so no PII shows up.
- Pick the dark theme — the SVGs and the marketing site default to a dark aesthetic.
- Crop tightly around the relevant UI surface; avoid huge whitespace.
- If you have a Figma export, that works too — just save as PNG at 1600×900.
