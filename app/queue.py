import os
import pika
import json
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = "notifications"

def get_connection():
    params = pika.ConnectionParameters(host=RABBITMQ_HOST)
    return pika.BlockingConnection(params)

def publish_notification(notification_data):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(notification_data),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()