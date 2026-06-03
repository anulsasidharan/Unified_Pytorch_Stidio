"""
Bulk-expand exercise bank to TARGET_PER_MODULE per topic (default 40 → ~520 total).
Usage: python -m seeds.bulk_expand
"""

import asyncio

from seeds.loader import append_questions_for_topic, build_exercise
from seeds.topics import TOPICS

TARGET_PER_MODULE = 40

# Per-topic drill templates: (title_suffix, slug_suffix, difficulty, task, starter, solution, tags, qtype)
_DRILL = (
    "Drill {n}",
    "expand-{topic}-{n}",
    "basic",
    "Practice core patterns for this module. Complete the snippet and print the result.",
    "import torch\n# YOUR CODE\nprint('done')",
    "import torch\nx = torch.randn(2, 3)\nprint(x.shape)",
    ["practice", "drill"],
    "code_completion",
)


def _drills_for_topic(slug: str, module_number: int, count: int) -> list[dict]:
    tag_prefix = slug.split("-")[0]
    questions = []
    for i in range(1, count + 1):
        title, slug_s, diff, task, starter, solution, tags, qtype = _DRILL
        questions.append(
            build_exercise(
                title=title.format(n=i) + f" (M{module_number:02d})",
                slug=slug_s.format(topic=slug, n=i),
                difficulty=diff if i <= count // 2 else ("intermediate" if i <= count * 3 // 4 else "advanced"),
                task=f"**{slug}** — {task} Exercise {i} of {count}.",
                starter_code=starter.replace("YOUR CODE", f"# Module {module_number} exercise {i}"),
                solution_code=solution,
                tags=[tag_prefix, *tags],
                question_type=qtype if i % 5 else "shape_assertion",
                expected_output_shape="(2, 3)" if i % 5 == 0 else None,
            )
        )
    return questions


async def expand_topic(slug: str, module_number: int, current: int) -> int:
    needed = max(0, TARGET_PER_MODULE - current)
    if needed == 0:
        print(f"[skip] {slug}: already at {current}+ questions")
        return 0
    drills = _drills_for_topic(slug, module_number, needed)
    label = f"Module {module_number:02d} bulk ({slug})"
    return await append_questions_for_topic(slug, drills, label)


async def get_question_counts() -> dict[str, int]:
    import os

    from dotenv import load_dotenv
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    load_dotenv()
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio",
    )
    engine = create_async_engine(url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    counts: dict[str, int] = {}
    async with async_session() as session:
        for topic in TOPICS:
            tid = (
                await session.execute(
                    text("SELECT id FROM topics WHERE slug = :slug"),
                    {"slug": topic["slug"]},
                )
            ).scalar()
            if tid is None:
                continue
            c = (
                await session.execute(
                    text("SELECT COUNT(*) FROM questions WHERE topic_id = :tid"),
                    {"tid": tid},
                )
            ).scalar()
            counts[topic["slug"]] = c or 0
    await engine.dispose()
    return counts


async def main() -> None:
    counts = await get_question_counts()
    total_added = 0
    for topic in TOPICS:
        slug = topic["slug"]
        current = counts.get(slug, 0)
        total_added += await expand_topic(slug, topic["module_number"], current)
    print(f"Bulk expansion complete (+{total_added} questions, target {TARGET_PER_MODULE}/module)")


if __name__ == "__main__":
    asyncio.run(main())
