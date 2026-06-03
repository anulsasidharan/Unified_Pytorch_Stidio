from celery import Celery

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "pytorch_learning_studio",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.timezone = "UTC"
