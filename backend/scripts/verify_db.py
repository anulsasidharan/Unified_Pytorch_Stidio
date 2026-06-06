"""Verify Phase 1 database state."""
import asyncio
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
load_dotenv()

EXPECTED_TABLES = {
    "users",
    "topics",
    "questions",
    "solutions",
    "test_cases",
    "user_attempts",
    "user_progress",
    "daily_activity",
    "revision_queue",
    "user_notes",
    "custom_questions",
}


async def main() -> int:
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/python_studio",
    )
    engine = create_async_engine(url)
    ok = True

    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                """
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                ORDER BY table_name
                """
            )
        )
        tables = {row[0] for row in result}
        missing = EXPECTED_TABLES - tables
        extra = tables - EXPECTED_TABLES - {"alembic_version"}

        print("Tables found:", sorted(tables))
        if missing:
            print("MISSING tables:", sorted(missing))
            ok = False
        if extra:
            print("Extra tables:", sorted(extra))

        for name in sorted(EXPECTED_TABLES):
            count = (
                await conn.execute(text(f"SELECT COUNT(*) FROM {name}"))
            ).scalar()
            print(f"  {name}: {count}")

        q_with_sol = (
            await conn.execute(
                text(
                    """
                    SELECT COUNT(DISTINCT q.id)
                    FROM questions q
                    INNER JOIN solutions s ON s.question_id = q.id
                    """
                )
            )
        ).scalar()
        print(f"  questions_with_solutions: {q_with_sol}")

    await engine.dispose()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
