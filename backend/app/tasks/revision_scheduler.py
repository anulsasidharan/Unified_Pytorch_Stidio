"""Revision queue refresh scheduler — logs due counts for monitoring."""

from sqlalchemy import func, select

from app.database_sync import get_sync_session
from app.models.revision import RevisionQueue
from app.tasks.celery_app import celery_app


@celery_app.task(name="tasks.refresh_revision_due_counts")
def refresh_revision_due_counts() -> dict:
    """Lightweight task to verify revision queue health (runs with beat)."""
    from datetime import date

    today = date.today()
    session = get_sync_session()
    try:
        due = session.execute(
            select(func.count())
            .select_from(RevisionQueue)
            .where(RevisionQueue.next_review_date <= today)
        ).scalar_one()
        total = session.execute(select(func.count()).select_from(RevisionQueue)).scalar_one()
        return {"due_today": due, "queue_total": total}
    finally:
        session.close()
