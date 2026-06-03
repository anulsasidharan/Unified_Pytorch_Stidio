"""User progress aggregation routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.topic import Topic
from app.models.user import User
from app.schemas.progress import ProgressSummary, TopicProgressDetail
from app.services.analytics_service import build_progress_summary, build_topic_progress

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressSummary)
async def get_progress_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ProgressSummary:
    data = await build_progress_summary(db, user.id)
    return ProgressSummary(**data)


@router.get("/topic/{slug}", response_model=TopicProgressDetail)
async def get_progress_for_topic(
    slug: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TopicProgressDetail:
    result = await db.execute(select(Topic).where(Topic.slug == slug, Topic.is_active.is_(True)))
    topic = result.scalar_one_or_none()
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    data = await build_topic_progress(db, user.id, topic)
    return TopicProgressDetail(**data)
