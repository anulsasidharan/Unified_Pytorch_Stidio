"""Leaderboard — weekly, monthly, and all-time XP rankings."""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import get_json_cached
from app.database import get_db
from app.schemas.leaderboard import LeaderboardOut
from app.services.leaderboard_service import CACHE_TTL, build_leaderboard

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

VALID_PERIODS = {"weekly", "monthly", "all_time"}


@router.get("", response_model=LeaderboardOut)
async def get_leaderboard(
    response: Response,
    period: str = Query("weekly", pattern="^(weekly|monthly|all_time)$"),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> LeaderboardOut:
    if period not in VALID_PERIODS:
        period = "weekly"
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL}"
    cache_key = f"cache:leaderboard:{period}:{limit}"
    data = await get_json_cached(
        cache_key,
        CACHE_TTL,
        lambda: build_leaderboard(db, period=period, limit=limit),
    )
    return LeaderboardOut(**data)
