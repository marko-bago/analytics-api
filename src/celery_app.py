from celery import Celery
from settings import settings

celery_app = Celery("ws_worker", broker=settings.celery_broker_url, backend=settings.celery_backend_url)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)