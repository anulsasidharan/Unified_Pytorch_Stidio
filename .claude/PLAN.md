# PLAN.md — PyTorch Learning Studio

High-level execution plan aligned with **`.claude/rules/CLAUDE.md` v1.0**. Granular phases and checklists live in **`PLAN_PHASE.md`**; day-to-day tasks in **`TASKS.md`**.

---

## 1. North star

Deliver a **comprehensive, AI-powered PyTorch learning platform** where practitioners progress from tensor fundamentals to production deployment through:

- Structured 13-module curriculum with three difficulty tiers  
- Runnable Colab notebook challenges embedded in exercises  
- PyTorch-expert AI tutor for debugging, autograd explanation, and architecture review  
- Persistent progress, XP system, spaced repetition (SM-2), and daily streaks  
- Custom exercise import (manual, CSV, JSON, notebook URL)  

**Primary measurable outcome:** sustained daily practice (streak + goal completion) with measurable module mastery and revision adherence.

---

## 2. Strategic pillars

| Pillar | Outcome |
|--------|---------|
| **Structured curriculum** | 13 PyTorch modules from Tensors to Lightning, curated sequences |
| **Quality content** | 500–650 exercises with starter code, test cases, hints, solutions |
| **Colab integration** | One-click notebook launch; auto-generate notebooks when link absent |
| **Shape validation** | Built-in tensor shape/dtype assertion for `shape_assertion` exercises |
| **Retention** | SM-2 spaced repetition with ease factor and adaptive intervals |
| **Insight** | Daily tracker, GitHub-style heatmap, XP timeline, module progress rings |
| **AI augmentation** | Anthropic tutor — debug code, explain autograd, review architectures |
| **Extensibility** | Manual, CSV, JSON, notebook URL import into user question bank |

---

## 3. Workstreams (parallel after foundation)

1. **Platform core** — `frontend/` + `backend/` scaffold, PostgreSQL, Redis, JWT auth, OpenAPI  
2. **Content model** — 13 modules, PyTorch question schema, test cases, solutions, seeds  
3. **Exercise arena** — Monaco editor, shape validator, Colab launcher, submissions  
4. **Progress & analytics** — Progress tables, daily activity, XP, dashboards  
5. **Revision** — SM-2 algorithm, due today, review rating flow  
6. **Import pipeline** — Manual, CSV, JSON, notebook URL import  
7. **AI tutor** — Anthropic integration, PyTorch system prompt, exercise context injection  
8. **Quality & launch** — E2E tests, CI/CD, AWS deployment, monitoring  

---

## 4. Phase mapping (executive)

| Phase | Weeks (spec) | Scope summary |
|-------|----------------|---------------|
| **1 — Foundation** | 1–4 | Fork setup, Alembic schema, seed Modules 01–03, basic UI |
| **2 — Content Expansion** | 5–8 | Modules 04–07, ColabLauncher, ShapeValidator, AI Tutor |
| **3 — Analytics & Tracker** | 9–12 | Dashboard, heatmap, Celery cron, XP, SM-2 revision |
| **4 — Import & Community** | 13–16 | Import system, community questions, user notes |
| **5 — Remaining Modules & Polish** | 17–20 | Modules 08–13, 500+ exercises, search, dark mode |
| **6 — Production** | 21–24 | AWS ECS, CloudFront, CI/CD, security audit |

Detail: **`PLAN_PHASE.md`**.

---

## 5. Dependencies & sequencing rules

1. **Auth + users** before any personalized progress or imports.  
2. **Topics + questions schema** before exercise UI or submissions.  
3. **FastAPI routers + SQLAlchemy models** before frontend API client.  
4. **User progress + attempts** before analytics and revision scheduling.  
5. **Revision queue (SM-2)** after solve path updates attempts.  
6. **AI tutor endpoints** after core question and attempt APIs exist (context).  
7. **Colab service** before notebook_challenge exercise type is usable.  
8. **Celery beat** before nightly aggregation and revision refresh.  

---

## 6. Risk register (engineering-facing)

| Risk | Mitigation |
|------|------------|
| PyTorch GPU exercises on CPU-only machines | `gpu_required` flag; Colab fallback for GPU exercises |
| AI gives full solutions too early | PyTorch tutor prompt + hint XP cost (−2 per hint) |
| Exercise bank size | Phase 1 seed 60 questions; bulk import in Phase 4 |
| Colab URL generation failures | Store `colab_link` on question; nbviewer fallback |
| Editor bundle size | Lazy-load Monaco; code-split exercise route |
| Streak timezone bugs | Store UTC dates; Celery aggregation at 00:05 UTC |
| SM-2 complexity | Port reference implementation from spec §12 verbatim |

---

## 7. Definition of "MVP done" (engineering)

A learner can:

- Register/login and browse 13 PyTorch modules with progress rings  
- Open an exercise, write Python in Monaco, submit for grading  
- Launch Colab for notebook challenges  
- See solutions after 1 attempt; use progressive hints (−2 XP each)  
- View dashboard: today's summary, streak, basic module progress  
- Have attempts and progress persisted in PostgreSQL  

**Not required for MVP:** full 500-exercise bank, in-browser PyTorch execution, mobile app, V2 live coding (see spec §19).

---

## 8. Success metrics (from spec)

| Category | Examples |
|----------|----------|
| Engagement | DAU, session duration, exercises/day, streak rate |
| Learning | Solved count, module completion %, difficulty progression |
| System | API < 200ms P95, submission < 5s, 99.9% uptime |
| Satisfaction | NPS, retention, tutor usage, Colab launch rate |

---

## 9. Future enhancements (out of initial plan)

V2: in-browser PyTorch execution (Judge0), video explanations, leaderboards, study groups  
V3: paper-to-exercise pipeline, interview mode, certifications, mobile app, multi-framework studios  

Track in product backlog; do not implement unless `PLAN_PHASE.md` is explicitly extended.


## ---

Then for each subsequent session, use this pattern:
Session 2 — API Routers:
Read .claude/CLAUDE.md (Section 8) and .claude/TASKS.md.
Backend foundation is complete (docker, models, migrations, seeds).
Next: Build the API routers for auth, topics, questions, and attempts
exactly as defined in Section 8. Use JWT auth from Section 17 config.


---
Session 3 — Frontend Skeleton:
Read .claude/CLAUDE.md (Sections 4 and 11) and .claude/TASKS.md.
Backend and API are complete. Next: Scaffold the Next.js 14 frontend
with the pages and components defined in Section 4 and Section 11.
Start with: /modules page and /modules/[slug]/[id] exercise page only.

---

Session 4 — AI Tutor:
Read .claude/CLAUDE.md (Section 9) and .claude/TASKS.md.
Next: Implement the AI Tutor using the exact system prompt in Section 9
and the Anthropic API. Wire it to the /tutor/chat endpoint from Section 8.

---