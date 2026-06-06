"""CSV/JSON/notebook URL question import and custom question helpers."""

from __future__ import annotations

import csv
import io
import json
import re
import ast
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import httpx
import nbformat
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.question import CustomQuestion
from app.models.topic import Topic
from app.models.user import User

CSV_MAX_ROWS = 50
CSV_REQUIRED_COLUMNS = {"title", "problem_statement"}
CSV_OPTIONAL_COLUMNS = {
    "topic_slug",
    "difficulty",
    "question_type",
    "starter_code",
    "solution_code",
    "expected_output",
    "tags",
    "colab_link",
    "time_estimate_mins",
}
VALID_DIFFICULTIES = {"basic", "intermediate", "advanced"}
NOTEBOOK_FETCH_TIMEOUT = 30.0


@dataclass
class ParsedQuestion:
    title: str
    topic_slug: str | None
    difficulty: str | None
    problem_statement: str
    solution_code: str | None
    colab_link: str | None
    tags: list[str] | None


@dataclass
class ImportRowResult:
    title: str
    status: str
    question_id: int | None = None
    error: str | None = None


class ImportValidationError(ValueError):
    pass


def _normalize_tags(raw: str | list[str] | None) -> list[str] | None:
    if raw is None:
        return None
    if isinstance(raw, list):
        return [t.strip() for t in raw if t and str(t).strip()]
    return [t.strip() for t in str(raw).split(",") if t.strip()]


def _validate_difficulty(value: str | None) -> str | None:
    if value is None or value == "":
        return None
    lowered = value.strip().lower()
    if lowered not in VALID_DIFFICULTIES:
        raise ImportValidationError(
            f"Invalid difficulty '{value}'. Use basic, intermediate, or advanced."
        )
    return lowered


def parse_csv_content(content: str) -> list[ParsedQuestion]:
    """Parse CSV bulk import (max 50 rows)."""
    reader = csv.DictReader(io.StringIO(content))
    if reader.fieldnames is None:
        raise ImportValidationError("CSV file is empty or missing header row")

    headers = {h.strip().lower() for h in reader.fieldnames if h}
    missing = CSV_REQUIRED_COLUMNS - headers
    if missing:
        raise ImportValidationError(f"CSV missing required columns: {', '.join(sorted(missing))}")

    rows = list(reader)
    if not rows:
        raise ImportValidationError("CSV contains no data rows")
    if len(rows) > CSV_MAX_ROWS:
        raise ImportValidationError(f"CSV exceeds maximum of {CSV_MAX_ROWS} questions per upload")

    parsed: list[ParsedQuestion] = []
    for idx, row in enumerate(rows, start=2):
        title = (row.get("title") or "").strip()
        statement = (row.get("problem_statement") or "").strip()
        if not title or not statement:
            raise ImportValidationError(f"Row {idx}: title and problem_statement are required")

        starter = (row.get("starter_code") or row.get("solution_code") or "").strip() or None
        difficulty = _validate_difficulty(row.get("difficulty"))
        parsed.append(
            ParsedQuestion(
                title=title,
                topic_slug=(row.get("topic_slug") or "").strip() or None,
                difficulty=difficulty,
                problem_statement=statement,
                solution_code=starter,
                colab_link=(row.get("colab_link") or "").strip() or None,
                tags=_normalize_tags(row.get("tags")),
            )
        )
    return parsed


def parse_json_payload(data: dict) -> list[ParsedQuestion]:
    """Parse JSON import format from spec §15."""
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ImportValidationError("JSON must contain a non-empty 'questions' array")
    if len(questions) > CSV_MAX_ROWS:
        raise ImportValidationError(f"JSON exceeds maximum of {CSV_MAX_ROWS} questions")

    parsed: list[ParsedQuestion] = []
    for idx, item in enumerate(questions, start=1):
        if not isinstance(item, dict):
            raise ImportValidationError(f"Question {idx}: must be an object")

        title = (item.get("title") or "").strip()
        statement = (item.get("problem_statement") or "").strip()
        if not title or not statement:
            raise ImportValidationError(f"Question {idx}: title and problem_statement are required")

        starter = item.get("starter_code") or item.get("solution_code")
        difficulty = _validate_difficulty(item.get("difficulty"))
        parsed.append(
            ParsedQuestion(
                title=title,
                topic_slug=(item.get("topic_slug") or "").strip() or None,
                difficulty=difficulty,
                problem_statement=statement,
                solution_code=(starter or "").strip() or None,
                colab_link=(item.get("colab_link") or "").strip() or None,
                tags=_normalize_tags(item.get("tags")),
            )
        )
    return parsed


