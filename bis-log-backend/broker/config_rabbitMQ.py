import os
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConfig:
    host = os.getenv('RABBIT_HOST', '')
    port = os.getenv('RABBIT_PORT', '')
    queue = os.getenv('QUEUE_NAME', '')
