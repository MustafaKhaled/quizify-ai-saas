# Marketing Demo Video — Capture & Swap

The hero on the homepage and every `/exams/*` landing page renders a video
element via `app/components/PromotionalVideo.vue`. Until you record a real
demo, the player falls back to the `dashboard.svg` poster image so the hero
never renders broken — but the user can't actually play anything.

## What to record (target: 30 seconds)

A tight screen capture showing the path from "open the app" to "first quiz
result". The strategy explicitly recommends a 30-second demo here, so don't
let it sprawl.

Suggested storyboard:

| Seconds | What's on screen |
|---|---|
| 0–4   | Dashboard with the four predefined-subject cards (PMP, AWS, German A1, German A2). Cursor moves toward German A1. |
| 5–10  | Click into the German A1 detail page. Pick `akkusativ` from the chapter list. Click "Generate Quiz". |
| 11–15 | Loading spinner → quiz appears. Show the first question with a mini-context stem. |
| 16–22 | Click an option, see the explanation card. |
| 23–28 | Skip to the results page — score ring, per-topic breakdown, "Focus next on" suggestions. |
| 29–30 | End frame: Quizify logo + "Get started — quizifyai.app". |

## Where to drop the files

Save the recording in two formats and put them in this folder:

- `public/videos/quizify-demo.mp4` — H.264, baseline profile, ~1500 kbps, max 30 fps
- `public/videos/quizify-demo.webm` — VP9, ~1200 kbps (smaller, modern browsers prefer it)

Use ffmpeg to produce both from a single source recording:

```bash
ffmpeg -i source.mov -vf scale=1600:-2 -c:v libx264 -profile:v baseline -b:v 1500k -an public/videos/quizify-demo.mp4
ffmpeg -i source.mov -vf scale=1600:-2 -c:v libvpx-vp9 -b:v 1200k -an public/videos/quizify-demo.webm
```

(`-an` strips audio — you don't want a soundtrack on a 30-second silent demo.)

## After dropping the files

Nothing else to do. `PromotionalVideo.vue` already references both paths; once
the files exist, the player works automatically. The poster image
(`/screenshots/dashboard.svg`) shows on first paint until the user clicks play,
which keeps Largest Contentful Paint (LCP) fast.

## Optional: also swap the poster

The current poster is the SVG dashboard placeholder. If you capture a
high-resolution still frame from the real demo (the dashboard frame around the
2-second mark), save it as `public/screenshots/dashboard.png` and update
`POSTER` in `PromotionalVideo.vue` to `.png`.
