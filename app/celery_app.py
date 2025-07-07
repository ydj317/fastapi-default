from celery import Celery

celery_app = Celery(
    "fastapi-celery",
    broker="redis://192.168.51.104:6379/0",        # Redis 브로커
    backend="redis://192.168.51.104:6379/1",       # 작업 결과 저장용 (선택)
)

celery_app.conf.task_routes = {
    "app.tasks.*": {"queue": "default"},
}

from app.tasks import user_task