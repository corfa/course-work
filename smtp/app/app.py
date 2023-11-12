import json
import subprocess

import pika

from app import AppConfig
from celery_tasks.tasks import task_email

from dotenv import load_dotenv

load_dotenv()
import os

host = os.getenv('RABBIT_HOST', '')
port = os.getenv('RABBIT_PORT', '')
username = os.getenv('RABBIT_USERNAME', '')  
password = os.getenv('RABBIT_PASSWORD', '')  
node_name = os.getenv('NODE_NAME', '')  


class App:
    def __init__(self, config: AppConfig):
        self.config = config
        self.celery_node_name = node_name

        self.celery_process = subprocess.Popen([
            'celery', '-A', 'celery_tasks.tasks', 'worker',
            '--loglevel=INFO', '-n', self.celery_node_name
        ])

        credentials = pika.PlainCredentials(username, password)
        connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
            heartbeat=1200
        )
        self.connection_rabbit = pika.BlockingConnection(connection_params)

        

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
