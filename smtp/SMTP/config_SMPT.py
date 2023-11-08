import os
from dotenv import load_dotenv

load_dotenv()


class SMTPConfig:
    SMTP_host = os.getenv('SMTP_HOST', '')
    SMTP_port = int(os.getenv('SMTP_PORT', ''))
    login = os.getenv('SMTP_LOGIN', '')
    password = os.getenv('SMTP_PASSWORD', '')

