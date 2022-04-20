import aiosmtplib


class EmailService:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.user = user
        self.password = password
        self.aio_smtp_obj = aiosmtplib.SMTP(hostname=host, port=port, start_tls=True, username=user, password=password)

    async def send_email(self, to_address: str, message: str):
        await self.aio_smtp_obj.connect()
        await self.aio_smtp_obj.sendmail(sender=self.user, recipients=to_address, message=message)
        await self.aio_smtp_obj.quit()
