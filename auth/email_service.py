import smtplib

from settings import get_settings


class EmailService:
    def __init__(self):
        self._settings = get_settings()

    def send_email(self, from_address: str, to_address: str, message: str):

        smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_obj.starttls()
        sender = self._settings.sender
        password = self._settings.sender_password
        smtp_obj.login(user=sender, password=password)
        try:
            smtp_obj.sendmail(from_addr=from_address, to_addrs=to_address, msg=message)
        except smtplib.SMTPException:
            print('Error')
        finally:
            smtp_obj.quit()
