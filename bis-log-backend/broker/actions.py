import json

from pika.adapters.blocking_connection import BlockingChannel
from broker.config_rabbitMQ import RabbitMQConfig


def put_in_queue(broker: BlockingChannel, email: str, token: str):
    queue_name = RabbitMQConfig.queue
    broker.queue_declare(queue=queue_name)
    message = {
        'email': email,
        'token': token
    }
    message_bytes = json.dumps(message).encode('utf-8')
    broker.basic_publish(exchange='', routing_key=queue_name, body=message_bytes)
    broker.close()
