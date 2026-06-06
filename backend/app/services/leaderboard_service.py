"""Weekly/monthly/all-time XP leaderboard."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.daily_activity import DailyActivity
from app.models.user import User

PERIOD_DAYS = {"weekly": 7, "monthly": 30}
CACHE_TTL = 300


async def build_leaderboard(db: AsyncSession, period: str = "weekly", limit: int = 50) -> dict:
    now = datetime.now(UTC)
    entries: list[dict] = []

    if period == "all_time":
        result = await db.execute(
            select(User.username, User.id, User.total_xp)
            .where(User.is_active.is_(True), User.total_xp > 0)
            .order_by(User.total_xp.desc())
            .limit(limit)
        )
        for rank, row in enumerate(result.all(), start=1):
            entries.append(
                {
                    "rank": rank,
                    "user_id": str(row.id),
                    "username": row.username,
                    "xp": row.total_xp,
                    "exercises_solved": 0,
                }
            )
    else:
        days = PERIOD_DAYS.get(period, 7)
        since = date.today() - timedelta(days=days - 1)
        result = await db.execute(
            select(
                User.username,
                User.id,
                func.coalesce(func.sum(DailyActivity.xp_earned), 0).label("xp"),
                func.coalesce(func.sum(DailyActivity.exercises_correct), 0).label("solved"),
            )
            .join(DailyActivity, DailyActivity.user_id == User.id)
            .where(
                User.is_active.is_(True),
                DailyActivity.activity_date >= since,
            )
            .group_by(User.id, User.username)
            .having(func.sum(DailyActivity.xp_earned) > 0)
            .order_by(func.sum(DailyActivity.xp_earned).desc())
            .limit(limit)
        )
        for rank, row in enumerate(result.all(), start=1):
            entries.append(
                {
                    "rank": rank,
                    "user_id": str(row.id),
                    "username": row.username,
                    "xp": int(row.xp),
                    "exercises_solved": int(row.solved),
                }
            )

    return {
        "period": period,
        "entries": entries,
        "updated_at": now.isoformat(),
    }
