"""Nightly daily activity aggregation cron task (00:05 UTC)."""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select

from app.database_sync import get_sync_session
from app.models.attempt import UserAttempt
from app.models.daily_activity import DailyActivity
from app.models.user import User
from app.tasks.celery_app import celery_app


@celery_app.task(name="tasks.aggregate_daily_activity")
def aggregate_daily_activity() -> dict:
    """
    Rolls up yesterday's attempts into daily_activity and reconciles streaks.
    Runs at 00:05 UTC for the previous calendar day.
    """
    target = date.today() - timedelta(days=1)
    session = get_sync_session()
    users_updated = 0

    try:
        user_ids = session.execute(
            select(UserAttempt.user_id)
            .where(func.date(UserAttempt.attempted_at) == target)
            .distinct()
        ).scalars().all()

        for user_id in user_ids:
            user = session.get(User, user_id)
            if user is None:
                continue

            stats = session.execute(
                select(
                    func.count(UserAttempt.id),
                    func.count(UserAttempt.id).filter(UserAttempt.result == "correct"),
                    func.coalesce(func.sum(UserAttempt.time_spent_secs), 0),
                ).where(
                    UserAttempt.user_id == user_id,
                    func.date(UserAttempt.attempted_at) == target,
                )
            ).one()

            exercises_done, exercises_correct, time_spent = stats

            row = session.execute(
                select(DailyActivity).where(
                    DailyActivity.user_id == user_id,
                    DailyActivity.activity_date == target,
                )
            ).scalar_one_or_none()

            if row is None:
                row = DailyActivity(user_id=user_id, activity_date=target)
                session.add(row)

            row.exercises_done = max(row.exercises_done, exercises_done or 0)
            row.exercises_correct = max(row.exercises_correct, exercises_correct or 0)
            row.time_spent_secs = max(row.time_spent_secs, int(time_spent or 0))
            row.goal_met = row.exercises_done >= user.daily_goal

            if row.goal_met and user.last_active_date == target:
                row.streak_day = user.streak_count
            elif not row.goal_met and user.last_active_date == target:
                user.streak_count = 0

            users_updated += 1

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return {"date": target.isoformat(), "users_updated": users_updated}
