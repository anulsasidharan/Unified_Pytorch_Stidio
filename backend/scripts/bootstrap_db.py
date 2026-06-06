"""Bootstrap dev/staging database for Unified Python Learning Studio.

Runs Alembic migrations, seeds topics (idempotent), deactivates legacy PyTorch
rows, optionally seeds questions, and verifies Phase 1 exit criteria.

Usage (from backend/):
    python scripts/bootstrap_db.py
    python scripts/bootstrap_db.py --no-questions
    python scripts/bootstrap_db.py --skip-migrations

Environment:
    DATABASE_URL — Postgres URL (async or sync; see .env.example)
    SEED_QUESTIONS — if true (default), run Python question seeds after topics
"""

from __future__ import annotations

import argparse
import asyncio
import os
import subprocess
import sys

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_ROOT)

if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

load_dotenv(os.path.join(REPO_ROOT, ".env"))
load_dotenv()

EXPECTED_ACTIVE_TOPICS = 25


def _async_database_url() -> str:
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/python_studio",
    )
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql+psycopg://"):
        return url.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
    return url


def run_migrations() -> None:
    print("=== Running Alembic migrations ===")
    subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=BACKEND_ROOT,
        check=True,
    )


async def seed_topics_and_dedupe() -> tuple[int, int]:
    from seeds.ensure_topics import ensure_topics_and_dedupe

    return await ensure_topics_and_dedupe()


async def seed_questions() -> None:
    from seeds.run_python_seeds import main

    await main()


async def verify_phase1() -> bool:
    engine = create_async_engine(_async_database_url(), echo=False)
    ok = True

    async with engine.connect() as conn:
        version = (
            await conn.execute(text("SELECT version_num FROM alembic_version"))
        ).scalar()
        print(f"  alembic_version: {version}")

        active_count = (
            await conn.execute(
                text("SELECT COUNT(*) FROM topics WHERE is_active = TRUE")
            )
        ).scalar()
        print(f"  active_topics: {active_count}")

        if active_count != EXPECTED_ACTIVE_TOPICS:
            print(
                f"  EXPECTED {EXPECTED_ACTIVE_TOPICS} active topics, got {active_count}"
            )
            ok = False

        dupes = (
            await conn.execute(
                text(
                    """
                    SELECT module_number, COUNT(*) AS n
                    FROM topics
                    WHERE is_active = TRUE
                    GROUP BY module_number
                    HAVING COUNT(*) > 1
                    """
                )
            )
        ).fetchall()
        if dupes:
            print(f"  duplicate active module_numbers: {dupes}")
            ok = False

        legacy = (
            await conn.execute(
                text(
                    """
                    SELECT slug FROM topics
                    WHERE is_active = TRUE
                      AND slug IN (
                        'tensors', 'autograd', 'nn-module', 'training-loops',
                        'loss-functions', 'loss-metrics', 'datasets',
                        'datasets-dataloaders', 'cnns', 'cnns-computer-vision',
                        'rnns', 'rnns-lstms', 'transformers',
                        'transformers-attention', 'transfer-learning',
                        'deployment', 'model-deployment', 'gpu-cuda',
                        'lightning', 'pytorch-lightning'
                      )
                    """
                )
            )
        ).fetchall()
        if legacy:
            print(f"  active legacy PyTorch slugs: {legacy}")
            ok = False

    await engine.dispose()
    return ok


async def main_async(seed_questions_flag: bool) -> int:
    added, removed = await seed_topics_and_dedupe()
    print(f"ensure_topics: {added} topic(s) added, {removed} duplicate(s) deactivated.")

    if seed_questions_flag:
        print("=== Seeding Python questions (modules 01-05) ===")
        await seed_questions()

    print("=== Verifying Phase 1 database state ===")
    if await verify_phase1():
        print("bootstrap_db: OK — 25 active Python modules, no legacy duplicates.")
        return 0

    print("bootstrap_db: FAILED — see messages above.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Python Learning Studio DB")
    parser.add_argument(
        "--skip-migrations",
        action="store_true",
        help="Skip Alembic upgrade (topics/verify only)",
    )
    parser.add_argument(
        "--no-questions",
        action="store_true",
        help="Skip Python question seeds",
    )
    args = parser.parse_args()

    seed_questions_flag = (
        not args.no_questions
        and os.getenv("SEED_QUESTIONS", "true").lower() in ("1", "true", "yes")
    )

    try:
        if not args.skip_migrations:
            run_migrations()
        return asyncio.run(main_async(seed_questions_flag))
    except subprocess.CalledProcessError as exc:
        print(f"bootstrap_db: migration failed (exit {exc.returncode})")
        return exc.returncode or 1


if __name__ == "__main__":
    sys.exit(main())
