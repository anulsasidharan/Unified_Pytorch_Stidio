# PLAN_PHASE.md — PyTorch Learning Studio

Phased delivery from **`.claude/rules/CLAUDE.md` §16 Implementation Roadmap** (6 phases, ~24 weeks). Tasks are **checklist items** for agents and developers—not fixed calendar dates unless program management assigns them.

**Status key:** Use `TASKS.md` for `✅` / `❌` per sub-task.

---

## Phase 1 — Foundation (Weeks 1–4)

**Goal:** Runnable `frontend/` + `backend/` scaffold, PostgreSQL schema, JWT auth, seed Modules 01–03, basic module grid and exercise page.

### Weeks 1–2: Project setup & infrastructure

- [ ] Fork from DSA Studio, rename repo, establish `frontend/` + `backend/` layout
- [ ] Docker Compose: PostgreSQL 16, Redis 7, backend, frontend
- [ ] FastAPI scaffold: `app/main.py`, config, database, Alembic init
- [ ] SQLAlchemy models for all tables from spec §5
- [ ] Alembic migration: PyTorch-specific question fields (`colab_link`, `expected_output_shape`, `gpu_required`, `pytorch_version`)
- [ ] `.env.example` + gitignore secrets
- [ ] JWT auth: register, login, logout, refresh, `GET/PUT /auth/me`

**Exit:** `docker compose up` + login returns JWT; FastAPI `/docs` green.

### Weeks 3–4: Core content & basic UI

- [ ] Seed 13 topics into `topics` table (`backend/seeds/topics.py`)
- [ ] Seed 60 starter questions across Modules 01–03 (20 per module)
- [ ] REST: topics list/detail, questions list/detail/filter
- [ ] FastAPI routers: auth, topics, questions, attempts (stub)
- [ ] Next.js: module grid (`/modules`) + exercise page (`/modules/[slug]/[questionId]`)
- [ ] Colab endpoint stub (`GET /colab/{question_id}`)

**Exit:** User browses 3 modules and opens an exercise with starter code loaded.

**Deliverable:** Functional app with 3 modules, 60 exercises, Colab links working.

---

## Phase 2 — Content Expansion (Weeks 5–8)

**Goal:** Modules 04–07 content, Colab integration, shape validator, full AI Tutor.

### Weeks 5–6: Content & Colab

- [ ] Seed Modules 04–07 (Training, Loss, DataLoaders, CNNs)
- [ ] Implement `ColabLauncher` component with notebook generation fallback
- [ ] Implement `colab_service.py` (nbformat → base64 Colab URL)
- [ ] Implement `ShapeValidator` component for shape_assertion exercises
- [ ] Monaco editor: PyTorch autocomplete snippets

**Exit:** Colab launch works for notebook_challenge exercises; shape check validates tensor output.

### Weeks 7–8: AI Tutor

- [ ] Anthropic API integration (`tutor_service.py`)
- [ ] PyTorch tutor system prompt (spec §9)
- [ ] `POST /tutor/chat`, `GET/DELETE /tutor/history`, `GET /tutor/usage`
- [ ] Exercise context injection from exercise page
- [ ] Tutor UI (`/tutor` page + in-exercise panel)

**Exit:** User asks tutor to debug shape mismatch; receives PyTorch-specific guidance.

**Deliverable:** 7 modules live, AI tutor working, Colab integration complete.

---

## Phase 3 — Analytics & Tracker (Weeks 9–12)

**Goal:** Full dashboard, heatmap, Celery nightly aggregation, XP system, SM-2 revision.

### Weeks 9–10: Tracker backend

- [ ] Progress APIs: `/progress`, `/progress/topic/{slug}`
- [ ] Tracker APIs: `/tracker/dashboard`, `/tracker/heatmap`, `/tracker/history`, `/tracker/streak`
- [ ] XP calculation and awards (spec §13)
- [ ] Celery app + `nightly_aggregation.py` (00:05 UTC cron)
- [ ] SM-2 implementation in `spaced_repetition.py`

**Exit:** API returns streak, heatmap data, and XP totals.

### Weeks 11–12: Tracker & revision UI

- [ ] Dashboard page: streak banner, today's summary, module progress rings, XP timeline
- [ ] HeatmapCalendar (52-week GitHub-style grid)
- [ ] Revision queue page with SM-2 review flow (`POST /revision/review`)
- [ ] WeeklyChart and ProgressRing components

**Exit:** Dashboard matches spec wireframe intent (§11); revision due today list works.

**Deliverable:** Full tracker + revision system live.

---

## Phase 4 — Import & Community (Weeks 13–16)

**Goal:** Full import pipeline and community question sharing.

### Weeks 13–14: Import backend

- [ ] `POST /import/manual`, `/import/csv`, `/import/json`, `/import/notebook`
- [ ] `GET /import/history`, CRUD on `/custom-questions`
- [ ] Notebook URL import: fetch `.ipynb`, extract statement + starter code
- [ ] CSV/JSON validation per spec §15 formats

**Exit:** User imports 1 exercise via JSON and sees it in practice list.

### Weeks 15–16: Import UI & community

- [ ] Import page: Manual Entry | CSV | JSON | Notebook URL tabs
- [ ] `is_shared` flag + community question browser
- [ ] User notes per exercise (`user_notes` CRUD)
- [ ] Import history table with preview before save

**Exit:** Community-shared custom question visible to other users.

**Deliverable:** Import system complete, community questions visible.

---

## Phase 5 — Remaining Modules & Polish (Weeks 17–20)

**Goal:** Full 13-module content library, search, keyboard shortcuts, responsive + dark mode.

### Weeks 17–18: Content completion

- [ ] Seed Modules 08–13 (RNNs, Transformers, Transfer Learning, Deployment, GPU, Lightning)
- [ ] Reach 500+ total exercises
- [ ] Search & filter across all exercises (title, tags, type, difficulty)

**Exit:** All 13 modules populated with exercises at target counts.

### Weeks 19–20: UX polish

- [ ] Keyboard shortcuts in editor (Ctrl+Enter run, Ctrl+H hints)
- [ ] Mobile-responsive layout
- [ ] Dark mode
- [ ] Performance: lazy routes, Monaco on demand

**Exit:** Full content library with polished UX on desktop and mobile.

**Deliverable:** Full 13-module content library, polished UX.

---

## Phase 6 — Production (Weeks 21–24)

**Goal:** AWS deployment, CI/CD, performance and security validation.

### Weeks 21–22: CI/CD & testing

- [ ] pytest suite for backend (models, services, API routes)
- [ ] Frontend tests (Playwright E2E critical paths)
- [ ] GitHub Actions CI (ruff, pytest, ESLint, build)
- [ ] k6 load tests for API endpoints

**Exit:** CI green on every PR; smoke tests pass on staging.

### Weeks 23–24: Production deploy

- [ ] AWS ECS Fargate deployment
- [ ] CloudFront CDN for frontend
- [ ] Security audit (OWASP top 10)
- [ ] README, API docs (auto-generated from FastAPI `/docs`)
- [ ] Runbook: DB backup, Celery scaling, Anthropic outage fallback

**Exit:** Production deploy passes smoke test; SLO dashboards live.

**Deliverable:** Production-ready deployment on AWS.

---

## Phase gate checklist (before marking phase complete)

1. All `TASKS.md` rows for phase marked ✅  
2. `MEMORY.md` phase row updated  
3. No open **blockers** for next phase in MEMORY  
4. API contract synced with `specs/api-design.md` if changed  
