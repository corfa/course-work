import pika
import os
import json
from dotenv import load_dotenv
import logging
from count_words.count_words import get_count_words_from_s3_file


logging.basicConfig(level=logging.INFO) 
load_dotenv()
rabbit_host = os.getenv('RABBIT_HOST', '')
rabbit_port = os.getenv('RABBIT_PORT', '')
rabbit_user = os.getenv('RABBIT_USERNAME','')
rabbit_password = os.getenv('RABBIT_PASSWORD','')




credentials = pika.PlainCredentials(rabbit_user, rabbit_password)

connection_params = pika.ConnectionParameters(rabbit_host, rabbit_port, credentials=credentials) 


connection = pika.BlockingConnection(connection_params)


channel = connection.channel()

channel.queue_declare(queue='file')
def callback(ch, method, properties, body):
        message_dict = json.loads(body.decode('utf-8'))
        patch_s3, id_row = message_dict['patch_s3'], message_dict['row_id']
        get_count_words_from_s3_file(patch_s3,id_row)
   

channel.basic_consume(queue='file', on_message_callback=callback, auto_ack=True)
logging.info("[*] CONSUMER IS START [*]")
channel.start_consuming()