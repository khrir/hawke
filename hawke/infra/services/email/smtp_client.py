import smtplib
from email.mime.text import MIMEText

class SmtpClient:
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def sendmail(self, to_address: str, subject: str, body: str):
        msg = MIMEText(body, 'html', 'utf-8')
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Subject'] = subject

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, to_address, msg.as_string())
            print(f"E-mail enviado para {to_address}")
            return True
        except Exception as e:
            print(f"Falha ao enviar e-mail: {str(e)}")
            return False