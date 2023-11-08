import os
from dotenv import load_dotenv

from app import AppConfig

load_dotenv()


class CeleryConfig:
    name = os.getenv('Celery_NAME', '')
    url_broker = f'pyamqp://guest@{AppConfig.host}:{AppConfig.port}//'
