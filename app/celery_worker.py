from celery import Celery
from app.core.settings import settings

my_task = Celery(
    "celery_app",
    broker=settings.celery_broker,
    backend=settings.celery_backend,
)

my_task.autodiscover_tasks(["app.tasks"])


# celery -A app.celery_worker.my_task worker --loglevel=info
# celery -A app.celery_worker.my_task worker --loglevel=info --pool=solo