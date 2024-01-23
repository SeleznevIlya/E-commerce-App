from celery import Celery
from celery.schedules import crontab

from src.config import settings

celery_worker = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["src.tasks.service", "src.tasks.scheduled"],
)


celery_worker.conf.beat_schedule = {
    "random_name": {
        "task": "send_message_every_day",
        # "schedule": crontab(minute="25", hour="20")
        "schedule": 10,
        "kwargs": {"email_to": settings.SMTP_USERNAME},
    }
}
