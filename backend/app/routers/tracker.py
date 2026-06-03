"""Daily tracker dashboard routes."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.tracker import ActivityHistoryOut, DashboardOut, HeatmapOut, StreakData
from app.services.analytics_service import (
    build_dashboard,
    build_heatmap,
    get_streak_data,
    list_activity_history,
)

router = APIRouter(prefix="/tracker", tags=["tracker"])


@router.get("/dashboard", response_model=DashboardOut)
async def tracker_dashboard(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> DashboardOut:
    data = await build_dashboard(db, user)
    return DashboardOut(**data)


@router.get("/heatmap", response_model=HeatmapOut)
async def tracker_heatmap(
    weeks: int = Query(52, ge=4, le=52),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> HeatmapOut:
    data = await build_heatmap(db, user.id, weeks=weeks)
    return HeatmapOut(**data)


@router.get("/history", response_model=ActivityHistoryOut)
async def tracker_history(
    page: int = Query(1, ge=1),
    limit: int = Query(30, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ActivityHistoryOut:
    data = await list_activity_history(db, user.id, page=page, limit=limit)
    return ActivityHistoryOut(**data)


@router.get("/streak", response_model=StreakData)
async def tracker_streak(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> StreakData:
    data = await get_streak_data(db, user)
    return StreakData(**data)
