import json

from pika.adapters.blocking_connection import BlockingChannel
from broker.config_rabbitMQ import RabbitMQConfig


def put_in_queue(broker: BlockingChannel, patch_s3: str, row_id: int):
    queue_name = RabbitMQConfig.queue
    broker.queue_declare(queue=queue_name)
    message = {
        'patch_s3': patch_s3,
        'row_id': row_id
    }
    message_bytes = json.dumps(message).encode('utf-8')
    broker.basic_publish(exchange='', routing_key=queue_name, body=message_bytes)
    broker.close()
