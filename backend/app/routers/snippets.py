"""Snippet library routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/snippets", tags=["snippets"])


class SnippetOut(BaseModel):
    id: int
    title: str
    slug: str | None
    description: str | None
    code: str
    module_id: int | None
    tags: list[str] | None
    difficulty: str | None
    is_featured: bool


class SnippetCreate(BaseModel):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str | None = None
    code: str
    module_id: int | None = None
    tags: list[str] | None = None
    difficulty: str | None = None
    is_featured: bool = False


def _row_to_snippet(row) -> SnippetOut:
    return SnippetOut(
        id=row.id,
        title=row.title,
        slug=row.slug,
        description=row.description,
        code=row.code,
        module_id=row.module_id,
        tags=list(row.tags) if row.tags else None,
        difficulty=row.difficulty,
        is_featured=bool(row.is_featured),
    )


@router.get("", response_model=list[SnippetOut])
async def list_snippets(
    module_id: int | None = Query(default=None),
    tag: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> list[SnippetOut]:
    query = "SELECT * FROM snippets WHERE 1=1"
    params: dict = {}
    if module_id is not None:
        query += " AND module_id = :module_id"
        params["module_id"] = module_id
    if tag:
        query += " AND :tag = ANY(tags)"
        params["tag"] = tag
    query += " ORDER BY title"

    try:
        result = await db.execute(text(query), params)
        return [_row_to_snippet(row) for row in result.fetchall()]
    except Exception:
        return []


@router.get("/featured", response_model=list[SnippetOut])
async def featured_snippets(db: AsyncSession = Depends(get_db)) -> list[SnippetOut]:
    try:
        result = await db.execute(
            text("SELECT * FROM snippets WHERE is_featured = TRUE ORDER BY title LIMIT 20")
        )
        return [_row_to_snippet(row) for row in result.fetchall()]
    except Exception:
        return []


@router.get("/{slug}", response_model=SnippetOut)
async def get_snippet(slug: str, db: AsyncSession = Depends(get_db)) -> SnippetOut:
    try:
        result = await db.execute(
            text("SELECT * FROM snippets WHERE slug = :slug"),
            {"slug": slug},
        )
        row = result.fetchone()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Snippets table not available",
        ) from exc

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Snippet not found")
    return _row_to_snippet(row)


@router.post("", response_model=SnippetOut, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    body: SnippetCreate,
    db: AsyncSession = Depends(get_db),
) -> SnippetOut:
    try:
        result = await db.execute(
            text("""
                INSERT INTO snippets (
                    title, slug, description, code, module_id, tags, difficulty, is_featured
                ) VALUES (
                    :title, :slug, :description, :code, :module_id, :tags, :difficulty, :is_featured
                )
                RETURNING *
            """),
            {
                "title": body.title,
                "slug": body.slug,
                "description": body.description,
                "code": body.code,
                "module_id": body.module_id,
                "tags": body.tags,
                "difficulty": body.difficulty,
                "is_featured": body.is_featured,
            },
        )
        await db.commit()
        row = result.fetchone()
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not create snippet — run migrations first",
        ) from exc

    return _row_to_snippet(row)
