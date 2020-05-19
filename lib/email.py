import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailServer:
    def __init__(self, domain='localhost', port=1025, email=None, password=None):
        self.domain = domain
        self.port = port

        if email:
            self.email = email

        if password:
            self.password = password

        self.server = smtplib.SMTP(domain, port)

        if domain != 'localhost':
            if not email or not password:
                raise Exception('EmailServer error: Username and password is required')
            self.server = smtplib.SMTP(domain, port)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(email, password)

        self.server.set_debuglevel(True)

    def send_email(self, to_list, subject, body, attachments=None):
        msg = MIMEMultipart()
        msg['To'] = ', '.join(to_list)
        msg['From'] = self.email
        msg['Subject'] = subject

        msg.attach(MIMEText(body))

        if attachments and len(attachments) > 0:
            for file in attachments:
                with open(file, 'rb') as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=basename(file)
                    )

                part['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=basename(file))
                msg.attach(part)

        self.server.sendmail(msg['From'], msg['To'], msg.as_string())

