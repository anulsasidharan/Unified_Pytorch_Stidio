from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "unified_python_studio",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.timezone = "UTC"
celery_app.conf.include = [
    "app.tasks.nightly_aggregation",
    "app.tasks.revision_scheduler",
]
celery_app.conf.beat_schedule = {
    "nightly-activity-aggregation": {
        "task": "tasks.aggregate_daily_activity",
        "schedule": crontab(hour=0, minute=5),
    },
    "revision-due-refresh": {
        "task": "tasks.refresh_revision_due_counts",
        "schedule": crontab(hour=0, minute=10),
    },
}
