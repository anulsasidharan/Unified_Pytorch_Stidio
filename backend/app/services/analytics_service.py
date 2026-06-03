"""Tracker aggregations and dashboard metrics."""

from __future__ import annotations

import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.daily_activity import DailyActivity
from app.models.progress import UserProgress
from app.models.topic import Topic
from app.models.user import User
from app.services.revision_service import get_revision_stats


def _heatmap_level(count: int) -> int:
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    return 3


async def get_streak_data(db: AsyncSession, user: User) -> dict:
    return {
        "current": user.streak_count,
        "longest": user.longest_streak,
        "last_active": user.last_active_date.isoformat() if user.last_active_date else None,
    }


async def build_dashboard(db: AsyncSession, user: User) -> dict:
    today = date.today()
    week_start = today - timedelta(days=6)

    daily_result = await db.execute(
        select(DailyActivity).where(
            DailyActivity.user_id == user.id,
            DailyActivity.activity_date == today,
        )
    )
    today_row = daily_result.scalar_one_or_none()

    week_result = await db.execute(
        select(DailyActivity)
        .where(
            DailyActivity.user_id == user.id,
            DailyActivity.activity_date >= week_start,
            DailyActivity.activity_date <= today,
        )
        .order_by(DailyActivity.activity_date.asc())
    )
    week_rows = week_result.scalars().all()
    week_map = {r.activity_date: r for r in week_rows}

    weekly = []
    xp_this_week = 0
    for i in range(7):
        d = week_start + timedelta(days=i)
        row = week_map.get(d)
        exercises = row.exercises_done if row else 0
        xp = row.xp_earned if row else 0
        xp_this_week += xp
        weekly.append(
            {
                "date": d.isoformat(),
                "exercises_done": exercises,
                "xp_earned": xp,
            }
        )

    revision_stats = await get_revision_stats(db, user.id)

    breakdown_result = await db.execute(
        select(
            UserProgress.basic_solved,
            UserProgress.intermediate_solved,
            UserProgress.advanced_solved,
        ).where(UserProgress.user_id == user.id)
    )
    basic = intermediate = advanced = 0
    for row in breakdown_result.all():
        basic += row[0] or 0
        intermediate += row[1] or 0
        advanced += row[2] or 0

    timeline_result = await db.execute(
        select(DailyActivity.activity_date, DailyActivity.xp_earned)
        .where(DailyActivity.user_id == user.id)
        .order_by(DailyActivity.activity_date.asc())
        .limit(90)
    )
    cumulative = 0
    xp_timeline = []
    for activity_date, xp in timeline_result.all():
        cumulative += xp or 0
        xp_timeline.append(
            {"date": activity_date.isoformat(), "cumulative_xp": cumulative}
        )

    exercises_done = today_row.exercises_done if today_row else 0
    exercises_correct = today_row.exercises_correct if today_row else 0
    xp_today = today_row.xp_earned if today_row else 0
    time_spent = today_row.time_spent_secs if today_row else 0
    goal_met = today_row.goal_met if today_row else False

    return {
        "today": {
            "exercises_done": exercises_done,
            "exercises_correct": exercises_correct,
            "xp_earned": xp_today,
            "time_spent_secs": time_spent,
            "goal": user.daily_goal,
            "goal_met": goal_met,
        },
        "streak": await get_streak_data(db, user),
        "weekly": weekly,
        "xp_this_week": xp_this_week,
        "total_xp": user.total_xp,
        "revision_due_today": revision_stats["due_today"],
        "difficulty_breakdown": {
            "basic": basic,
            "intermediate": intermediate,
            "advanced": advanced,
        },
        "xp_timeline": xp_timeline,
    }


