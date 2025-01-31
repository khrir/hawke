from infra.services.email.smtp_client import SmtpClient
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_client = self.__configure_smtp_client()

    def send(self, to_address, subject, body):
        res = self.smtp_client.sendmail(to_address, subject, body)
        return res

    def __configure_smtp_client(self):
        smtp_server = os.getenv("SMTP_SERVER")
        port = int(os.getenv("SMTP_PORT"))
        username = os.getenv("SMTP_USERNAME")
        password = os.getenv("SMTP_PASSWORD")

        return SmtpClient(smtp_server, port, username, password)