def _question_dict_to_parsed(item: dict, idx: int) -> ParsedQuestion:
    title = (item.get("title") or "").strip()
    statement = (item.get("problem_statement") or "").strip()
    if not title or not statement:
        raise ImportValidationError(f"Question {idx}: title and problem_statement are required")

    starter = item.get("starter_code") or item.get("solution_code")
    solutions = item.get("solutions") or []
    if not starter and solutions:
        starter = solutions[0].get("code") if isinstance(solutions[0], dict) else None

    difficulty = _validate_difficulty(item.get("difficulty"))
    return ParsedQuestion(
        title=title,
        topic_slug=(item.get("topic_slug") or "").strip() or None,
        difficulty=difficulty,
        problem_statement=statement,
        solution_code=(starter or "").strip() or None,
        colab_link=(item.get("colab_link") or "").strip() or None,
        tags=_normalize_tags(item.get("tags")),
    )


def parse_py_content(content: str) -> list[ParsedQuestion]:
    """Parse a .py file into one or more importable questions.

    Supports:
    1. Bulk seed format: ``QUESTIONS = [{...}, ...]``
    2. Single exercise with comment metadata and string variables
    """
    content = content.strip()
    if not content:
        raise ImportValidationError(".py file is empty")

    # Bulk format: extract QUESTIONS list via AST
    questions_match = re.search(r"^QUESTIONS\s*=\s*\[", content, re.MULTILINE)
    if questions_match:
        try:
            tree = ast.parse(content)
        except SyntaxError as exc:
            raise ImportValidationError(f"Invalid Python syntax: {exc}") from exc

        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "QUESTIONS":
                        try:
                            raw_list = ast.literal_eval(node.value)
                        except (ValueError, SyntaxError) as exc:
                            raise ImportValidationError(
                                "QUESTIONS must be a static list of dicts"
                            ) from exc
                        if not isinstance(raw_list, list) or not raw_list:
                            raise ImportValidationError("QUESTIONS must be a non-empty list")
                        if len(raw_list) > CSV_MAX_ROWS:
                            raise ImportValidationError(
                                f".py import exceeds maximum of {CSV_MAX_ROWS} questions"
                            )
                        return [
                            _question_dict_to_parsed(item, idx)
                            for idx, item in enumerate(raw_list, start=1)
                            if isinstance(item, dict)
                        ]

    # Single-question format with # metadata comments
    meta: dict[str, str] = {}
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and ":" in stripped:
            key, _, val = stripped.lstrip("#").partition(":")
            meta[key.strip().lower()] = val.strip()

    title = meta.get("title") or meta.get("question")
    topic_slug = meta.get("topic_slug") or meta.get("topic")
    difficulty = meta.get("difficulty")

    # Extract triple-quoted docstring as problem_statement
    doc_match = re.search(r'^\s*"""(.*?)"""', content, re.DOTALL | re.MULTILINE)
    problem_statement = doc_match.group(1).strip() if doc_match else ""

    # Extract starter_code and expected_output assignments
    starter_match = re.search(
        r"starter_code\s*=\s*(['\"]{3}.*?['\"]{3}|['\"].*?['\"])",
        content,
        re.DOTALL,
    )
    starter_code = None
    if starter_match:
        try:
            starter_code = ast.literal_eval(starter_match.group(1))
        except (ValueError, SyntaxError):
            starter_code = starter_match.group(1).strip("'\"")

    if not title:
        raise ImportValidationError(
            "Single .py import requires '# title: ...' comment or QUESTIONS list"
        )
    if not problem_statement:
        problem_statement = f"Complete the exercise: {title}"

    return [
        ParsedQuestion(
            title=title,
            topic_slug=topic_slug or None,
            difficulty=_validate_difficulty(difficulty),
            problem_statement=problem_statement,
            solution_code=starter_code,
            colab_link=meta.get("colab_link") or None,
            tags=_normalize_tags(meta.get("tags")),
        )
    ]


