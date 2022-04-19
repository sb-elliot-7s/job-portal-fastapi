import smtplib


class EmailService:
    def __init__(self, host: str, port: int, user: str, password: str):
        self.user = user
        self.password = password
        self.smtp_obj = smtplib.SMTP(host=host, port=port)

    def login(self):
        self.smtp_obj.login(user=self.user, password=self.password)

    def send_email(self, to_address: str, message: str):
        self.smtp_obj.starttls()
        self.login()
        try:
            self.smtp_obj.sendmail(from_addr=self.user, to_addrs=to_address, msg=message)
        except smtplib.SMTPException:
            print('Error')
        finally:
            self.smtp_obj.quit()
