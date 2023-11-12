import os
from dotenv import load_dotenv

from app import AppConfig

load_dotenv()


class CeleryConfig:
    name = os.getenv('Celery_NAME', '')
    RABBIT_USERNAME = os.getenv('RABBIT_USERNAME', '')
    RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD', '')
    RABBIT_HOST = os.getenv('RABBIT_HOST', '')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '')
    url_broker = f'amqp://{RABBIT_USERNAME}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}//'
    # url_broker = f'pyamqp://guest@{AppConfig.host}:{AppConfig.port}//'