async def build_heatmap(db: AsyncSession, user_id: uuid.UUID, weeks: int = 52) -> dict:
    end = date.today()
    start = end - timedelta(days=weeks * 7 - 1)

    result = await db.execute(
        select(DailyActivity.activity_date, DailyActivity.exercises_done)
        .where(
            DailyActivity.user_id == user_id,
            DailyActivity.activity_date >= start,
            DailyActivity.activity_date <= end,
        )
    )
    counts = {row[0]: row[1] or 0 for row in result.all()}

    cells = []
    current = start
    while current <= end:
        count = counts.get(current, 0)
        cells.append(
            {
                "date": current.isoformat(),
                "count": count,
                "level": _heatmap_level(count),
            }
        )
        current += timedelta(days=1)

    return {
        "cells": cells,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
    }


async def list_activity_history(
    db: AsyncSession,
    user_id: uuid.UUID,
    *,
    page: int = 1,
    limit: int = 30,
) -> dict:
    offset = (page - 1) * limit
    result = await db.execute(
        select(DailyActivity)
        .where(DailyActivity.user_id == user_id)
        .order_by(DailyActivity.activity_date.desc())
        .offset(offset)
        .limit(limit)
    )
    rows = result.scalars().all()
    return {
        "items": [
            {
                "activity_date": r.activity_date.isoformat(),
                "exercises_done": r.exercises_done,
                "exercises_correct": r.exercises_correct,
                "xp_earned": r.xp_earned,
                "time_spent_secs": r.time_spent_secs,
                "goal_met": r.goal_met,
                "streak_day": r.streak_day,
                "modules_touched": r.modules_touched or [],
            }
            for r in rows
        ],
        "page": page,
        "limit": limit,
    }


async def build_progress_summary(db: AsyncSession, user_id: uuid.UUID) -> dict:
    topics_result = await db.execute(
        select(Topic).where(Topic.is_active.is_(True)).order_by(Topic.order_index)
    )
    topics = topics_result.scalars().all()

    progress_result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user_id)
    )
    progress_map = {p.topic_id: p for p in progress_result.scalars().all()}

    modules = []
    total_attempted = 0
    total_solved = 0
    total_questions = 0

    for topic in topics:
        p = progress_map.get(topic.id)
        attempted = p.questions_attempted if p else 0
        solved = p.questions_solved if p else 0
        completion = float(p.completion_pct) if p else 0.0
        total_attempted += attempted
        total_solved += solved
        total_questions += topic.total_questions
        modules.append(
            {
                "topic_id": topic.id,
                "slug": topic.slug,
                "name": topic.name,
                "icon": topic.icon,
                "color": topic.color,
                "module_number": topic.module_number,
                "total_questions": topic.total_questions,
                "questions_attempted": attempted,
                "questions_solved": solved,
                "completion_pct": completion,
                "basic_solved": p.basic_solved if p else 0,
                "intermediate_solved": p.intermediate_solved if p else 0,
                "advanced_solved": p.advanced_solved if p else 0,
            }
        )

    overall_pct = round(100.0 * total_solved / max(total_questions, 1), 2)

    return {
        "modules": modules,
        "totals": {
            "questions_attempted": total_attempted,
            "questions_solved": total_solved,
            "completion_pct": overall_pct,
        },
    }


async def build_topic_progress(
    db: AsyncSession, user_id: uuid.UUID, topic: Topic
) -> dict:
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.topic_id == topic.id,
        )
    )
    p = result.scalar_one_or_none()
    return {
        "topic_id": topic.id,
        "slug": topic.slug,
        "name": topic.name,
        "total_questions": topic.total_questions,
        "questions_attempted": p.questions_attempted if p else 0,
        "questions_solved": p.questions_solved if p else 0,
        "completion_pct": float(p.completion_pct) if p else 0.0,
        "basic_solved": p.basic_solved if p else 0,
        "intermediate_solved": p.intermediate_solved if p else 0,
        "advanced_solved": p.advanced_solved if p else 0,
        "total_time_spent_secs": p.total_time_spent_secs if p else 0,
    }
