"""Utility helpers for Python Learning Studio seed files."""

from __future__ import annotations

from typing import Any


XP_BY_DIFFICULTY = {
    "basic": 8,
    "intermediate": 18,
    "advanced": 30,
}

TIME_BY_DIFFICULTY = {
    "basic": 3,
    "intermediate": 6,
    "advanced": 10,
}


def build_python_exercise(
    *,
    title: str,
    slug: str,
    difficulty: str,
    problem_statement: str,
    starter_code: str,
    expected_output: str,
    tags: list[str],
    solution_code: str,
    solution_explanation: str = "",
    question_type: str = "code_completion",
    xp_reward: int | None = None,
    time_estimate_mins: int | None = None,
) -> dict[str, Any]:
    """Build a consistently shaped Python exercise payload."""
    if difficulty not in XP_BY_DIFFICULTY:
        raise ValueError(f"Unsupported difficulty: {difficulty}")

    if not slug.startswith("py-"):
        raise ValueError("Question slug must start with 'py-'")

    return {
        "title": title,
        "slug": slug,
        "difficulty": difficulty,
        "question_type": question_type,
        "problem_statement": problem_statement,
        "starter_code": starter_code,
        "expected_output": expected_output,
        "tags": tags,
        "xp_reward": xp_reward if xp_reward is not None else XP_BY_DIFFICULTY[difficulty],
        "time_estimate_mins": (
            time_estimate_mins if time_estimate_mins is not None else TIME_BY_DIFFICULTY[difficulty]
        ),
        "solutions": [
            {
                "title": "Solution",
                "code": solution_code,
                "explanation": solution_explanation,
                "is_optimal": True,
            }
        ],
    }
