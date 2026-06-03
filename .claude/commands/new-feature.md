# New feature workflow

Before coding:

1. Read `.claude/MEMORY.md` — confirm phase allows this work
2. Read `.claude/SKILLS.md` § `pytorch-studio-dev` — follow reading order
3. Map the feature to `PLAN_PHASE.md` and add/update a row in `TASKS.md` if missing
4. Identify affected specs: `stack`, `database`, `api-design`, `frontend-ui`, `ai-chatbot`

Implementation:

- Vertical slice: Alembic migration + FastAPI router + Next.js page + tests
- Update `specs/api-design.md` if endpoints change
- Mark `TASKS.md` ✅ when done; update `MEMORY.md` if decisions were locked

Branch: `feature/<short-description>`
