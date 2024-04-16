import time
from datetime import datetime, timedelta
import json
import logging
import threading

import pika

from utils import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_request(request: dict):
    # Фиксируем время прихода сообщения, ожидаем время обработки, фиксируем время обработки, отправляем в очередь записи первого файла txt
    credentials = pika.PlainCredentials('user', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                                   port=5672,
                                                                   credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue='handler_writer')
    receive_datetime = datetime.now()
    receive_time_str = receive_datetime.time().strftime(format='%H:%M:%S')
    time.sleep(request.get('delay'))
    write_time = datetime.now()
    write_time_str = write_time.time().strftime(format='%H:%M:%S')
    file2_data = {
        'id': request.get('id'),
        'receive_time': receive_time_str,
        'write_time': write_time_str
    }
    file_data_json = json.dumps(file2_data)
    channel.basic_publish(exchange='', routing_key='handler_writer', body=file_data_json)


def callback(ch, method, properties, body):
    request = body.decode('utf-8')
    request_data = load_data(request)
    t = threading.Thread(target=handle_request, args=(request_data, ))
    t.start()


def handler():
    credentials = pika.PlainCredentials('user', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                                   port=5672,
                                                                   credentials=credentials))

    channel = connection.channel()
    while True:
        request = channel.basic_consume(queue='consumer_handler', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    handler()
