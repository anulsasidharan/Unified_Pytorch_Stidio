"""Insert any missing topics from topics.TOPICS (idempotent)."""

import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from seeds.dedupe_topics import deactivate_duplicate_topics
from seeds.topics import TOPICS

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/python_studio",
)


async def ensure_all_topics() -> int:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    added = 0

    async with async_session() as session:
        for topic in TOPICS:
            exists = await session.execute(
                text("SELECT id FROM topics WHERE slug = :slug"),
                {"slug": topic["slug"]},
            )
            if exists.scalar() is not None:
                continue
            await session.execute(
                text("""
                    INSERT INTO topics (
                        module_number, name, slug, description,
                        icon, color, order_index, total_questions, is_active
                    ) VALUES (
                        :module_number, :name, :slug, :description,
                        :icon, :color, :order_index, 0, TRUE
                    )
                """),
                topic,
            )
            added += 1
            print(f"[ok] Added topic: {topic['slug']}")
        await session.commit()

    await engine.dispose()
    return added


async def ensure_topics_and_dedupe() -> tuple[int, int]:
    added = await ensure_all_topics()
    removed = await deactivate_duplicate_topics()
    return added, removed


if __name__ == "__main__":
    added, removed = asyncio.run(ensure_topics_and_dedupe())
    print(f"ensure_topics: {added} topic(s) added, {removed} duplicate(s) deactivated.")
