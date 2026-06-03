import asyncio
import os

import pytest

os.environ.setdefault("TESTING", "1")


@pytest.fixture
def api_client():
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def dispose_db_engine():
    yield
    from app.database import engine

    asyncio.run(engine.dispose())
