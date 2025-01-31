from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailTemplate:
    def __init__(self, from_address, to_address, subject):
        self.from_address = from_address
        self.to_address = to_address
        self.subject = subject

        self.message = MIMEText('', 'html', 'utf-8')

    def set_body(self, html_content):
        self.message.set_payload(html_content)

    def as_string(self):
        return self.message.as_string()
    