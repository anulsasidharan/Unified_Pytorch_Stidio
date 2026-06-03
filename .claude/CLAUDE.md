# PyTorch Learning Studio — Development Specification (Entry Point)

This file is the **Claude Code CLI entry point** for **PyTorch Learning Studio**. The full product and engineering specification lives in **`.claude/rules/CLAUDE.md`** (v1.0, June 2026).

> **Architecture Origin**: Forked and adapted from Unified DSA Studio. Backend infrastructure, spaced repetition engine, daily tracker, auth, and DB patterns are reused. Domain content, topic taxonomy, question schema extensions, and AI tutor persona are PyTorch-specific.

---

## Project overview

**PyTorch Learning Studio** is a full-stack, AI-powered interactive learning platform for mastering PyTorch — from foundational tensor operations to production model deployment.

| Layer | Choice |
|-------|--------|
| **Frontend** | Next.js 14 (App Router) · TypeScript · Tailwind · shadcn/ui · Zustand · Monaco Editor |
| **Backend** | Python 3.11+ · FastAPI · SQLAlchemy 2 · Alembic · Celery |
| **Database** | PostgreSQL 16 · Redis 7 (cache, sessions, Celery broker) |
| **AI** | Anthropic `claude-sonnet-4-20250514` (PyTorch-expert tutor) |
| **Notebooks** | Google Colab integration · nbviewer · notebook URL import |

---

## Modular specifications

Read these for focused work; defer to **`rules/CLAUDE.md`** when they conflict.

| File | Scope |
|------|--------|
| [rules/CLAUDE.md](rules/CLAUDE.md) | Full spec: features, data model, UI, APIs, roadmap |
| [specs/stack.md](specs/stack.md) | Technology stack and repo layout |
| [specs/database.md](specs/database.md) | PostgreSQL schema and entities |
| [specs/api-design.md](specs/api-design.md) | REST endpoints and contracts |
| [specs/frontend-ui.md](specs/frontend-ui.md) | Pages, components, UX patterns |
| [specs/ai-chatbot.md](specs/ai-chatbot.md) | AI tutor capabilities and guardrails |
| [specs/deployment.md](specs/deployment.md) | Local dev, Docker, CI/CD, production |

---

## Agent operating files

| File | Role |
|------|------|
| [MEMORY.md](MEMORY.md) | Locked decisions, phase status, blockers — **update after milestones** |
| [SKILLS.md](SKILLS.md) | Skill catalog and implementation workflows |
| [PLAN.md](PLAN.md) | North star, pillars, risks, MVP definition |
| [PLAN_PHASE.md](PLAN_PHASE.md) | Phased checklist (6 phases × ~4 weeks) |
| [TASKS.md](TASKS.md) | Granular task tracker with branch convention |

**Read order for implementation:** `MEMORY.md` → `PLAN_PHASE.md` → `rules/CLAUDE.md` (relevant section) → `PLAN.md` if trade-offs arise.

---

## Autonomous development instructions

When implementing or modifying this codebase:

1. **Treat `rules/CLAUDE.md` as scope** — features, schema, and API shapes are defined there unless a PR documents intentional divergence.
2. **Ship vertical slices** — Alembic migration + FastAPI router + Next.js page + tests for the same user-visible capability.
3. **Exercise quality bar** — every bank question needs statement, constraints, starter code, test cases (sample + hidden), progressive hints, and solutions (see spec §10).
4. **Never commit secrets** — API keys, DB URLs, JWT secrets stay in `.env` (gitignored).
5. **Respect difficulty tiers** — `basic` · `intermediate` · `advanced`; spaced repetition uses SM-2 algorithm (spec §12).
6. **Support all question types** — `code_completion`, `debug_model`, `conceptual_mcq`, `build_from_scratch`, `notebook_challenge`, `shape_assertion`.
7. **Update `MEMORY.md` and `TASKS.md`** when completing a phase checkpoint or changing a locked decision.

---

## Success metrics (engineering)

| Area | Target |
|------|--------|
| API latency | P95 < 200ms |
| Code execution | < 5s per submission |
| DB queries | < 100ms typical |
| Uptime | 99.9% production |
| Exercise bank | 500–650 exercises across 13 PyTorch modules |

---

## References

- **Authoritative spec:** `.claude/rules/CLAUDE.md`
- **Based on:** Unified DSA Studio CLAUDE.md v1.0

**Document version:** 1.0 · **Status:** Phase 1 complete — Phase 2 (content expansion) next
