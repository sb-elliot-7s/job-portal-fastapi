import faust
from faust import StreamT
from email_service.email_logic import EmailService
from settings import get_settings


class EmailView(faust.Record):
    email: str
    code: str


app = faust.App('email_service', broker='kafka://localhost:9092')

send_email_topic = app.topic('send_email_topic', value_type=EmailView)

email_service = EmailService(user=get_settings().sender,
                             password=get_settings().sender_password,
                             host=get_settings().google_host_smtp,
                             port=587)


@app.agent(send_email_topic)
async def send_email(messages: StreamT[EmailView]):
    async for message in messages:
        print(message)
        await email_service.send_email(to_address=message.email, message=message.code)
