from email.message import EmailMessage
from uuid import UUID
from pydantic import EmailStr

from src.config import settings


def create_order_information_template(
    order_id: UUID, product_dict: dict, email_to: EmailStr
):
    product_name = list(product_dict.values())

    email = EmailMessage()
    email["Subject"] = "Hobby Games"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(
        f"""
			<h1> Заказ № {order_id} </h1>
			Вы заказали следующие позиции:
			<br>{product_name}</br>
			
		""",
        subtype="html",
    )
    return email


def create_user_information_template(user_id: UUID, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Hobby Games"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(
        f"""
			<h1> Спасибо за регистрацию </h1>
			Ваш user_id
			<br>{user_id}</br>
			
		""",
        subtype="html",
    )
    return email


def send_test_schedule_message(email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Hobby Games"
    email["From"] = settings.SMTP_USERNAME
    email["To"] = email_to

    email.set_content(
        f"""
			<h1> Здарова чел </h1>
            Проверяю работу задач по расписанию
		""",
        subtype="html",
    )
    return email
