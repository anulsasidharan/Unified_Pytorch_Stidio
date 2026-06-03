# TASKS.md — PyTorch Learning Studio

> Granular checklist for visible progress.  
> Plan: `PLAN.md` · Phases: `PLAN_PHASE.md` · Spec: `rules/CLAUDE.md`

**Branch convention:** `feature/<short-description>`  
**Status:** `✅ Completed` · `❌ Pending`

---

## Phase 1 — Foundation

| Task | Branch | Status |
|------|--------|--------|
| P1-1 · Repo fork + `frontend/` + `backend/` scaffold | `feature/repo-scaffold` | ✅ Completed |
| P1-2 · Docker Compose (PostgreSQL 16, Redis 7) | `feature/docker-compose` | ✅ Completed |
| P1-3 · SQLAlchemy models + Alembic migrations (spec §5) | `feature/alembic-schema` | ✅ Completed |
| P1-4 · FastAPI auth (JWT register/login/refresh/me) | `feature/auth-jwt` | ✅ Completed |
| P1-5 · Seed 13 topics + 60 questions (Modules 01–03) | `feature/db-seed` | ✅ Completed (59 in DB if M01=19; re-seed M01 for 60) |
| P1-6 · Topics & questions REST routers | `feature/core-apis` | ✅ Completed |
| P1-7 · Next.js module grid + exercise page | `feature/module-ui` | ✅ Completed |
| P1-8 · Colab endpoint stub | `feature/colab-stub` | ✅ Completed |

---

## Phase 2 — Content Expansion

| Task | Branch | Status |
|------|--------|--------|
| P2-1 · Seed Modules 04–07 questions | `feature/seed-modules-04-07` | ✅ Completed |
| P2-2 · ColabLauncher + colab_service.py | `feature/colab-integration` | ✅ Completed |
| P2-3 · ShapeValidator component | `feature/shape-validator` | ✅ Completed |
| P2-4 · Monaco PyTorch autocomplete snippets | `feature/monaco-snippets` | ✅ Completed |
| P2-5 · Anthropic tutor_service.py | `feature/tutor-service` | ✅ Completed |
| P2-6 · Tutor API + exercise context injection | `feature/tutor-api` | ✅ Completed |
| P2-7 · Tutor UI (`/tutor` + in-exercise panel) | `feature/tutor-ui` | ✅ Completed |

---

## Phase 3 — Analytics & Tracker

| Task | Branch | Status |
|------|--------|--------|
| P3-1 · Progress & tracker APIs | `feature/progress-api` | ✅ Completed |
| P3-2 · XP calculation + awards | `feature/xp-system` | ✅ Completed |
| P3-3 · Celery nightly aggregation task | `feature/celery-aggregation` | ✅ Completed |
| P3-4 · SM-2 spaced repetition service | `feature/sm2-revision` | ✅ Completed |
| P3-5 · Dashboard UI (streak, heatmap, progress rings) | `feature/dashboard-ui` | ✅ Completed |
| P3-6 · Revision queue page + review flow | `feature/revision-ui` | ✅ Completed |

---

## Phase 4 — Import & Community

| Task | Branch | Status |
|------|--------|--------|
| P4-1 · Import APIs (manual, CSV, JSON, notebook) | `feature/import-api` | ✅ Completed |
| P4-2 · Notebook URL import parser | `feature/notebook-import` | ✅ Completed |
| P4-3 · Import page UI (4 tabs) | `feature/import-ui` | ✅ Completed |
| P4-4 · Community questions (`is_shared`) | `feature/community-questions` | ✅ Completed |
| P4-5 · User notes CRUD | `feature/user-notes` | ✅ Completed |

---

## Phase 5 — Remaining Modules & Polish

| Task | Branch | Status |
|------|--------|--------|
| P5-1 · Seed Modules 08–13 questions | `feature/seed-modules-08-13` | ❌ Pending |
| P5-2 · Search & filter across exercises | `feature/search-filter` | ❌ Pending |
| P5-3 · Keyboard shortcuts in editor | `feature/editor-shortcuts` | ❌ Pending |
| P5-4 · Mobile-responsive layout | `feature/responsive` | ❌ Pending |
| P5-5 · Dark mode | `feature/dark-mode` | ❌ Pending |

---

## Phase 6 — Production

| Task | Branch | Status |
|------|--------|--------|
| P6-1 · pytest backend test suite | `feature/backend-tests` | ❌ Pending |
| P6-2 · Playwright E2E (critical paths) | `feature/e2e` | ❌ Pending |
| P6-3 · GitHub Actions CI/CD pipeline | `feature/cicd` | ❌ Pending |
| P6-4 · k6 load tests | `feature/load-tests` | ❌ Pending |
| P6-5 · AWS ECS Fargate + CloudFront deploy | `feature/aws-deploy` | ❌ Pending |
| P6-6 · Security audit + runbooks | `feature/security-audit` | ❌ Pending |

---

## How to update

1. Mark task ✅ when merged to main development branch.  
2. Update `MEMORY.md` phase tracker when all rows in a phase are ✅.  
3. Add new rows only with matching `PLAN_PHASE.md` scope.
