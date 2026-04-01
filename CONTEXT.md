# Quizify AI — Project Context

## Architecture

| Layer | Tech | URL (dev) |
|---|---|---|
| Marketing site | Nuxt 3 + Nuxt UI | `http://localhost:3000` |
| Dashboard | Nuxt 3 + Nuxt UI | `http://localhost:3001` |
| Backend API | FastAPI + PostgreSQL | `http://localhost:8000` |

---

## Authentication Flow

### Email Login / Signup
1. User submits form on marketing site
2. `POST /auth/login` or `POST /auth/register` with `credentials: 'include'`
3. Backend sets **two HttpOnly cookies** on the response:
   - `auth_token` — JWT, **3 months**, path `/`
   - `refresh_token` — random token (hashed in DB), **1 year**, path `/auth/refresh`
4. Frontend calls `window.location.replace(dashboardUrl)` — replaces history so back button skips login
5. Dashboard global middleware (`auth.global.ts`) calls `GET /auth/verify` with `credentials: 'include'`
6. If valid → user lands on dashboard

### Google OAuth
1. User clicks "Continue with Google" → navigates to `GET /auth/google/login`
2. Backend stores OAuth state in `oauth_states` DB table (cross-device safe)
3. Backend redirects to Google
4. Google redirects back to `GET /auth/google/callback`
5. Backend validates state against DB, manually exchanges code with Google token endpoint (bypasses authlib session)
6. Backend creates a **one-time handoff code** (stored in `handoff_codes` table, 60s TTL) and redirects to `dashboard/?code=xxx`
7. Dashboard middleware sees `?code=`, calls `POST /auth/exchange` with `credentials: 'include'`
8. Backend validates code, sets both cookies on the exchange response
9. Middleware cleans the URL, user lands on dashboard

> **Why handoff code for Google?** Setting cookies on a `RedirectResponse` is unreliable across ports in development. The exchange-via-fetch approach guarantees the browser stores the cookie correctly.

### Token Refresh
- Dashboard plugin (`auth-refresh.client.ts`) intercepts any 401 response
- Calls `POST /auth/refresh` — browser automatically sends `refresh_token` cookie (path-scoped)
- Backend validates refresh token hash in DB, issues a new `auth_token` cookie
- Original request is retried transparently
- If refresh also fails → redirect to `marketingUrl/login`

### Logout
- `POST /auth/logout` — blacklists the access token + marks refresh token as revoked in DB
- Clears both cookies
- Frontend redirects to `marketingUrl/login`

---

## Cookie Security Design

| Cookie | HttpOnly | Secure | SameSite | Path | Max-Age |
|---|---|---|---|---|---|
| `auth_token` | ✓ | prod only | Lax | `/` | 3 months |
| `refresh_token` | ✓ | prod only | Lax | `/auth/refresh` | 1 year |

- `COOKIE_DOMAIN` env var: `None` in dev, `.quizify.ai` in production (covers all subdomains)
- `ENVIRONMENT=production` enables `Secure` flag

---

## Backend Key Endpoints

### Auth
| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register, sets both cookies |
| POST | `/auth/login` | Login, sets both cookies |
| GET | `/auth/verify` | Check if session is valid |
| POST | `/auth/refresh` | Issue new access token from refresh cookie |
| POST | `/auth/logout` | Revoke tokens, clear cookies |
| GET | `/auth/google/login` | Start Google OAuth |
| GET | `/auth/google/callback` | Google OAuth callback |
| POST | `/auth/exchange` | Exchange handoff code for cookie (Google OAuth) |

### Subjects
| Method | Path | Description |
|---|---|---|
| POST | `/subjects` | Create a subject |
| GET | `/subjects` | List user's subjects (with source/quiz counts) |
| GET | `/subjects/{id}` | Get subject detail |
| PATCH | `/subjects/{id}` | Rename or recolor subject |
| DELETE | `/subjects/{id}` | Delete subject (sources become unassigned) |
| GET | `/subjects/{id}/sources` | List sources in subject |
| GET | `/subjects/{id}/quizzes` | List all quizzes in subject (source-level + subject-wide) |
| POST | `/subjects/{id}/quiz` | Generate subject-wide quiz from all sources' combined text |

### Quizzes
| Method | Path | Description |
|---|---|---|
| POST | `/quizzes/create` | Upload PDF + generate quiz (accepts `subject_id` form field) |
| POST | `/quizzes/create-focused` | Generate focused quiz from existing source on specific topics |
| GET | `/quizzes/sources` | List all user sources |
| DELETE | `/quizzes/sources/{id}` | Delete source and its quizzes |
| GET | `/quizzes/my_quizzes` | List all user quizzes |
| GET | `/quizzes/{quiz_id}` | Get quiz by ID |
| DELETE | `/quizzes/{quiz_id}` | Delete quiz |
| POST | `/quizzes/submit/{quiz_id}` | Submit answers, returns score + result_id |
| GET | `/quizzes/my_results` | List all user results |
| GET | `/quizzes/results/{quiz_id}` | Results for a specific quiz |
| GET | `/quizzes/result/{result_id}/review` | Full result review with breakdown |
| GET | `/quizzes/performance/by-topic` | Aggregated topic performance + weak areas |

---

## Database Tables

### Auth-related
| Table | Purpose |
|---|---|
| `users` | User accounts |
| `blacklisted_tokens` | Revoked access tokens (logout) |
| `refresh_tokens` | Refresh token hashes with expiry/revoked flag |
| `handoff_codes` | One-time codes for Google OAuth cookie exchange |
| `oauth_states` | Google OAuth CSRF state (cross-device safe) |

