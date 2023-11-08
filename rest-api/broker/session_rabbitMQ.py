import pika
from broker.config_rabbitMQ import RabbitMQConfig

ConnectionBroker = pika.BlockingConnection(pika.ConnectionParameters(RabbitMQConfig.host, RabbitMQConfig.port))

