from celery_app import celery_app
from .email_service import EmailService
from settings import get_settings


@celery_app.task(name='send_to_email')
def send_code_email(to_address: str, message: str):
    email_service = EmailService(user=get_settings().sender,
                                 password=get_settings().sender_password,
                                 host='smtp.gmail.com', port=587)
    return email_service.send_email(to_address=to_address, message=message)
