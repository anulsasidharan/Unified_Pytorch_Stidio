# API Design — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §8 REST API Endpoints*

Base URL: `/api/v1` · Auth: Bearer JWT unless noted.

---

## Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/auth/logout` | Invalidate session |
| POST | `/auth/refresh` | Refresh JWT token |
| GET | `/auth/me` | Get current user profile |
| PUT | `/auth/me` | Update profile (name, daily_goal, pytorch_level) |

---

## Topics & Modules

| Method | Path | Description |
|--------|------|-------------|
| GET | `/topics` | List all 13 modules with user progress |
| GET | `/topics/{slug}` | Get module detail + exercise list |
| GET | `/topics/{slug}/progress` | Get user's progress for this module |

---

## Questions

| Method | Path | Description |
|--------|------|-------------|
| GET | `/questions` | List questions (filters: topic, difficulty, type, tags) |
| GET | `/questions/{id}` | Get question detail (statement, starter_code, hints) |
| GET | `/questions/{id}/solution` | Get solution (requires 1 attempt first) |
| GET | `/questions/{id}/test-cases` | Get visible test cases |
| POST | `/questions/{id}/bookmark` | Toggle bookmark |
| GET | `/questions/bookmarked` | Get all bookmarked questions |

---

## Attempts & Submissions

| Method | Path | Description |
|--------|------|-------------|
| POST | `/attempts` | Submit answer `{question_id, code, result, time_spent_secs}` |
| GET | `/attempts` | Get user's attempt history (paginated) |
| GET | `/attempts/question/{id}` | Get all attempts for a specific question |

**Submit response (example shape):**

```json
{
  "result": "correct",
  "xp_earned": 20,
  "runtime_ms": 45,
  "error_message": null,
  "added_to_revision": true
}
```

---

## Progress & Tracker

| Method | Path | Description |
|--------|------|-------------|
| GET | `/progress` | Full progress summary across all modules |
| GET | `/progress/topic/{slug}` | Progress for specific module |
| GET | `/tracker/dashboard` | Dashboard stats (streak, today's summary, weekly) |
| GET | `/tracker/heatmap` | 52-week heatmap data |
| GET | `/tracker/history` | Daily activity log (paginated) |
| GET | `/tracker/streak` | Streak data (current, longest, last_active) |

---

## Revision Queue (SM-2)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/revision/due` | Questions due for review today |
| POST | `/revision/review` | Submit review rating `{question_id, rating: 0-5}` |
| GET | `/revision/stats` | Queue size, due today, overdue |
| DELETE | `/revision/{question_id}` | Remove from queue |

**SM-2 rating scale:** 0=blackout, 3=hard, 4=good, 5=easy

---

## AI Tutor

| Method | Path | Description |
|--------|------|-------------|
| POST | `/tutor/chat` | Send message to AI tutor |
| GET | `/tutor/history` | Get chat history (last 50 messages) |
| DELETE | `/tutor/history` | Clear chat history |
| GET | `/tutor/usage` | Get daily message count vs limit |

---

## Colab Integration

| Method | Path | Description |
|--------|------|-------------|
| GET | `/colab/{question_id}` | Get or generate Colab URL for question |
| POST | `/colab/import` | Import notebook from Colab URL |

---

## Import

| Method | Path | Description |
|--------|------|-------------|
| POST | `/import/manual` | Create custom question manually |
| POST | `/import/csv` | Bulk import from CSV file |
| POST | `/import/json` | Import from JSON payload |
| POST | `/import/notebook` | Import from notebook URL |
| GET | `/import/history` | Get import history |
| GET | `/custom-questions` | List user's custom questions |
| PUT | `/custom-questions/{id}` | Update custom question |
| DELETE | `/custom-questions/{id}` | Delete custom question |

---

## Cross-cutting concerns

| Concern | Rule |
|---------|------|
| Errors | `{ "detail": "message" }` (FastAPI default) or structured `{ error: { code, message } }` |
| Pagination | `?page=&limit=` on list endpoints |
| Rate limit | Redis-backed; stricter on `/tutor/*` (20/day free) and `/attempts` |
| Idempotency | Optional `Idempotency-Key` on POST import |
| CORS | Allow `FRONTEND_URL` only in production |
| Docs | Auto-generated OpenAPI at `/docs` (FastAPI) |

---

## OpenAPI

FastAPI auto-generates OpenAPI schema at `/docs` and `/openapi.json`. Keep Pydantic schemas in sync with this document when contracts change.
