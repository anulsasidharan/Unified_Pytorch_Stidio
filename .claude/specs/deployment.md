# Deployment & Operations — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §3 Infrastructure, §17 Environment Variables, §18 Development Commands, and Phase 6*

---

## Local development

```bash
# Backend setup (using uv)
cd backend
uv venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
alembic upgrade head
python -m seeds.topics
python -m seeds.questions_tensors

# Run backend
uvicorn app.main:app --reload --port 8000

# Run Celery (separate terminals)
celery -A app.tasks.celery_app worker --loglevel=info
celery -A app.tasks.celery_app beat --loglevel=info

# Frontend
cd frontend
npm install
npm run dev                            # starts on :3000

# Full stack via Docker
docker-compose up -d                   # postgres + redis + backend + frontend
docker-compose logs -f backend
```

| Service | Port |
|---------|------|
| Frontend (Next.js) | 3000 |
| Backend (FastAPI) | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |

Use `.env.example` at repo root and in `backend/`.

---

## Docker services

| Container | Role |
|-----------|------|
| `pytorch-frontend` | Next.js production build |
| `pytorch-backend` | FastAPI + Uvicorn |
| `pytorch-celery` | Celery worker + beat |
| `postgres` | PostgreSQL 16 |
| `redis` | Cache + Celery broker |

Production compose: `docker-compose.prod.yml`

---

## CI/CD (GitHub Actions)

**On pull request:**

- ruff check + format (backend)  
- pytest (backend)  
- ESLint + typecheck (frontend)  
- Build frontend and backend Docker images  

**On main:**

- Push Docker images to registry  
- Deploy to staging (ECS Fargate)  
- Playwright smoke on staging  

---

## Environments

| Env | Purpose |
|-----|---------|
| `development` | Local compose |
| `staging` | Full stack, anonymized seed data |
| `production` | AWS ECS Fargate, managed PostgreSQL, CloudFront CDN |

---

## Secrets management

| Secret | Storage |
|--------|---------|
| `DATABASE_URL` | Platform secret manager |
| `SECRET_KEY` | Rotatable JWT secret |
| `ANTHROPIC_API_KEY` | Never in frontend bundle |
| `AWS_S3_BUCKET` credentials | Backend only |
| `REDIS_URL`, `CELERY_BROKER_URL` | Backend only |

Full env var list: spec §17.

---

## Database operations

- Automated daily backups (managed PostgreSQL)  
- Alembic migration run before new API revision deploy  
- Connection pooling via SQLAlchemy async pool settings  

---

## Monitoring & SLOs

| Metric | Target |
|--------|--------|
| API P95 latency | < 200ms |
| Submission processing | < 5s |
| Uptime | 99.9% |
| Error rate | Alert if > 1% 5xx over 5m |
| Tutor response time | < 10s P95 |

Tools: CloudWatch (AWS) or Prometheus + Grafana.

---

## Logging

- Structured JSON logs from FastAPI  
- `requestId` on every request  
- Do not log: passwords, JWT, full user code blobs at INFO (use DEBUG gated)  
- Log tutor token usage at INFO for cost tracking  

---

## Runbooks (minimum)

1. **Celery backlog** — scale worker replicas  
2. **DB connection exhaustion** — check pool size, slow queries  
3. **Anthropic outage** — degrade tutor to static DB hints; show retry message  
4. **Failed Alembic migration** — rollback procedure documented per release  
5. **Colab URL generation failure** — fall back to stored `colab_link` or nbviewer  

---

## Cloud deployment (Phase 6)

- **Compute:** AWS ECS Fargate (backend + Celery)  
- **Frontend:** S3 + CloudFront CDN  
- **Database:** RDS PostgreSQL 16  
- **Cache:** ElastiCache Redis 7  
- **Assets:** S3 bucket for notebook uploads  

Record chosen provider details in `MEMORY.md` when decided.

---

## Testing commands

```bash
# Backend
pytest backend/tests/ -v
ruff check backend/
ruff format backend/

# Frontend
cd frontend && npm run lint
cd frontend && npm run test

# Load tests (Phase 6)
k6 run tests/load/api-smoke.js
```
