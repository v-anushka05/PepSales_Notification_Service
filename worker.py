from app.queue import get_connection, QUEUE_NAME
from app.notifier import process_notification
from app.retries import retry_with_backoff
import json

def callback(ch, method, properties, body):
    notification_data = json.loads(body)
    try:
        retry_with_backoff(process_notification, (notification_data,))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process notification {notification_data['id']}: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print(" [*] Worker started! Waiting for messages...")
    channel.start_consuming()