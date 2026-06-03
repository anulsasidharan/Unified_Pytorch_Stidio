# PyTorch Learning Studio

Fork of Unified DSA Studio — AI-powered PyTorch learning platform.

## Quick start (Phase 1)

```powershell
# Full stack (PostgreSQL, Redis, FastAPI, Next.js)
copy .env.example .env
docker compose up -d --build
docker compose logs -f

# Or run services locally:
docker compose up -d postgres redis

# Backend
cd backend
uv venv
uv pip install -e ".[dev]"
copy ..\.env.example ..\.env
alembic upgrade head
python -m seeds.run_phase1
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

- API docs: http://localhost:8000/docs  
- Modules UI: http://localhost:3000/modules  

## Phase 1 deliverables

- JWT auth (`/api/v1/auth/*`)
- Topics & questions APIs
- 60 seed exercises (modules 01–03)
- Colab URL stub (`/api/v1/colab/{id}`)
- Next.js module grid + exercise page

Spec: `.claude/rules/CLAUDE.md`
