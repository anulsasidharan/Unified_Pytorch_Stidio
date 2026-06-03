"""Shared question seeding utilities."""

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
    "postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio",
)


async def get_topic_id(session: AsyncSession, slug: str) -> int | None:
    result = await session.execute(
        text("SELECT id FROM topics WHERE slug = :slug"),
        {"slug": slug},
    )
    return result.scalar()


async def seed_questions_for_topic(
    topic_slug: str,
    questions: list[dict],
    module_label: str,
) -> int:
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    inserted = 0

    async with async_session() as session:
        topic_id = await get_topic_id(session, topic_slug)
        if topic_id is None:
            print(f"[error] Topic '{topic_slug}' not found. Run: python -m seeds.topics")
            await engine.dispose()
            return 0

        result = await session.execute(
            text("SELECT COUNT(*) FROM questions WHERE topic_id = :tid"),
            {"tid": topic_id},
        )
        if (result.scalar() or 0) > 0:
            print(f"[skip] {module_label}: questions already seeded for '{topic_slug}'. Skipping.")
            await engine.dispose()
            return 0

        for q in questions:
            ins = await session.execute(
                text("""
                    INSERT INTO questions (
                        topic_id, title, slug, difficulty, question_type,
                        problem_statement, constraints, starter_code,
                        expected_output, expected_output_shape,
                        pytorch_version, gpu_required, colab_link,
                        tags, xp_reward, time_estimate_mins,
                        is_published, source
                    ) VALUES (
                        :topic_id, :title, :slug, :difficulty, :question_type,
                        :problem_statement, :constraints, :starter_code,
                        :expected_output, :expected_output_shape,
                        :pytorch_version, :gpu_required, :colab_link,
                        :tags, :xp_reward, :time_estimate_mins,
                        TRUE, 'internal'
                    ) RETURNING id
                """),
                {
                    "topic_id": topic_id,
                    "title": q["title"],
                    "slug": q["slug"],
                    "difficulty": q["difficulty"],
                    "question_type": q["question_type"],
                    "problem_statement": q["problem_statement"],
                    "constraints": q.get("constraints"),
                    "starter_code": q.get("starter_code"),
                    "expected_output": q.get("expected_output"),
                    "expected_output_shape": q.get("expected_output_shape"),
                    "pytorch_version": "2.x",
                    "gpu_required": q.get("gpu_required", False),
                    "colab_link": q.get("colab_link", ""),
                    "tags": q.get("tags", []),
                    "xp_reward": q.get("xp_reward", 10),
                    "time_estimate_mins": q.get("time_estimate_mins", 15),
                },
            )
            question_id = ins.scalar()

            for idx, sol in enumerate(q.get("solutions", [])):
                await session.execute(
                    text("""
                        INSERT INTO solutions (
                            question_id, title, code, explanation,
                            is_optimal, order_index
                        ) VALUES (
                            :question_id, :title, :code, :explanation,
                            :is_optimal, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "title": sol["title"],
                        "code": sol["code"],
                        "explanation": sol.get("explanation", ""),
                        "is_optimal": sol.get("is_optimal", False),
                        "order_index": idx + 1,
                    },
                )

            for idx, tc in enumerate(q.get("test_cases", [])):
                await session.execute(
                    text("""
                        INSERT INTO test_cases (
                            question_id, input_data, expected_output,
                            is_hidden, order_index
                        ) VALUES (
                            :question_id, :input_data, :expected_output,
                            :is_hidden, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "input_data": json.dumps(tc["input_data"]),
                        "expected_output": json.dumps(tc["expected_output"]),
                        "is_hidden": tc.get("is_hidden", False),
                        "order_index": idx + 1,
                    },
                )
            inserted += 1

        await session.execute(
            text("UPDATE topics SET total_questions = :count WHERE id = :tid"),
            {"count": inserted, "tid": topic_id},
        )
        await session.commit()

    await engine.dispose()
    print(f"[ok] Seeded {inserted} questions for {module_label}")
    return inserted


async def append_questions_for_topic(
    topic_slug: str,
    questions: list[dict],
    module_label: str,
) -> int:
    """Insert questions whose slugs are not already present (for bulk expansion)."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    inserted = 0

    async with async_session() as session:
        topic_id = await get_topic_id(session, topic_slug)
        if topic_id is None:
            print(f"[error] Topic '{topic_slug}' not found.")
            await engine.dispose()
            return 0

        result = await session.execute(
            text("SELECT slug FROM questions WHERE topic_id = :tid"),
            {"tid": topic_id},
        )
        existing = {row[0] for row in result.fetchall()}

        for q in questions:
            if q["slug"] in existing:
                continue
            ins = await session.execute(
                text("""
                    INSERT INTO questions (
                        topic_id, title, slug, difficulty, question_type,
                        problem_statement, constraints, starter_code,
                        expected_output, expected_output_shape,
                        pytorch_version, gpu_required, colab_link,
                        tags, xp_reward, time_estimate_mins,
                        is_published, source
                    ) VALUES (
                        :topic_id, :title, :slug, :difficulty, :question_type,
                        :problem_statement, :constraints, :starter_code,
                        :expected_output, :expected_output_shape,
                        :pytorch_version, :gpu_required, :colab_link,
                        :tags, :xp_reward, :time_estimate_mins,
                        TRUE, 'internal'
                    ) RETURNING id
                """),
                {
                    "topic_id": topic_id,
                    "title": q["title"],
                    "slug": q["slug"],
                    "difficulty": q["difficulty"],
                    "question_type": q["question_type"],
                    "problem_statement": q["problem_statement"],
                    "constraints": q.get("constraints"),
                    "starter_code": q.get("starter_code"),
                    "expected_output": q.get("expected_output"),
                    "expected_output_shape": q.get("expected_output_shape"),
                    "pytorch_version": "2.x",
                    "gpu_required": q.get("gpu_required", False),
                    "colab_link": q.get("colab_link", ""),
                    "tags": q.get("tags", []),
                    "xp_reward": q.get("xp_reward", 10),
                    "time_estimate_mins": q.get("time_estimate_mins", 15),
                },
            )
            question_id = ins.scalar()
            existing.add(q["slug"])

            for idx, sol in enumerate(q.get("solutions", [])):
                await session.execute(
                    text("""
                        INSERT INTO solutions (
                            question_id, title, code, explanation,
                            is_optimal, order_index
                        ) VALUES (
                            :question_id, :title, :code, :explanation,
                            :is_optimal, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "title": sol["title"],
                        "code": sol["code"],
                        "explanation": sol.get("explanation", ""),
                        "is_optimal": sol.get("is_optimal", False),
                        "order_index": idx + 1,
                    },
                )

            for idx, tc in enumerate(q.get("test_cases", [])):
                await session.execute(
                    text("""
                        INSERT INTO test_cases (
                            question_id, input_data, expected_output,
                            is_hidden, order_index
                        ) VALUES (
                            :question_id, :input_data, :expected_output,
                            :is_hidden, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "input_data": json.dumps(tc["input_data"]),
                        "expected_output": json.dumps(tc["expected_output"]),
                        "is_hidden": tc.get("is_hidden", False),
                        "order_index": idx + 1,
                    },
                )
            inserted += 1

        count_result = await session.execute(
            text("SELECT COUNT(*) FROM questions WHERE topic_id = :tid"),
            {"tid": topic_id},
        )
        total = count_result.scalar() or 0
        await session.execute(
            text("UPDATE topics SET total_questions = :count WHERE id = :tid"),
            {"count": total, "tid": topic_id},
        )
        await session.commit()

    await engine.dispose()
    if inserted:
        print(f"[ok] Appended {inserted} questions for {module_label} (total now {total})")
    else:
        print(f"[skip] No new questions for {module_label}")
    return inserted


def build_exercise(
    *,
    title: str,
    slug: str,
    difficulty: str,
    task: str,
    starter_code: str,
    solution_code: str,
    tags: list[str],
    question_type: str = "code_completion",
    xp_reward: int | None = None,
    constraints: str | None = None,
    expected_output_shape: str | None = None,
    gpu_required: bool = False,
) -> dict:
    xp = xp_reward or {"basic": 10, "intermediate": 20, "advanced": 30}[difficulty]
    return {
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "question_type": question_type,
        "problem_statement": f"## {title}\n\n{task}",
        "constraints": constraints,
        "starter_code": starter_code,
        "expected_output": None,
        "expected_output_shape": expected_output_shape,
        "gpu_required": gpu_required,
        "colab_link": "",
        "tags": tags,
        "xp_reward": xp,
        "time_estimate_mins": 12,
        "solutions": [
            {
                "title": "Reference Solution",
                "code": solution_code,
                "explanation": "Compare your tensor shapes and dtypes with the reference.",
                "is_optimal": True,
            }
        ],
        "test_cases": [
            {"input_data": {}, "expected_output": {"ok": True}, "is_hidden": False},
        ],
    }
