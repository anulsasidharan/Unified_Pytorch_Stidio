"""End-of-module project specs and grading."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project_submission import ProjectSubmission
from app.models.topic import Topic
from app.services.linter import lint_code
from app.services.sandbox import run_python_sandbox

# Mirrors frontend lib/module-meta.ts mini_project strings
MODULE_PROJECTS: dict[str, dict] = {
    "python-basics": {
        "title": "Hello World+",
        "description": "CLI tool that greets the user by name with timestamp",
        "requirements": ["Accept name via input()", "Print greeting with ISO timestamp"],
    },
    "variables-types": {
        "title": "Type Inspector",
        "description": "CLI that reports types and sizes of user inputs",
        "requirements": ["Use type()", "Report sys.getsizeof() for values"],
    },
    "strings": {
        "title": "Text Formatter",
        "description": "Normalize and summarize multi-line user text",
        "requirements": ["Strip whitespace", "Count words and lines"],
    },
    "control-flow": {
        "title": "Grade Calculator",
        "description": "Classify scores with match-case and validation",
        "requirements": ["Validate score range 0-100", "Use match-case for letter grades"],
    },
    "loops": {
        "title": "Number Guessing Game",
        "description": "Loop-driven CLI with attempt tracking",
        "requirements": ["Random target", "Track attempts", "Loop until correct"],
    },
    "lists-tuples": {
        "title": "Todo List CLI",
        "description": "CRUD operations on an in-memory task list",
        "requirements": ["Add, list, complete, and remove tasks"],
    },
    "dicts-sets": {
        "title": "Word Frequency Counter",
        "description": "Count tokens from stdin or a file",
        "requirements": ["Use dict/Counter", "Sort by frequency"],
    },
    "functions": {
        "title": "Calculator Library",
        "description": "Reusable pure functions with tests",
        "requirements": ["Separate functions for +, -, *, /", "Handle division by zero"],
    },
    "oop": {
        "title": "Bank Account Model",
        "description": "OOP design with validation and transaction history",
        "requirements": ["Deposit/withdraw methods", "Prevent overdraft"],
    },
    "dunder-methods": {
        "title": "Vector2D Class",
        "description": "Arithmetic dunder methods with repr/str",
        "requirements": ["__add__, __sub__, __mul__", "__repr__ and __str__"],
    },
    "modules-packages": {
        "title": "Mini Package",
        "description": "Split code into a reusable installable package",
        "requirements": ["__init__.py", "Relative imports", "__all__"],
    },
    "file-io": {
        "title": "JSON Config Manager",
        "description": "Load, validate, and save app settings",
        "requirements": ["Read/write JSON", "Validate required keys"],
    },
    "exceptions": {
        "title": "Robust File Parser",
        "description": "Graceful errors with structured logging",
        "requirements": ["Custom exceptions", "logging module", "try/except/finally"],
    },
    "iterators-generators": {
        "title": "Log Pipeline",
        "description": "Lazy generator chain filtering large files",
        "requirements": ["Generator functions", "Filter/map pipeline"],
    },
    "decorators": {
        "title": "Timing Decorator Suite",
        "description": "Measure and log function runtime",
        "requirements": ["@wraps", "Timing decorator", "Optional args"],
    },
    "functional": {
        "title": "Data Pipeline",
        "description": "Compose small pure functions over records",
        "requirements": ["map/filter/reduce", "Function composition"],
    },
    "comprehensions": {
        "title": "Report Builder",
        "description": "Nested comprehensions over nested JSON",
        "requirements": ["Dict/list comprehensions", "Aggregate stats"],
    },
    "type-hints": {
        "title": "Typed API Client",
        "description": "Fully annotated HTTP wrapper with validation",
        "requirements": ["Type hints on all functions", "Optional/Union types"],
    },
    "testing": {
        "title": "Test Suite",
        "description": "pytest coverage for a small library module",
        "requirements": ["Test functions", "Fixtures or parametrize"],
    },
    "stdlib": {
        "title": "CLI File Stats Tool",
        "description": "pathlib + collections + argparse",
        "requirements": ["argparse CLI", "File size/count stats"],
    },
    "concurrency": {
        "title": "Parallel Downloader",
        "description": "Thread pool fetching URLs safely",
        "requirements": ["ThreadPoolExecutor", "Error handling per URL"],
    },
    "async": {
        "title": "Async URL Fetcher",
        "description": "Concurrent HTTP requests with asyncio",
        "requirements": ["async/await", "asyncio.gather()"],
    },
    "performance": {
        "title": "Benchmark Harness",
        "description": "Compare implementations with timeit",
        "requirements": ["timeit module", "Compare two approaches"],
    },
    "design-patterns": {
        "title": "Plugin System",
        "description": "Strategy + Factory for swappable handlers",
        "requirements": ["Strategy pattern", "Factory for plugins"],
    },
    "data-scripting": {
        "title": "ETL Script",
        "description": "Ingest CSV, validate with Pydantic, export JSON",
        "requirements": ["CSV read", "Validation", "JSON export"],
    },
}


def _default_starter(title: str, description: str) -> str:
    return (
        f"#!/usr/bin/env python3\n"
        f'"""{title} — {description}"""\n\n'
        f"from datetime import datetime\n\n\n"
        f"def main() -> None:\n"
        f"    # TODO: implement the project\n"
        f"    pass\n\n\n"
        f'if __name__ == "__main__":\n'
        f"    main()\n"
    )


def get_project_spec(slug: str, module_name: str) -> dict | None:
    meta = MODULE_PROJECTS.get(slug)
    if meta is None:
        return None
    return {
        "slug": slug,
        "module_name": module_name,
        "title": meta["title"],
        "description": meta["description"],
        "starter_code": _default_starter(meta["title"], meta["description"]),
        "requirements": meta["requirements"],
    }


def grade_project_code(code: str) -> dict:
    """Grade a project submission: run, lint, and score."""
    lint = lint_code(code)
    sandbox = run_python_sandbox(code, time_limit=10.0)
    has_runtime_error = bool(sandbox.stderr.strip())
    code_len = len(code.strip())

    score = lint.score
    if has_runtime_error:
        score = max(0, score - 40)
    if code_len < 30:
        score = max(0, score - 20)

    is_passed = not has_runtime_error and score >= 60 and code_len >= 30

    feedback_parts: list[str] = []
    if has_runtime_error:
        feedback_parts.append(f"Runtime error: {sandbox.stderr.strip()[:200]}")
    if lint.violations:
        feedback_parts.append(f"{len(lint.violations)} PEP 8 violation(s) found.")
    if code_len < 30:
        feedback_parts.append("Submission is too short — flesh out your implementation.")
    if is_passed:
        feedback_parts.append("Project passed! Code runs cleanly with acceptable style.")
    elif not feedback_parts:
        feedback_parts.append("Code runs but needs improvement to pass (score >= 60).")

    return {
        "stdout": sandbox.stdout,
        "stderr": sandbox.stderr,
        "score": score,
        "is_passed": is_passed,
        "pep8_score": lint.score,
        "feedback": " ".join(feedback_parts),
    }


async def get_user_submission(
    db: AsyncSession, user_id: uuid.UUID, topic_id: int
) -> ProjectSubmission | None:
    result = await db.execute(
        select(ProjectSubmission).where(
            ProjectSubmission.user_id == user_id,
            ProjectSubmission.topic_id == topic_id,
        )
    )
    return result.scalar_one_or_none()


async def upsert_submission(
    db: AsyncSession,
    user_id: uuid.UUID,
    topic: Topic,
    code: str,
) -> ProjectSubmission:
    grade = grade_project_code(code)
    existing = await get_user_submission(db, user_id, topic.id)

    if existing:
        existing.code = code
        existing.stdout = grade["stdout"]
        existing.stderr = grade["stderr"]
        existing.score = grade["score"]
        existing.is_passed = grade["is_passed"]
        existing.feedback = grade["feedback"]
        existing.pep8_score = grade["pep8_score"]
        submission = existing
    else:
        submission = ProjectSubmission(
            user_id=user_id,
            topic_id=topic.id,
            code=code,
            stdout=grade["stdout"],
            stderr=grade["stderr"],
            score=grade["score"],
            is_passed=grade["is_passed"],
            feedback=grade["feedback"],
            pep8_score=grade["pep8_score"],
        )
        db.add(submission)

    await db.commit()
    await db.refresh(submission)
    return submission
