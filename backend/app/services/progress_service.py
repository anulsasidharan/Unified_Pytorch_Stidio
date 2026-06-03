"""User progress, daily activity, and attempt side-effects."""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attempt import UserAttempt
from app.models.daily_activity import DailyActivity
from app.models.progress import UserProgress
from app.models.question import Question
from app.models.revision import RevisionQueue
from app.models.topic import Topic
from app.models.user import User
from app.services import xp_service


async def _count_prior_attempts(
    db: AsyncSession,
    user_id: uuid.UUID,
    question_id: int,
    *,
    correct_only: bool = False,
) -> int:
    q = select(func.count()).select_from(UserAttempt).where(
        UserAttempt.user_id == user_id,
        UserAttempt.question_id == question_id,
    )
    if correct_only:
        q = q.where(UserAttempt.result == "correct")
    result = await db.execute(q)
    return result.scalar_one()


async def _get_or_create_progress(
    db: AsyncSession, user_id: uuid.UUID, topic_id: int
) -> UserProgress:
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.topic_id == topic_id,
        )
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = UserProgress(user_id=user_id, topic_id=topic_id)
        db.add(progress)
        await db.flush()
    return progress


async def _get_or_create_daily(
    db: AsyncSession, user_id: uuid.UUID, activity_date: date
) -> DailyActivity:
    result = await db.execute(
        select(DailyActivity).where(
            DailyActivity.user_id == user_id,
            DailyActivity.activity_date == activity_date,
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        row = DailyActivity(user_id=user_id, activity_date=activity_date)
        db.add(row)
        await db.flush()
    return row


async def _add_to_revision_queue(
    db: AsyncSession, user_id: uuid.UUID, question_id: int
) -> None:
    result = await db.execute(
        select(RevisionQueue).where(
            RevisionQueue.user_id == user_id,
            RevisionQueue.question_id == question_id,
        )
    )
    existing = result.scalar_one_or_none()
    today = date.today()
    if existing is None:
        db.add(
            RevisionQueue(
                user_id=user_id,
                question_id=question_id,
                next_review_date=today + timedelta(days=1),
                interval_days=1,
                repetition_count=0,
            )
        )
    else:
        existing.next_review_date = today + timedelta(days=1)
        existing.interval_days = 1
        existing.last_result = "correct"


async def _update_streak(
    db: AsyncSession,
    user: User,
    daily: DailyActivity,
    *,
    goal_just_met: bool,
) -> int:
    """Update streak when daily goal is met; return bonus XP from milestones."""
    old_streak = user.streak_count
    today = date.today()
    if goal_just_met and not daily.goal_met:
        yesterday = today - timedelta(days=1)
        y_result = await db.execute(
            select(DailyActivity).where(
                DailyActivity.user_id == user.id,
                DailyActivity.activity_date == yesterday,
            )
        )
        yesterday_row = y_result.scalar_one_or_none()
        if yesterday_row and yesterday_row.goal_met:
            user.streak_count += 1
        else:
            user.streak_count = 1
        daily.goal_met = True
        daily.streak_day = user.streak_count
        user.last_active_date = today
        if user.streak_count > user.longest_streak:
            user.longest_streak = user.streak_count
    elif user.last_active_date != today:
        user.last_active_date = today
    return xp_service.streak_milestone_bonus(old_streak, user.streak_count)


async def process_attempt_submission(
    db: AsyncSession,
    user: User,
    question: Question,
    *,
    result: str,
    hints_used: int = 0,
    time_spent_secs: int = 0,
) -> dict:
    """
    Update progress, daily activity, XP, and revision queue after an attempt.
    Call before commit; returns xp_earned and flags for the API response.
    """
    today = date.today()
    topic_result = await db.execute(select(Topic).where(Topic.id == question.topic_id))
    topic = topic_result.scalar_one()

    prior_total = await _count_prior_attempts(db, user.id, question.id)
    prior_correct = await _count_prior_attempts(db, user.id, question.id, correct_only=True)

    progress = await _get_or_create_progress(db, user.id, question.topic_id)
    old_completion = float(progress.completion_pct or 0)
    daily = await _get_or_create_daily(db, user.id, today)

    xp_earned = 0
    added_to_revision = False
    bonuses: list[str] = []

    daily.exercises_done += 1
    if result == "correct":
        daily.exercises_correct += 1
    daily.time_spent_secs += time_spent_secs

    modules = list(daily.modules_touched or [])
    if topic.slug not in modules:
        modules.append(topic.slug)
    daily.modules_touched = modules

    is_first_attempt = prior_total == 0
    is_first_correct = result == "correct" and prior_correct == 0

    if is_first_attempt:
        progress.questions_attempted += 1
        progress.last_attempted_at = datetime.now(UTC)

    if is_first_correct:
        progress.questions_solved += 1
        if question.difficulty == "basic":
            progress.basic_solved += 1
        elif question.difficulty == "intermediate":
            progress.intermediate_solved += 1
        elif question.difficulty == "advanced":
            progress.advanced_solved += 1

        total_q = max(topic.total_questions, 1)
        progress.completion_pct = Decimal(
            str(round(100.0 * progress.questions_solved / total_q, 2))
        )

        base = xp_service.base_xp_for_difficulty(question.difficulty, question.xp_reward)
        penalty = xp_service.hint_penalty(hints_used)
        xp_earned = max(0, base - penalty)
        daily.xp_earned += xp_earned
        user.total_xp += xp_earned

        milestone = xp_service.module_complete_bonus(old_completion, progress.completion_pct)
        if milestone:
            xp_earned += milestone
            user.total_xp += milestone
            daily.xp_earned += milestone
            bonuses.append("module_complete")

        await _add_to_revision_queue(db, user.id, question.id)
        added_to_revision = True

    goal_before = daily.goal_met
    if daily.exercises_done >= user.daily_goal and not daily.goal_met:
        xp_earned += xp_service.DAILY_GOAL_BONUS
        user.total_xp += xp_service.DAILY_GOAL_BONUS
        daily.xp_earned += xp_service.DAILY_GOAL_BONUS
        bonuses.append("daily_goal")

    streak_bonus = await _update_streak(
        db,
        user,
        daily,
        goal_just_met=daily.exercises_done >= user.daily_goal and not goal_before,
    )
    if streak_bonus:
        xp_earned += streak_bonus
        user.total_xp += streak_bonus
        daily.xp_earned += streak_bonus
        bonuses.append("streak_milestone")

    return {
        "xp_earned": xp_earned,
        "added_to_revision": added_to_revision,
        "bonuses": bonuses,
    }
