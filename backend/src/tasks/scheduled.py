import smtplib
from pydantic import EmailStr

from src.config import settings
from src.tasks.email_templates import send_test_schedule_message
from src.tasks.celery import celery_worker



@celery_worker.task(name="send_message_every_day")
def send_message_every_day(email_to: EmailStr):
        
    msg_content = send_test_schedule_message(email_to)
        
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg_content)
