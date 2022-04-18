from celery_app import celery_app
from .email_service import EmailService


@celery_app.task(name='send_to_email')
def send_code_email(from_address: str, to_address: str, message: str):
    email_service = EmailService()
    return email_service.send_email(from_address=from_address, to_address=to_address, message=message)
