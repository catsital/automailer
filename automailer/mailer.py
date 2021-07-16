import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.utils import COMMASPACE, formatdate, formataddr
from email import encoders
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Optional, List

class Mailer:
    def __init__(
        self,
        host: str,
        port: int,
        sender: str,
        password: Optional[str] = None
    ):
        self.sender = sender
        self.host = host
        self.port = port
        self.server = self.connect(password)

    def connect(self, password: str):
        server = smtplib.SMTP(self.host, self.port)
        server.set_debuglevel(True)
        server.ehlo()
        server.starttls()
        if password: server.login(self.sender, password)
        return server

    def send(
        self,
        subject: str,
        receivers: str,
        cc: List[str],
        bcc: List[str],
        body: Optional[str] = None,
        html: Optional[str] = None,
        img: Optional[str] = None,
        files: List[str]
    ):
        msg = MIMEMultipart('related')
        msg['From'] = formataddr((self.name, self.sender))
        msg['To'] = (',' . join(receivers))
        msg['Cc'] = (',' . join(cc))
        msg['Bcc'] = (',' . join(bcc))
        msg['Subject'] = subject

        msg_content = MIMEMultipart('alternative')
        msg.attach(msg_content)
        msg_content.attach(MIMEText(body, 'plain'))

        if html:
            msg_content.attach(MIMEText(html, 'html'))

        if img:
            fp = open(img, 'rb')
            msg_img = MIMEImage(fp.read())
            fp.close()
            msg_img.add_header('Content-ID', '<image1>')
            msg.attach(msg_img)

        if files:
            for path in files:
                part = MIMEBase('application',"octet-stream")
                with open(path, 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(Path(path).name))
                msg.attach(part)

        recipients = receivers + cc + bcc
        self.server.sendmail(
            self.sender,
            recipients,
            msg.as_string()
        )

    def set_template(self, template_path, file, **kwargs):
        file_loader = FileSystemLoader(template_path)
        env = Environment(loader=file_loader)
        template = env.get_template(file)
        output = template.render(**kwargs)
        return output
