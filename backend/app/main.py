from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.config import get_settings
from app.core.redis_client import close_redis
from app.routers import (
    attempts,
    auth,
    colab,
    execute,
    import_,
    lint,
    modules,
    notes,
    progress,
    questions,
    revision,
    snippets,
    topics,
    tracker,
    tutor,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await close_redis()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(topics.router)
api_router.include_router(questions.router)
api_router.include_router(attempts.router)
api_router.include_router(colab.router)
api_router.include_router(tutor.router)
api_router.include_router(progress.router)
api_router.include_router(tracker.router)
api_router.include_router(revision.router)
api_router.include_router(import_.router)
api_router.include_router(notes.router)
api_router.include_router(execute.router)
api_router.include_router(lint.router)
api_router.include_router(modules.router)
api_router.include_router(snippets.router)
app.include_router(api_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
