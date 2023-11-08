import os
from dotenv import load_dotenv

load_dotenv()


class RabbitMQConfig:
    host = os.getenv('HOST_rabbitMQ', '')
    port = os.getenv('PORT_rabbitMQ', '')
    queue = os.getenv('QUEUE_NAME', '')
