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

---

## Database Tables (auth-related)

| Table | Purpose |
|---|---|
| `users` | User accounts |
| `blacklisted_tokens` | Revoked access tokens (logout) |
| `refresh_tokens` | Refresh token hashes with expiry/revoked flag |
| `handoff_codes` | One-time codes for Google OAuth cookie exchange |
| `oauth_states` | Google OAuth CSRF state (cross-device safe) |

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
