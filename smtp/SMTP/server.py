from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl


from SMTP.config_SMPT import SMTPConfig

import os
from dotenv import load_dotenv

load_dotenv()


def create_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server = smtplib.SMTP_SSL(SMTPConfig.SMTP_host, SMTPConfig.SMTP_port, context=context)
    server.ehlo(SMTPConfig.login)
    server.login(SMTPConfig.login, SMTPConfig.password)
    server.auth_plain()
    return server


def send_email_verification(recipient: str, token: str):
    msg = MIMEMultipart()
    msg['From'] = SMTPConfig.login
    msg['To'] = recipient
    url = os.getenv('URL_USER_HOST', '')
    url += f"/email/verification/?token={token}&email={recipient}"
    html = f"""
    <html>
        <head></head>
        <body>
            <p>Click the link below to verify your email:</p>
            <p><a href="{url}">link verification</a></p>
            <h1>{url}</h1>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))
    server = create_server()
    server.send_message(msg)
    server.quit()
