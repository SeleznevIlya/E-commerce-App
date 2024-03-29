import logging
import smtplib

from src.config import settings
from src.tasks.celery import celery_worker
from src.tasks.email_templates import (
    create_order_information_template,
    create_user_information_template,
)


@celery_worker.task
def send_message(service: str, *args, **kwargs):
    match service:
        case "order":
            msg_content = create_order_information_template(**kwargs)
        case "user":
            msg_content = create_user_information_template(**kwargs)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
        logging.info(f"send email result: {msg_content}")
