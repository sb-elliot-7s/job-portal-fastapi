import faust

from .email_logic import EmailService
from settings import get_settings
from ..app import app, EmailView

email_service = EmailService(user=get_settings().sender, password=get_settings().sender_password, host=get_settings().google_host_smtp, port=587)

send_email_topic = app.topic('send_email_topic', value_type=EmailView)


@app.agent(send_email_topic)
async def send_email(messages: faust.Stream[EmailView]):
    async for message in messages:
        print(message)
        yield await email_service.send_email(to_address=message.email, message=message.code)
