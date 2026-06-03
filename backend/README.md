# PyTorch Learning Studio — Backend

Python 3.11 · FastAPI · SQLAlchemy 2.x · Alembic · uv

## Setup

```bash
cd backend
uv venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
uv pip install -e ".[dev]"
cp ../.env.example .env
alembic upgrade head
python -m seeds.topics
uvicorn app.main:app --reload --port 8000
```

## Docker (from repo root)

```bash
docker compose up -d
docker compose logs -f backend
```
