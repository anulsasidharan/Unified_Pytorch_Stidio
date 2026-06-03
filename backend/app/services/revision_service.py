"""Revision queue operations."""

from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.question import Question
from app.models.revision import RevisionQueue
from app.services.spaced_repetition import calculate_next_review


async def submit_review(
    db: AsyncSession,
    user_id: uuid.UUID,
    question_id: int,
    rating: int,
) -> dict:
    if rating < 0 or rating > 5:
        raise ValueError("Rating must be between 0 and 5")

    result = await db.execute(
        select(RevisionQueue)
        .where(
            RevisionQueue.user_id == user_id,
            RevisionQueue.question_id == question_id,
        )
        .options(joinedload(RevisionQueue.question).joinedload(Question.topic))
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise LookupError("Question not in revision queue")

    review = calculate_next_review(
        rating=rating,
        ease_factor=float(item.ease_factor),
        interval_days=item.interval_days,
        repetition_count=item.repetition_count,
    )

    item.ease_factor = Decimal(str(review.new_ease_factor))
    item.interval_days = review.new_interval
    item.repetition_count = review.new_repetition_count
    item.next_review_date = review.next_review_date
    item.last_result = "blackout" if rating < 3 else "recalled"

    from datetime import UTC, datetime

    item.last_reviewed_at = datetime.now(UTC)

    return {
        "question_id": question_id,
        "next_review_date": review.next_review_date.isoformat(),
        "interval_days": review.new_interval,
        "ease_factor": review.new_ease_factor,
    }


async def get_revision_stats(db: AsyncSession, user_id: uuid.UUID) -> dict:
    today = date.today()
    total_result = await db.execute(
        select(func.count()).select_from(RevisionQueue).where(RevisionQueue.user_id == user_id)
    )
    due_result = await db.execute(
        select(func.count())
        .select_from(RevisionQueue)
        .where(
            RevisionQueue.user_id == user_id,
            RevisionQueue.next_review_date <= today,
        )
    )
    overdue_result = await db.execute(
        select(func.count())
        .select_from(RevisionQueue)
        .where(
            RevisionQueue.user_id == user_id,
            RevisionQueue.next_review_date < today,
        )
    )
    return {
        "queue_size": total_result.scalar_one(),
        "due_today": due_result.scalar_one(),
        "overdue": overdue_result.scalar_one(),
    }


async def list_due_items(db: AsyncSession, user_id: uuid.UUID) -> list[dict]:
    today = date.today()
    result = await db.execute(
        select(RevisionQueue)
        .where(
            RevisionQueue.user_id == user_id,
            RevisionQueue.next_review_date <= today,
        )
        .options(joinedload(RevisionQueue.question).joinedload(Question.topic))
        .order_by(RevisionQueue.next_review_date.asc())
    )
    items = []
    for row in result.scalars().all():
        q = row.question
        topic = q.topic if q else None
        days_overdue = (today - row.next_review_date).days
        items.append(
            {
                "question_id": row.question_id,
                "title": q.title if q else "",
                "difficulty": q.difficulty if q else "",
                "topic_slug": topic.slug if topic else "",
                "topic_name": topic.name if topic else "",
                "module_number": topic.module_number if topic else 0,
                "next_review_date": row.next_review_date.isoformat(),
                "days_overdue": days_overdue,
                "ease_factor": float(row.ease_factor),
                "interval_days": row.interval_days,
            }
        )
    return items
