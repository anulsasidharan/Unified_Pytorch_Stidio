# MEMORY.md — PyTorch Learning Studio

> Persistent project memory for agents and developers. Update after meaningful decisions, phase completions, or blockers.

**Last updated:** 2026-06-03  
**Specification version:** `rules/CLAUDE.md` v1.0  
**Repository state:** Phase 5 **complete** — Modules 08–13 seeded, bulk expansion (~520 exercises), search UI/API, editor shortcuts, dark mode, responsive nav

---

## Project identity

| Field | Value |
|-------|--------|
| **Product** | PyTorch Learning Studio — AI-powered PyTorch learning platform |
| **Repo** | `Unified_Pytorch_Stidio` / `pytorch-learning-studio` |
| **Vision** | 13 PyTorch modules, three-tier difficulty, Colab integration, PyTorch-expert AI tutor, spaced repetition, daily tracker, external import |
| **Exercise bank target** | 500–650 exercises across 13 modules |
| **Roadmap** | 6 phases × ~4 weeks (24 weeks total per spec) |

---

## Locked technical decisions

| Decision | Choice | Rationale (short) |
|----------|--------|-------------------|
| Frontend framework | Next.js 14 (App Router) + TypeScript | Spec default; App Router for modules/exercises routing |
| UI | Tailwind CSS + shadcn/ui | Consistent accessible components |
| State | **Zustand** | Spec default for client state |
| Code editor | Monaco Editor | Python syntax + PyTorch autocomplete snippets |
| Charts | Recharts | Analytics dashboard and heatmap |
| Math rendering | MathJax 3.x | LaTeX in problem statements |
| Backend runtime | Python 3.11+ with FastAPI | Spec default; async support for Anthropic API |
| ORM | **SQLAlchemy 2.x** + Alembic | Spec default; Python-native migrations |
| Package manager | **uv** (preferred) | Spec default for backend deps |
| Primary DB | PostgreSQL 16 | Relational model for users, questions, progress |
| Cache / broker | Redis 7 | Sessions, rate limits, Celery broker |
| Background tasks | Celery 5.x | Nightly aggregation, revision scheduler |
| AI provider | **Anthropic** `claude-sonnet-4-20250514` | PyTorch-specialist tutor (spec §9) |
| Spaced repetition | **SM-2 algorithm** | Per-question ease factor and interval (spec §12) |
| Notebook integration | Google Colab + nbviewer | One-click launch and notebook URL import |
| File storage | AWS S3 | Notebook assets, uploads (production) |
| CI/CD | GitHub Actions | Spec default |
| Auth | JWT (register/login/refresh/logout) | Endpoints defined in spec §8 |

---

## Core domain concepts

| Concept | Notes |
|---------|--------|
| **Modules (topics)** | 13 PyTorch modules (Tensors → Lightning); `module_number` 1–13 |
| **Questions** | 6 types: `code_completion`, `debug_model`, `conceptual_mcq`, `build_from_scratch`, `notebook_challenge`, `shape_assertion` |
| **PyTorch fields** | `starter_code`, `expected_output_shape`, `colab_link`, `gpu_required`, `pytorch_version`, `xp_reward` |
| **Test cases** | JSONB input/output; sample vs hidden; shape/dtype assertions |
| **User attempts** | Result: `correct` \| `incorrect` \| `partial` \| `skipped` |
| **User progress** | Per-module: attempted/solved counts by difficulty, completion % |
| **Revision** | SM-2: ease_factor, interval_days, repetition_count, next_review_date |
| **Daily activity** | Per-user per-date; XP earned, modules touched, goal_met, streak |
| **Custom questions** | User imports with `is_shared` community flag |
| **XP system** | +10/+20/+30 by difficulty; −2 per hint; streak and milestone bonuses |

---

## Documentation index

