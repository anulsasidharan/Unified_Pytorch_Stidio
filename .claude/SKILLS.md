# SKILLS.md — PyTorch Learning Studio

Catalog of agent skills for this repository. Each skill defines **when** to use it, **what to read first**, and **non-negotiable implementation rules**.

---

## Skill index

| Skill | Path | Use when |
|-------|------|----------|
| **pytorch-studio-dev** | This file § [Primary skill](#primary-skill-pytorch-studio-dev) | Building features, APIs, UI, DB, AI tutor, or infra in this repo |
| **pytorch-question-authoring** | This file § [Question authoring](#skill-pytorch-question-authoring) | Seeding or creating exercises, test cases, hints, solutions |
| **pytorch-analytics-tracking** | This file § [Analytics](#skill-pytorch-analytics-tracking) | Daily tracker, streaks, XP, heatmap, SM-2 revision queue |

---

## Primary skill: `pytorch-studio-dev`

```yaml
name: pytorch-studio-dev
description: >-
  Builds and extends PyTorch Learning Studio (Next.js/FastAPI/PostgreSQL platform:
  13 modules, exercises, Colab, tracker, SM-2 revision, AI tutor). Use per CLAUDE.md,
  PLAN_PHASE.md, and MEMORY.md.
disable-model-invocation: false
```

### When to use

- Scaffolding or changing `frontend/`, `backend/`, or `docker-compose.yml`
- Adding FastAPI routers, SQLAlchemy models, Next.js pages, or Monaco exercise flows
- Implementing import (CSV/JSON/notebook), SM-2 spaced repetition, Colab, or tutor endpoints
- Following the phased roadmap in `PLAN_PHASE.md`

### Required reading order

1. `.claude/MEMORY.md` — current phase, locked decisions, blockers
2. `.claude/PLAN_PHASE.md` — active phase tasks and exit criteria
3. `.claude/rules/CLAUDE.md` — detailed spec for the area you are changing
4. `.claude/specs/<area>.md` — focused extract (database, api-design, etc.)
5. `.claude/PLAN.md` — scope and priorities if trade-offs arise

### Non-negotiables

| Area | Rule |
|------|------|
| API | FastAPI + Pydantic v2; validate inputs; consistent error JSON |
| Auth | JWT; protect user-scoped routes; never log passwords or tokens |
| Data | PostgreSQL as source of truth; Alembic migrations backward-compatible |
| Exercises | Full quality bar: statement, constraints, starter code, test cases, hints, solutions |
| Question types | Support all 6 types per spec §7 Feature 2 |
| AI tutor | Anthropic only; PyTorch system prompt from spec §9; no full solution on first hint |
| Colab | Generate notebook via nbformat when `colab_link` absent |
| Spaced repetition | SM-2 algorithm from spec §12 — do not use fixed intervals |
| Secrets | `.env` only; never commit API keys |
| Tests | pytest (backend); Playwright (frontend E2E); meaningful paths not trivia |
| UI | Tailwind + shadcn/ui; responsive; accessibility for forms and editor |

### Target directory layout

```text
frontend/
  app/                     # Next.js 14 App Router pages
  components/              # editor/, question/, tracker/, tutor/, ui/
  lib/                     # api.ts, auth.ts, utils.ts
  store/                   # Zustand stores
backend/
  app/
    main.py, config.py, database.py
    models/                # SQLAlchemy models
    routers/               # FastAPI route modules
    services/              # spaced_repetition, tutor, colab, import, analytics
    tasks/                 # Celery app + cron tasks
  alembic/versions/
  seeds/                   # topics.py, questions_*.py
  tests/
docker-compose.yml
.env.example
```

### Implementation workflow

#### 1. Scope the task

- Map request to **phase** in `PLAN_PHASE.md` and row in `TASKS.md`
- List surfaces: DB, API, frontend, AI, infra
- If out of current phase, note in `MEMORY.md` and confirm with user

#### 2. Backend feature pattern

1. SQLAlchemy model + Alembic migration
2. Service layer (`services/`)
3. Router (`routers/`) + Pydantic schemas
4. pytest integration tests
5. Register router in `main.py`; document env vars in `.env.example`

#### 3. Frontend feature pattern

1. API client methods in `lib/api.ts`
2. Zustand store slice if needed
3. Page under `app/` + components under `components/`
4. Loading, error, and empty states
5. Playwright tests for critical flows (login, submit, tutor chat)

#### 4. Exercise / submission flow

1. Load question + sample test cases
2. Monaco editor with starter code (type-specific behavior per spec §7)
3. `POST /attempts` → validate code output / shape
4. Persist `user_attempts` + update `user_progress` + award XP
5. On correct, add to `revision_queue` via SM-2

#### 5. Done checklist

- [ ] Migration applied locally (`alembic upgrade head`)
- [ ] API documented in FastAPI `/docs` or `specs/api-design.md` if contract changed
- [ ] `TASKS.md` row updated
- [ ] `MEMORY.md` updated if decision locked or phase completed

---

## Skill: `pytorch-question-authoring`

### When to use

- Writing seed data, bulk CSV/JSON import, or manual exercise forms
- Reviewing exercise quality before merge

### Rules

- Three difficulty levels per module subtopic where applicable
- Six question types: `code_completion`, `debug_model`, `conceptual_mcq`, `build_from_scratch`, `notebook_challenge`, `shape_assertion`
- Hints: 3–5 progressive levels; each costs −2 XP when revealed
- At least one solution with explanation; mark optimal where applicable
- Tags: text array (e.g. `["autograd", "backprop", "loss"]`)
- Slug: URL-safe unique per question
- PyTorch fields: `starter_code`, `expected_output_shape`, `colab_link`, `gpu_required`, `pytorch_version`, `xp_reward`

### Reference

- Example format: `rules/CLAUDE.md` §10 (Gradient Accumulation exercise)
- Distribution: ~40 exercises per module (varies by module per spec §6)
- CSV/JSON import formats: spec §15

---

## Skill: `pytorch-analytics-tracking`

### When to use

- Daily summary cards, heatmaps, streaks, goals, XP timeline, revision dashboard
- `daily_activity`, `user_progress`, `revision_queue` logic

### Rules

- One `daily_activity` row per user per calendar date (unique constraint)
- Streak: increment when daily goal met; Celery aggregation at 00:05 UTC
- XP awards per spec §13 (difficulty-based, hint penalty, streak bonuses)
- SM-2 revision: use `calculate_next_review()` from spec §12 verbatim
- Rating scale: 0=blackout, 3=hard, 4=good, 5=easy
- Charts: Recharts — match dashboard wireframes in spec §11

### SM-2 intervals (adaptive)

- Failed recall (rating < 3): reset to 1 day, decrease ease factor
- First success: 1 day
- Second success: 6 days
- Subsequent: `round(interval_days * ease_factor)`

---

## Adding a new skill

1. Add a row to the **Skill index** table above  
2. Document YAML `name` + `description`, reading order, and non-negotiables  
3. Link to the relevant `specs/*.md` section  
4. Update `MEMORY.md` documentation index if the skill changes agent workflow
