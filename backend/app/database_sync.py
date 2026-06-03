"""Sync SQLAlchemy session for Celery tasks and scripts."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import get_settings

settings = get_settings()
_engine_kwargs: dict = {"pool_pre_ping": True}
if os.getenv("TESTING"):
    _engine_kwargs["poolclass"] = NullPool

sync_engine = create_engine(settings.sync_database_url, **_engine_kwargs)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


def get_sync_session() -> Session:
    return SyncSessionLocal()