| File | Role |
|------|------|
| `.claude/CLAUDE.md` | Entry point and read order |
| `.claude/rules/CLAUDE.md` | Full technical specification |
| `.claude/SKILLS.md` | Agent skills and workflows |
| `.claude/PLAN.md` | Master plan and success metrics |
| `.claude/PLAN_PHASE.md` | Weekly phases and checkpoints |
| `.claude/TASKS.md` | Phase/sub-task tracker |
| `.claude/specs/stack.md` | Stack and directory layout |
| `.claude/specs/database.md` | Schema summary |
| `.claude/specs/api-design.md` | REST API surface |
| `.claude/specs/frontend-ui.md` | UI pages and components |
| `.claude/specs/ai-chatbot.md` | AI tutor behavior |
| `.claude/specs/deployment.md` | Dev and deploy |

---

## Current phase tracker

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 1 | Foundation | **Complete** | Auth, core APIs, seeds M01–03, Next.js `/modules` + exercise page, Colab stub |
| 2 | Content Expansion | **Complete** | Modules 04–07 (80 Qs), Colab nbformat URLs, ShapeValidator, Anthropic tutor + `/tutor` UI |
| 3 | Analytics & Tracker | **Complete** | Dashboard, heatmap, Celery cron, XP, SM-2 revision |
| 4 | Import & Community | **Complete** | Import APIs, notebook parser, `/import` + `/community` UI, user notes on exercises |
| 5 | Remaining Modules & Polish | **Complete** | M08–13 seeds, bulk_expand to 40/module, `/exercises` search, Ctrl+Enter/Ctrl+H, theme toggle, mobile nav |
| 6 | Production | Not started | AWS ECS, CloudFront, CI/CD, security audit |

**Active focus:** Phase 6 — Production (see `TASKS.md` P6-*)

---

## Open questions / blockers

| ID | Item | Status |
|----|------|--------|
| OQ-1 | Fork strategy from DSA Studio monorepo | **Open** — migrate to `frontend/` + `backend/` layout per spec |
| OQ-2 | Reuse existing DSA Docker Compose vs new compose | **Resolved** — root `docker-compose.yml` for PG16 + Redis7 + FastAPI backend |
| OQ-3 | In-browser PyTorch execution vs Colab-only (Phase 1) | **Resolved** — Colab-first; Judge0 deferred to V2 |
| OQ-4 | Next.js App Router vs migrate from existing Vite SPA | **Open** — spec requires Next.js 14 App Router |

---

## Conventions (agents)

- API base: `/api/v1` as in spec (auth, topics, questions, attempts, progress, tracker, revision, tutor, colab, import)
- Difficulty enum: `basic` | `intermediate` | `advanced`
- Attempt result: `correct` | `incorrect` | `partial` | `skipped`
- SM-2 rating: 0=blackout, 3=hard, 4=good, 5=easy
- Branch convention: `feature/<short-description>` per `TASKS.md` row
- Tutor rate limit: 20 messages/day (free tier)

---

## Changelog (memory)

| Date | Change |
|------|--------|
| 2026-06-03 | Initial PyTorch spec alignment — all `.claude` agent files updated from DSA Studio to PyTorch Learning Studio |
| 2026-06-03 | Spec v1.0 authored in `rules/CLAUDE.md`; Phase 1 not started |
| 2026-06-03 | Phase 1 backend foundation: 11 ORM models, Alembic `001_initial_schema`, docker-compose (PG16/Redis7/FastAPI), `.env`, 13 topics + 19 Module-01 questions seeded, `/health` verified |
| 2026-06-03 | Phase 1 complete: JWT auth, topics/questions/attempts/colab routers, seeds M02–M03 (+M01), Next.js 14 frontend, pytest API suite |
| 2026-06-03 | Phase 2 complete: seeds M04–M07, colab_service (nbformat), tutor_service (Anthropic+mock), Monaco editor, ShapeValidator, `/tutor` + in-exercise panel |
| 2026-06-03 | Phase 3 complete: progress/tracker/revision routers, XP+SM-2 services, Celery beat, dashboard/tracker/revision UI (Recharts) |
| 2026-06-03 | Phase 4 complete: import_service + import_/notes routers, custom-questions CRUD, community browser, import page (4 tabs), UserNotes on exercise page |
| 2026-06-03 | Phase 5 complete: questions_modules_08_13 + bulk_expand seeds, GET /questions/search, /exercises page, HintDrawer + shortcuts, ThemeProvider + AppHeader |