def resolve_notebook_fetch_url(url: str) -> str:
    """Convert Colab/nbviewer/GitHub URLs to a fetchable raw .ipynb URL."""
    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower()
    path = parsed.path or ""

    if "nbviewer.org" in host:
        if "/url/" in url:
            return url.split("/url/", 1)[1]
        if "/github/" in path:
            github_path = path.split("/github/", 1)[1]
            return f"https://raw.githubusercontent.com/{github_path.replace('/blob/', '/', 1)}"
        raise ImportValidationError("Invalid nbviewer URL format")

    if "raw.githubusercontent.com" in host:
        return url

    if "github.com" in host and "/blob/" in path:
        return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/", 1)

    if "gist.github.com" in host:
        gist_id = path.strip("/").split("/")[0]
        return f"https://gist.githubusercontent.com/{gist_id}/raw/notebook.ipynb"

    if "gist.githubusercontent.com" in host:
        return url

    if "colab.research.google.com" in host:
        match = re.search(r"/drive/([a-zA-Z0-9_-]+)", path)
        if match:
            file_id = match.group(1)
            return (
                f"https://drive.google.com/uc?export=download&id={file_id}"
            )
        raise ImportValidationError(
            "Colab URLs must include /drive/<file_id>. "
            "Export the notebook to GitHub or use nbviewer for direct import."
        )

    if url.endswith(".ipynb") or "jupyter" in host:
        return url

    raise ImportValidationError(
        "Unsupported notebook URL. Use nbviewer, GitHub raw .ipynb, or Colab drive links."
    )


def extract_notebook_fields(nb_json: dict, fallback_title: str | None = None) -> ParsedQuestion:
    """Extract problem statement and starter code from notebook JSON."""
    nb = nbformat.from_dict(nb_json)
    markdown_parts: list[str] = []
    first_code: str | None = None
    title = fallback_title

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            source = cell.source if isinstance(cell.source, str) else "".join(cell.source)
            if title is None and source.startswith("#"):
                first_line = source.split("\n", 1)[0].lstrip("# ").strip()
                if first_line:
                    title = first_line
            markdown_parts.append(source)
        elif cell.cell_type == "code" and first_code is None:
            first_code = cell.source if isinstance(cell.source, str) else "".join(cell.source)

    problem_statement = "\n\n".join(markdown_parts).strip()
    if not problem_statement:
        problem_statement = "Imported notebook challenge. Complete the exercises in the starter code."

    if not title:
        title = "Imported Notebook Challenge"

    return ParsedQuestion(
        title=title,
        topic_slug=None,
        difficulty="intermediate",
        problem_statement=problem_statement,
        solution_code=first_code,
        colab_link=None,
        tags=["notebook-challenge", "imported"],
    )


async def fetch_notebook_json(url: str) -> dict:
    """Download and parse notebook JSON from URL."""
    fetch_url = resolve_notebook_fetch_url(url)
    async with httpx.AsyncClient(timeout=NOTEBOOK_FETCH_TIMEOUT, follow_redirects=True) as client:
        response = await client.get(fetch_url)
        if response.status_code != 200:
            raise ImportValidationError(
                f"Failed to fetch notebook (HTTP {response.status_code}). "
                "Try a direct .ipynb raw URL or nbviewer link."
            )
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise ImportValidationError("Response is not valid notebook JSON") from exc


async def resolve_topic_id(
    db: AsyncSession, topic_slug: str | None
) -> int | None:
    if not topic_slug:
        return None
    result = await db.execute(
        select(Topic.id).where(Topic.slug == topic_slug, Topic.is_active.is_(True))
    )
    topic_id = result.scalar_one_or_none()
    if topic_id is None:
        raise ImportValidationError(f"Unknown topic slug: {topic_slug}")
    return topic_id


