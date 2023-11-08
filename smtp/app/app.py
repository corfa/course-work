import json
import subprocess

import pika

from app import AppConfig
from celery_tasks.tasks import task_email


class App:
    def __init__(self, config: AppConfig):
        self.config = config
        self.celery_process = subprocess.Popen(['celery', '-A', 'celery_tasks.tasks', 'worker', '--loglevel=INFO'])
        self.connection_rabbit = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.host, port=self.config.port))

    def callback(self, ch, method, properties, body):
        data = json.loads(body.decode('utf-8'))
        task_email.delay(data["email"], data["token"])

    def run(self):
        channel = self.connection_rabbit.channel()

        channel.queue_declare(queue=self.config.queue)
        channel.basic_consume(queue=self.config.queue, on_message_callback=self.callback, auto_ack=True)
        try:
            channel.start_consuming()
        except:
            pass
        finally:
            self.celery_process.terminate()
