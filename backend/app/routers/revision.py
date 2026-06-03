"""Spaced repetition revision queue routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.revision import RevisionQueue
from app.models.user import User
from app.schemas.revision import (
    ReviewResultOut,
    ReviewSubmit,
    RevisionDueItem,
    RevisionStats,
)
from app.services import revision_service, xp_service

router = APIRouter(prefix="/revision", tags=["revision"])


@router.get("/due", response_model=list[RevisionDueItem])
async def revision_due(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[RevisionDueItem]:
    items = await revision_service.list_due_items(db, user.id)
    return [RevisionDueItem(**item) for item in items]


@router.get("/stats", response_model=RevisionStats)
async def revision_stats(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> RevisionStats:
    data = await revision_service.get_revision_stats(db, user.id)
    return RevisionStats(**data)


@router.post("/review", response_model=ReviewResultOut)
async def submit_revision_review(
    body: ReviewSubmit,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ReviewResultOut:
    try:
        result = await revision_service.submit_review(
            db, user.id, body.question_id, body.rating
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    xp_bonus = 0
    if body.rating >= 4:
        stats = await revision_service.get_revision_stats(db, user.id)
        if stats["due_today"] == 0:
            xp_bonus = xp_service.REVISION_SESSION_BONUS
            user.total_xp += xp_bonus

    await db.commit()
    await db.refresh(user)

    return ReviewResultOut(**result, xp_bonus=xp_bonus)


@router.delete("/{question_id}", status_code=204)
async def remove_from_revision(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> None:
    await db.execute(
        delete(RevisionQueue).where(
            RevisionQueue.user_id == user.id,
            RevisionQueue.question_id == question_id,
        )
    )
    await db.commit()