async def persist_custom_questions(
    db: AsyncSession,
    user: User,
    items: list[ParsedQuestion],
    import_source: str,
    *,
    is_shared: bool = False,
    colab_link_override: str | None = None,
) -> list[tuple[CustomQuestion, ImportRowResult]]:
    results: list[tuple[CustomQuestion, ImportRowResult]] = []

    for item in items:
        try:
            topic_id = await resolve_topic_id(db, item.topic_slug)
            record = CustomQuestion(
                user_id=user.id,
                topic_id=topic_id,
                title=item.title,
                difficulty=item.difficulty,
                problem_statement=item.problem_statement,
                solution_code=item.solution_code,
                colab_link=colab_link_override or item.colab_link,
                tags=item.tags,
                is_shared=is_shared,
                import_source=import_source,
            )
            db.add(record)
            await db.flush()
            results.append(
                (
                    record,
                    ImportRowResult(title=item.title, status="created", question_id=record.id),
                )
            )
        except ImportValidationError as exc:
            results.append(
                (None, ImportRowResult(title=item.title, status="failed", error=str(exc)))
            )
        except Exception as exc:
            results.append(
                (None, ImportRowResult(title=item.title, status="failed", error=str(exc)))
            )

    await db.commit()
    return results


def custom_question_to_dict(
    q: CustomQuestion, topic_slug: str | None = None, author_username: str | None = None
) -> dict[str, Any]:
    return {
        "id": q.id,
        "title": q.title,
        "topic_id": q.topic_id,
        "topic_slug": topic_slug,
        "difficulty": q.difficulty,
        "problem_statement": q.problem_statement,
        "solution_code": q.solution_code,
        "colab_link": q.colab_link,
        "tags": q.tags,
        "is_shared": q.is_shared,
        "import_source": q.import_source,
        "created_at": q.created_at,
        "author_username": author_username,
    }


async def list_custom_questions(
    db: AsyncSession,
    user: User | None,
    *,
    mine_only: bool = False,
    community_only: bool = False,
) -> list[dict[str, Any]]:
    stmt = select(CustomQuestion).options(
        joinedload(CustomQuestion.user),
    )
    if community_only:
        stmt = stmt.where(CustomQuestion.is_shared.is_(True))
    elif mine_only and user is not None:
        stmt = stmt.where(CustomQuestion.user_id == user.id)
    elif user is not None:
        stmt = stmt.where(
            (CustomQuestion.user_id == user.id) | (CustomQuestion.is_shared.is_(True))
        )
    else:
        stmt = stmt.where(CustomQuestion.is_shared.is_(True))

    stmt = stmt.order_by(CustomQuestion.created_at.desc())
    result = await db.execute(stmt)
    rows = result.scalars().unique().all()

    topic_ids = {r.topic_id for r in rows if r.topic_id}
    slug_map: dict[int, str] = {}
    if topic_ids:
        topics = await db.execute(select(Topic.id, Topic.slug).where(Topic.id.in_(topic_ids)))
        slug_map = {tid: slug for tid, slug in topics.all()}

    return [
        custom_question_to_dict(
            q,
            topic_slug=slug_map.get(q.topic_id) if q.topic_id else None,
            author_username=q.user.username if q.user else None,
        )
        for q in rows
    ]


async def build_import_history(db: AsyncSession, user_id) -> list[dict]:
    """Aggregate custom_questions into import history batches."""
    bucket = func.date_trunc("minute", CustomQuestion.created_at).label("bucket")
    stmt = (
        select(
            CustomQuestion.import_source,
            bucket,
            func.count(CustomQuestion.id).label("cnt"),
            func.min(CustomQuestion.created_at).label("imported_at"),
        )
        .where(
            CustomQuestion.user_id == user_id,
            CustomQuestion.import_source.isnot(None),
        )
        .group_by(CustomQuestion.import_source, bucket)
        .order_by(func.min(CustomQuestion.created_at).desc())
        .limit(50)
    )
    result = await db.execute(stmt)
    entries = []
    for row in result.all():
        source, _bucket, count, imported_at = row
        entries.append(
            {
                "import_source": source or "unknown",
                "imported_at": imported_at,
                "questions_count": count,
                "status": "success" if count > 0 else "failed",
            }
        )
    return entries
