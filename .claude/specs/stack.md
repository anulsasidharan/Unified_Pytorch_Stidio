# Technology Stack — PyTorch Learning Studio

*Extracted from `.claude/rules/CLAUDE.md` §3 Technology Stack & §4 Project Directory Structure*

---

## Layer choices

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Frontend** | Next.js 14 (App Router), TypeScript 5.x | Spec default; file-based routing for modules/exercises |
| **UI** | Tailwind CSS 3.x + shadcn/ui | Accessible components, consistent design |
| **State** | Zustand 4.x | Spec default for client state |
| **Code editor** | Monaco Editor 0.44.x | Python syntax + PyTorch autocomplete snippets |
| **Charts** | Recharts 2.x | Analytics dashboard, heatmap, weekly charts |
| **Math** | MathJax 3.x | LaTeX in problem statements |
| **Syntax display** | react-syntax-highlighter 15.x | Solution code display |
| **Backend** | Python 3.11+, FastAPI 0.111.x | Spec default; async Anthropic API calls |
| **ORM** | SQLAlchemy 2.x + Alembic 1.13.x | Python-native schema, migrations |
| **Validation** | Pydantic v2 | Request/response schemas |
| **Background tasks** | Celery 5.x | Nightly aggregation, revision scheduler |
| **Auth** | python-jose 3.x + passlib 1.7.x | JWT tokens, password hashing |
| **HTTP client** | httpx 0.27.x | Async Anthropic, Colab, notebook fetch |
| **Package manager** | uv (preferred) | Fast Python dependency management |
| **Database** | PostgreSQL 16 | Relational progress and question model |
| **Cache / broker** | Redis 7 | Sessions, rate limits, Celery broker |
| **AI** | Anthropic `claude-sonnet-4-20250514` | PyTorch-expert tutor |
| **Notebooks** | nbformat + Google Colab API | Notebook generation and launch |
| **Storage** | AWS S3 | Notebook assets, uploads (production) |
| **CDN** | CloudFront | Static assets (production) |
| **CI/CD** | GitHub Actions | Lint, test, build, deploy |
| **Deployment** | AWS ECS Fargate | Production (Phase 6) |
| **Testing** | pytest, Playwright | Backend unit/integration, frontend E2E |
| **Linting** | ruff (Python), ESLint (frontend) | Code quality |

---

## Recommended directory structure

```text
pytorch-learning-studio/
├── .claude/                    # Agent specs (this tree)
├── frontend/
│   ├── app/
│   │   ├── (auth)/login/, register/
│   │   ├── dashboard/
│   │   ├── modules/[slug]/[questionId]/
│   │   ├── tracker/, revision/, import/, tutor/, profile/
│   ├── components/
│   │   ├── editor/             # CodeEditor, OutputPanel, ShapeValidator
│   │   ├── question/           # QuestionCard, ColabLauncher, HintDrawer
│   │   ├── tracker/            # StreakCounter, HeatmapCalendar, ProgressRing
│   │   ├── tutor/              # ChatInterface, CodeSuggestion
│   │   └── ui/                 # shadcn components
│   ├── lib/                    # api.ts, auth.ts, utils.ts
│   └── store/                  # Zustand stores
├── backend/
│   ├── app/
│   │   ├── main.py, config.py, database.py
│   │   ├── models/             # SQLAlchemy models
│   │   ├── routers/            # auth, topics, questions, attempts, tutor, colab, import
│   │   ├── services/           # spaced_repetition, tutor, colab, import, analytics
│   │   └── tasks/              # Celery app + cron tasks
│   ├── alembic/versions/
│   ├── seeds/                  # topics.py, questions_*.py
│   └── tests/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

---

## Code execution

**Phase 1–5:** Colab-first — exercises run in Google Colab notebooks  
**V2:** In-browser PyTorch execution via Judge0 or custom sandbox  

Shape/dtype validation runs locally via `ShapeValidator` component for `shape_assertion` exercises.

---

## Environment variables (minimum)

| Variable | Used by |
|----------|---------|
| `DATABASE_URL` | Backend (asyncpg) |
| `REDIS_URL` | Backend cache |
| `CELERY_BROKER_URL` | Celery worker |
| `SECRET_KEY` | JWT auth |
| `ANTHROPIC_API_KEY` | AI tutor |
| `TUTOR_MODEL` | Tutor service (default: claude-sonnet-4-20250514) |
| `TUTOR_DAILY_LIMIT_FREE` | Rate limiting (default: 20) |
| `FRONTEND_URL` | CORS |
| `AWS_S3_BUCKET` | Production asset storage (Phase 6) |
| `COLAB_NOTEBOOK_BASE_URL` | Colab integration |

Full list: spec §17. Never commit real values; use `.env.example`.