### Quiz-related
| Table | Purpose |
|---|---|
| `subjects` | Top-level study containers (name, color, user_id) |
| `quiz_sources` | Uploaded PDFs with extracted text; `subject_id` FK (nullable, SET NULL on subject delete) |
| `quizzes` | Generated quizzes; `source_id` nullable (NULL for subject-wide quizzes); `subject_id` nullable (set for subject-wide quizzes) |
| `quiz_results` | Attempt records: score, breakdown JSONB, `started_at`, `ended_at`, `time_taken_seconds`, `time_remaining_seconds` |

### Quiz type: source-level vs subject-wide
- **Source-level quiz**: `source_id IS NOT NULL`, `subject_id IS NULL`
- **Subject-wide quiz**: `source_id IS NULL`, `subject_id IS NOT NULL` — generated by concatenating extracted text from all sources in the subject

---

## Quiz Types
| Value | Description |
|---|---|
| `single_choice` | One correct answer (radio buttons) |
| `multiple_select` | Multiple correct answers (checkboxes); scored with exact set match |
| `true_or_false` | Two options True/False (radio buttons); uses `correct_option_index` |

---

## Timer & Submission Tracking
- `time_limit` on `quizzes` table is in **minutes**
- Frontend records `started_at` when quiz page loads; sends it with submission
- Backend computes `time_taken_seconds = ended_at - started_at`, `time_remaining_seconds = (time_limit * 60) - time_taken_seconds`
- Countdown timer auto-submits the quiz when it reaches 0
- Navigation guard (`onBeforeRouteLeave` + `beforeunload`) warns user if they try to leave mid-quiz

---

## Frontend Structure

### Marketing (`frontend/marketing/`)
- `app/pages/login.vue` — Email login + Google OAuth button
- `app/pages/signup.vue` — Email signup + Google OAuth button
- `app/components/AppHeader.vue` — Calls `/auth/verify` to show "Your Account" vs "Sign in"
- `app/middleware/redirect-if-authenticated.global.ts` — Redirects logged-in users away from login/signup

### Dashboard (`frontend/dashboard/`)
- `app/middleware/auth.global.ts` — Protects all routes, handles `?code=` exchange for Google OAuth
- `app/plugins/auth-refresh.client.ts` — Auto-refresh on 401
- `app/components/UserMenu.vue` — Visible logout button in sidebar footer
- `app/layouts/default.vue` — Sidebar nav: Dashboard, My Subjects, New Quiz, My Quizzes

#### Pages
| Route | File | Purpose |
|---|---|---|
| `/dashboard` | `pages/dashboard.vue` | Home: stats, weak topics, recent quizzes |
| `/subjects` | `pages/subjects/index.vue` | Subject card grid |
| `/subjects/new` | `pages/subjects/new.vue` | Create subject (name + color picker) |
| `/subjects/[id]` | `pages/subjects/[id].vue` | Subject detail: sources + quizzes per source + subject-wide quiz modal |
| `/quiz-new` | `pages/quiz-new.vue` | Upload PDF, create quiz; accepts `?subject_id=` and `?source_id=` query params |
| `/quizzes` | `pages/quizzes.vue` | All quizzes list |
| `/quiz/[id]` | `pages/quiz/[id].vue` | Take quiz with countdown timer |
| `/results/[id]` | `pages/results/[id].vue` | Results + topic breakdown; back button returns to subject if applicable |

---

## User Flow

```
Subject (e.g. "Organic Chemistry")
  └── Source 1 (Chapter 1.pdf)  — uploaded via /quiz-new?subject_id=xxx
        ├── Quiz A — single_choice
        └── Quiz B — true_or_false
  └── Source 2 (Chapter 2.pdf)
        └── Quiz A — multiple_select
  └── Subject-Wide Quiz — generated from all sources combined via POST /subjects/{id}/quiz
```

Navigation after quiz creation uses `replace: true` so the back button skips the creation form.

---

## Environment Variables

### Backend
| Var | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | Secret for signing JWTs |
| `SESSION_SECRET_KEY` | Starlette session middleware secret |
| `FRONTEND_URL` | Marketing site URL |
| `DASHBOARD_URL` | Dashboard URL |
| `BACKEND_URL` | Backend URL (for OAuth redirect URI) |
| `COOKIE_DOMAIN` | Cookie domain (empty in dev, `.quizify.ai` in prod) |
| `ENVIRONMENT` | Set to `production` to enable Secure cookies |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `GEMINI_API_KEY` | Gemini API key for AI quiz generation |

### Frontend (both apps via `nuxt.config`)
| Var | Description |
|---|---|
| `NUXT_PUBLIC_API_BASE` | Backend API URL |
| `NUXT_PUBLIC_DASHBOARD_URL` | Dashboard URL (marketing app) |
| `NUXT_PUBLIC_MARKETING_URL` | Marketing URL (dashboard app) |

---

## Production Deployment (Railway + Subdomains)

- Marketing: `quizify.ai`
- Dashboard: `dashboard.quizify.ai`
- Backend: `api.quizify.ai`
- Set `COOKIE_DOMAIN=.quizify.ai` and `ENVIRONMENT=production` on the backend service
- Cookies will be shared across all subdomains automatically

---

## Pending / Notes
- Logo files: `quizify_ai_logo.png` and `quizify_icon.png` must be in `public/` of both frontend apps
- Run `alembic upgrade head` after each deploy to apply DB migrations
- Access token is 3 months — refresh token logic exists but is rarely triggered
- Gemini model in use: `gemini-2.5-flash`
