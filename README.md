# Unified Python Learning Studio

Interactive, AI-powered platform for learning Python from absolute beginner to professional level.

Forked from Unified PyTorch Studio — backend infrastructure (auth, spaced repetition, daily tracker) is reused; domain content, live code execution, and the AI tutor are Python-specific.

## Features

| Feature | Description |
|---------|-------------|
| **25-module curriculum** | Basic → Intermediate → Advanced tiers per module |
| **Live code execution** | Monaco Editor + Pyodide (Python 3.11 WASM in the browser) |
| **Auto-grader** | Exact / contains / regex output checks |
| **PEP 8 linter** | Real-time style feedback via pycodestyle + pyflakes |
| **AI Python tutor** | GPT-4o / Anthropic tutor with Python-specific system prompt |
| **Snippet library** | Reusable Pythonic patterns (`/snippets`) |
| **Spaced repetition** | SM-2 scheduling for long-term retention |

## Quick start

```powershell
copy .env.example .env
docker compose up -d --build

# Or run locally:
docker compose up -d postgres redis

# Backend
cd backend
uv venv
uv pip install -e ".[dev]"
uv pip install -r requirements.txt
# Apply SQL migration (once):
# psql $DATABASE_URL -f migrations/001_python_studio_schema.sql
alembic upgrade head
python -m seeds.topics
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

- API docs: http://localhost:8000/docs  
- Modules: http://localhost:3000/modules  
- Practice (live editor): http://localhost:3000/practice/{questionId}  
- Snippets: http://localhost:3000/snippets  

## Curriculum (25 modules)

1. Python Basics & Setup · 2. Variables & Types · 3. Strings · 4. Control Flow · 5. Loops  
6. Lists & Tuples · 7. Dicts & Sets · 8. Functions · 9. OOP · 10. Dunder Methods  
11. Modules & Packages · 12. File I/O · 13. Exceptions · 14. Iterators & Generators · 15. Decorators  
16. Functional · 17. Comprehensions · 18. Type Hints · 19. Testing · 20. Standard Library  
21. Concurrency · 22. Async · 23. Performance · 24. Design Patterns · 25. Data & Scripting  

Target exercise bank: **660 questions** across all modules (see spec §12).

## Live code execution

- **Primary:** Pyodide loads from CDN (`NEXT_PUBLIC_PYODIDE_VERSION`, default `0.25.0`) — zero server cost for browser-eligible questions.
- **Fallback:** `POST /api/v1/execute` runs code in an isolated server subprocess (`backend/app/services/sandbox.py`).
- **Grading:** `backend/app/services/grader.py` supports exact, contains, regex, and custom validators.
- **Linting:** `POST /api/v1/lint` — PEP 8 score 0–100.

## Environment

See `.env.example` for `APP_NAME=unified-python-studio`, database, Redis, OpenAI, AWS, and Pyodide settings.

## Specification

Authoritative product spec: `.claude/rules/CLAUDE.md`
