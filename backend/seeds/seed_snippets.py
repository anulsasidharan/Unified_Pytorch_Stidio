"""Seed starter snippet library from backend/data/snippets.json (idempotent).

Usage:
    python -m seeds.seed_snippets
"""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/python_studio",
)

SNIPPETS_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "snippets.json")


async def seed_snippets() -> int:
    if not os.path.isfile(SNIPPETS_JSON):
        print(f"[error] Missing snippets file: {SNIPPETS_JSON}")
        return 0

    with open(SNIPPETS_JSON, encoding="utf-8") as fh:
        snippets: list[dict] = json.load(fh)

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    inserted = 0

    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM snippets"))
        existing = result.scalar() or 0
        if existing > 0:
            print(f"[skip] Snippets table already has {existing} rows. Skipping.")
            await engine.dispose()
            return 0

        slug_to_topic_id: dict[str, int] = {}
        topic_rows = await session.execute(
            text("SELECT id, slug FROM topics WHERE is_active = TRUE")
        )
        for row in topic_rows.fetchall():
            slug_to_topic_id[row.slug] = row.id

        for snip in snippets:
            topic_slug = snip.get("topic_slug")
            module_id = slug_to_topic_id.get(topic_slug) if topic_slug else None
            await session.execute(
                text("""
                    INSERT INTO snippets (
                        title, slug, description, code, module_id,
                        tags, difficulty, is_featured
                    ) VALUES (
                        :title, :slug, :description, :code, :module_id,
                        :tags, :difficulty, :is_featured
                    )
                """),
                {
                    "title": snip["title"],
                    "slug": snip["slug"],
                    "description": snip.get("description"),
                    "code": snip["code"],
                    "module_id": module_id,
                    "tags": snip.get("tags", []),
                    "difficulty": snip.get("difficulty", "basic"),
                    "is_featured": snip.get("is_featured", False),
                },
            )
            inserted += 1

        await session.commit()

    await engine.dispose()
    print(f"[ok] Seeded {inserted} snippets")
    return inserted


async def main() -> None:
    await seed_snippets()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
