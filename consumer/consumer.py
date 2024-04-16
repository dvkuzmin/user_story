from datetime import datetime, timedelta
import json
import logging

import pika

from serializer import RequestData
from utils import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                               port=5672,
                                                               credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='consumer_handler')
channel.queue_declare(queue='writer')


def callback(ch, method, properties, body):
    # Фиксируем время получения сообщения
    receive_datetime = datetime.now()
    receive_time_str = receive_datetime.time().strftime(format='%H:%M:%S')

    request = body.decode('utf-8')
    request_data = load_data(request)
    if RequestData.is_valid(request_data):
        # Отправляем валидное сообщение в очередь обработчик
        channel.basic_publish(exchange='', routing_key='consumer_handler', body=body)

        request_data['receive_time'] = receive_time_str
        request_data.pop('delay')
        request = json.dumps(request_data)
        body = request.encode()
        # Отправляем данные для записи в очередь записи во второй файл txt
        channel.basic_publish(exchange='', routing_key='writer', body=body)
        return {'asyncAnswer': 'Ok'}

def consumer():
    # Получаем сообщения от клиента из очереди rabbitmq
    while True:
        request = channel.basic_consume(queue='client_consumer', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    consumer()
