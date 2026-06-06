# TASKS.md — Unified Python Learning Studio

> Granular checklist for visible progress.  
> Plan: `PLAN.md` · Phases: `PLAN_PHASE.md` · Spec: `rules/CLAUDE.md` §13

**Branch convention:** `feature/<short-description>`  
**Status:** `✅ Completed` · `❌ Pending`

**Baseline:** Auth, tracker, spaced repetition, import, dashboard, and Colab infrastructure are inherited from Unified PyTorch Studio and remain ✅ unless a Python-specific change is listed below.

---

## Phase 1 — Foundation Fork (Weeks 1–2)

**Goal:** Domain swap PyTorch → Python — seeds, schema, theme, env, tutor prompt.  
**Phase status:** ✅ Completed (10/10 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P1-1 · Rename app references to `unified-python-studio` (config, docker, package names) | `feature/python-rename` | ✅ Completed |
| P1-2 · Replace `backend/seeds/topics.py` with 25 Python modules + level breakdown | `feature/python-topics-seed` | ✅ Completed |
| P1-3 · SQL migration `001_python_studio_schema.sql` + Alembic `002_python_studio_extensions` | `feature/python-schema-migration` | ✅ Completed |
| P1-4 · Update `.env.example` + `config.py` (spec §14) | `feature/python-env` | ✅ Completed |
| P1-5 · Retheme frontend — Python blue `#3776AB` / yellow `#FFD43B` | `feature/python-theme` | ✅ Completed |
| P1-6 · Python tutor system prompt (`backend/app/services/chatbot.py`) | `feature/python-tutor-prompt` | ✅ Completed |
| P1-7 · Update `module-meta.ts` + modules sidebar (25 modules) | `feature/python-module-meta` | ✅ Completed |
| P1-8 · Rewrite `README.md` for Python Learning Studio | `feature/python-readme` | ✅ Completed |
| P1-9 · Apply migration + re-seed topics in dev/staging DB | `feature/python-db-bootstrap` | ✅ Completed |
| P1-10 · Deactivate legacy PyTorch topic rows (`dedupe_topics.py` wired to bootstrap) | `feature/python-topic-dedupe` | ✅ Completed |

**Exit:** DB has 25 Python modules; app branding and theme reflect Python Learning Studio.

> **Note:** `docker-entrypoint.sh` and `backend/scripts/bootstrap_db.py` run Alembic + `ensure_topics` (includes dedupe) + `run_python_seeds` when `SEED_*` flags are true. Non-Docker dev: `cd backend && python scripts/bootstrap_db.py`.

---

## Phase 2 — Live Execution Engine (Weeks 3–4)

**Goal:** Monaco + Pyodide in browser, auto-grader, PEP 8 linter, server sandbox fallback.  
**Phase status:** ✅ Completed (12/12 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P2-1 · `CodeEditor.tsx` — Monaco wrapper (python, vs-dark/light) | `feature/code-editor` | ✅ Completed |
| P2-2 · `pyodide-runner.ts` — CDN load + stdout/stderr capture | `feature/pyodide-runner` | ✅ Completed |
| P2-3 · `RunButton.tsx` + `OutputPane.tsx` components | `feature/run-output-ui` | ✅ Completed |
| P2-4 · `PEP8Badge.tsx` — live lint score + violation list | `feature/pep8-badge` | ✅ Completed |
| P2-5 · `grader.py` — exact / contains / regex / custom modes | `feature/grader-service` | ✅ Completed |
| P2-6 · `linter.py` — pycodestyle + pyflakes (`pycodestyle`, `pyflakes` deps) | `feature/linter-service` | ✅ Completed |
| P2-7 · `sandbox.py` — server-side subprocess fallback | `feature/sandbox-service` | ✅ Completed |
| P2-8 · Routes: `POST /execute`, `POST /execute/batch`, `POST /lint` | `feature/execute-lint-routes` | ✅ Completed |
| P2-9 · `/practice/[id]` page — embed CodeEditor + RunButton + OutputPane | `feature/practice-page` | ✅ Completed |
| P2-10 · Wire practice page to question `expected_output` grading end-to-end | `feature/practice-grading-e2e` | ✅ Completed |
| P2-11 · Persist submissions to `code_submissions` table on run/submit | `feature/code-submissions` | ✅ Completed |
| P2-12 · Add ORM columns: `expected_output_type`, `run_in_browser`, `pep8_required`, etc. | `feature/question-orm-extensions` | ✅ Completed |

**Exit:** User runs Python in browser on `/practice/{id}`; server fallback grades non-Pyodide exercises.

---

## Phase 3 — Content Seeding (Weeks 5–7)

**Goal:** 660 Python questions across 25 modules + starter snippet library (spec §12).  
**Phase status:** ✅ Completed (10/10 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P3-1 · Seed all 25 topic rows via `ensure_topics.py` (idempotent) | `feature/seed-25-topics` | ✅ Completed |
| P3-2 · Module 01–05 questions — Python basics through loops (94 seeded) | `feature/seed-modules-01-05` | ✅ Completed |
| P3-3 · Module 06–10 questions (152) — lists through dunder methods | `feature/seed-modules-06-10` | ✅ Completed |
| P3-4 · Module 11–15 questions (124) — packages through decorators | `feature/seed-modules-11-15` | ✅ Completed |
| P3-5 · Module 16–20 questions (126) — functional through stdlib | `feature/seed-modules-16-20` | ✅ Completed |
| P3-6 · Module 21–25 questions (114) — concurrency through data scripting | `feature/seed-modules-21-25` | ✅ Completed |
| P3-7 · Question JSON format: `starter_code`, `expected_output`, `test_cases`, hints | `feature/python-question-format` | ✅ Completed |
| P3-8 · Seed 100 starter snippets (`snippets` table + `snippets.json`) | `feature/seed-snippets` | ✅ Completed |
| P3-9 · Update lesson content (`lib/lessons/`) for Modules 01–05 | `feature/python-lessons-01-05` | ✅ Completed |
| P3-10 · Update lesson content for Modules 06–25 | `feature/python-lessons-06-25` | ✅ Completed |

**Exit:** All 25 modules have exercises (610 total) + 100 starter snippets; lesson curricula cover all modules via `python-curriculum.ts`.

---

## Phase 4 — Advanced Features (Weeks 8–10)

**Goal:** Projects, snippet library, batch grader UX, `.py` import, module progress API.  
**Phase status:** ✅ Completed (12/12 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P4-1 · End-of-module project spec section on `/modules/[slug]` | `feature/module-project-ui` | ✅ Completed |
| P4-2 · Snippet library browser (`/snippets`) + runnable detail (`/snippets/[slug]`) | `feature/snippets-ui` | ✅ Completed |
| P4-3 · Snippets API — list, featured, detail, create (`/snippets/*`) | `feature/snippets-api` | ✅ Completed |
| P4-4 · `SnippetCard.tsx` — preview, copy, open in editor | `feature/snippet-card` | ✅ Completed |
| P4-5 · Batch grader API (`POST /execute/batch`) | `feature/batch-grader-api` | ✅ Completed |
| P4-6 · Batch grader UI — multi test-case results on practice page | `feature/batch-grader-ui` | ✅ Completed |
| P4-7 · Module progress API — `GET/POST /modules/{slug}/project` | `feature/module-project-api` | ✅ Completed |
| P4-8 · Project submission flow + grading | `feature/project-submission` | ✅ Completed |
| P4-9 · Question import from `.py` files (extend import pipeline) | `feature/py-file-import` | ✅ Completed |
| P4-10 · Colab launcher — point to Python notebooks per question | `feature/python-colab` | ✅ Completed |
| P4-11 · `ModuleProgressRing` component (Basic/Intermediate/Advanced %) | `feature/module-progress-ring` | ✅ Completed |
| P4-12 · Migrate exercise page (`/modules/[slug]/[questionId]`) to Pyodide run flow | `feature/exercise-pyodide-migration` | ✅ Completed |

**Exit:** Snippet library populated; projects submittable; `.py` import works.

---

## Phase 5 — Polish & Launch (Weeks 11–12)

**Goal:** Tutor polish, leaderboard, mobile/SEO, production readiness.  
**Phase status:** ✅ Completed (10/10 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P5-1 · AI tutor — Python prompt wired + offline fallback messages | `feature/python-tutor-live` | ✅ Completed |
| P5-2 · OpenAI GPT-4o tutor path (spec §14 env vars) alongside Anthropic | `feature/openai-tutor` | ✅ Completed |
| P5-3 · Leaderboard activation (`GET /leaderboard` + UI) | `feature/leaderboard` | ✅ Completed |
| P5-4 · Mobile-responsive practice editor + snippet pages | `feature/responsive-practice` | ✅ Completed |
| P5-5 · SEO / OG tags for modules, practice, snippets | `feature/seo-og` | ✅ Completed |
| P5-6 · Settings page — editor theme, Pyodide version preference | `feature/settings-page` | ✅ Completed |
| P5-7 · Analytics labels retheme (PyTorch → Python module names) | `feature/analytics-retheme` | ✅ Completed |
| P5-8 · Remove/replace remaining PyTorch copy in UI and lessons | `feature/pytorch-copy-cleanup` | ✅ Completed |
| P5-9 · `/modules/[slug]/[level]` route — basic/intermediate/advanced question lists | `feature/level-routes` | ✅ Completed |
| P5-10 · Docker Compose production profile + env validation | `feature/docker-prod` | ✅ Completed |

**Exit:** Production-quality UX; no stale PyTorch references in user-facing surfaces.

---

## Phase 6 — Production (Weeks 13–16)

**Goal:** CI/CD, tests, load validation, AWS deployment.  
**Phase status:** ❌ Pending (0/6 tasks complete)

| Task | Branch | Status |
|------|--------|--------|
| P6-1 · pytest — grader, linter, sandbox, execute/lint/snippet routes | `feature/backend-tests-python` | ❌ Pending |
| P6-2 · Playwright E2E — `/practice/{id}` run, `/snippets`, module browse | `feature/e2e-python` | ❌ Pending |
| P6-3 · GitHub Actions CI/CD (ruff, pytest, ESLint, build) | `feature/cicd` | ❌ Pending |
| P6-4 · k6 load tests — `/execute`, `/lint`, topics list | `feature/load-tests` | ❌ Pending |
| P6-5 · AWS ECS Fargate + CloudFront + RDS deploy | `feature/aws-deploy` | ❌ Pending |
| P6-6 · Security audit + runbooks (Pyodide CSP, sandbox isolation) | `feature/security-audit` | ❌ Pending |

**Exit:** CI green on every PR; production deploy passes smoke test.

---

## Inherited baseline (PyTorch Studio — no re-work unless regressed)

**Phase status:** ✅ Completed

| Area | Status |
|------|--------|
| Docker Compose (PostgreSQL, Redis, backend, frontend) | ✅ Completed |
| JWT auth (`/api/v1/auth/*`) | ✅ Completed |
| Topics & questions REST routers | ✅ Completed |
| Dashboard, tracker, heatmap, SM-2 revision | ✅ Completed |
| Import APIs (manual, CSV, JSON, notebook) + UI | ✅ Completed |
| Community questions + user notes | ✅ Completed |
| Dark mode + responsive nav | ✅ Completed |
| Search & filter exercises | ✅ Completed |

---

## Summary

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1 — Foundation Fork | ✅ Completed | 10 / 10 |
| Phase 2 — Live Execution Engine | ✅ Completed | 12 / 12 |
| Phase 3 — Content Seeding | ✅ Completed | 10 / 10 |
| Phase 4 — Advanced Features | ✅ Completed | 12 / 12 |
| Phase 5 — Polish & Launch | ✅ Completed | 10 / 10 |
| Phase 6 — Production | ❌ Pending | 0 / 6 |
| Inherited baseline | ✅ Completed | 8 / 8 |

---

## How to update

1. Mark task ✅ when merged to main development branch.  
2. Update `MEMORY.md` phase tracker when all rows in a phase are ✅.  
3. Add new rows only with matching `PLAN_PHASE.md` and `rules/CLAUDE.md` §13 scope.  
4. When seeding content (Phase 3), note actual question counts in the task row if they differ from spec targets.
