"""
Deactivate legacy duplicate PyTorch module topics.

Older seeds used short slugs (e.g. loss-metrics, datasets) while the app uses
canonical slugs from seeds.topics.TOPICS (loss-functions, datasets-dataloaders).
Both sets were left active, which duplicated modules 5–13 in the UI.

Usage:
    python -m seeds.dedupe_topics
"""

import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from seeds.topics import TOPICS

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/python_studio",
)
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Superseded PyTorch slugs — canonical Python slugs live in TOPICS
LEGACY_TOPIC_SLUGS = frozenset(
    {
        "tensors",
        "autograd",
        "nn-module",
        "training-loops",
        "loss-functions",
        "loss-metrics",
        "datasets",
        "datasets-dataloaders",
        "cnns",
        "cnns-computer-vision",
        "rnns",
        "rnns-lstms",
        "transformers",
        "transformers-attention",
        "transfer-learning",
        "deployment",
        "model-deployment",
        "gpu-cuda",
        "lightning",
        "pytorch-lightning",
    }
)

CANONICAL_SLUGS = frozenset(t["slug"] for t in TOPICS)


async def deactivate_duplicate_topics() -> int:
    """Deactivate legacy slugs and any extra active row sharing a module_number."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    deactivated = 0

    async with async_session() as session:
        for slug in LEGACY_TOPIC_SLUGS:
            result = await session.execute(
                text(
                    """
                    UPDATE topics
                    SET is_active = FALSE
                    WHERE slug = :slug AND is_active = TRUE
                    RETURNING id
                    """
                ),
                {"slug": slug},
            )
            deactivated += len(result.fetchall())

        # Deactivate any remaining active row whose slug is not in the Python canon
        result = await session.execute(
            text(
                """
                UPDATE topics
                SET is_active = FALSE
                WHERE is_active = TRUE
                  AND slug != ALL(:canonical_slugs)
                RETURNING id
                """
            ),
            {"canonical_slugs": list(CANONICAL_SLUGS)},
        )
        deactivated += len(result.fetchall())

        rows = (
            await session.execute(
                text(
                    """
                    SELECT id, slug, module_number
                    FROM topics
                    WHERE is_active = TRUE
                    ORDER BY module_number, id
                    """
                )
            )
        ).fetchall()

        by_module: dict[int, list[tuple[int, str]]] = {}
        for topic_id, slug, module_number in rows:
            by_module.setdefault(module_number, []).append((topic_id, slug))

        for entries in by_module.values():
            if len(entries) <= 1:
                continue
            canonical = [e for e in entries if e[1] in CANONICAL_SLUGS]
            keep_id = (canonical[0] if canonical else entries[0])[0]
            for topic_id, _slug in entries:
                if topic_id == keep_id:
                    continue
                await session.execute(
                    text("UPDATE topics SET is_active = FALSE WHERE id = :id"),
                    {"id": topic_id},
                )
                deactivated += 1

        await session.commit()

    await engine.dispose()
    return deactivated


if __name__ == "__main__":
    n = asyncio.run(deactivate_duplicate_topics())
    print(f"dedupe_topics: deactivated {n} duplicate topic(s).")
