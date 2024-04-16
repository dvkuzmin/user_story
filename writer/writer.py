import time
from datetime import datetime, timedelta
import json
import logging
import threading

import pika

from utils import load_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                               port=5672,
                                                               credentials=credentials))

channel = connection.channel()


def write_file(request: dict):
    if len(request) == 2:
        with open('./files/file2.txt', 'a') as f:
            f.write(f'| {request.get("id")} | {request.get("receive_time")} |\n')
    if len(request) == 3:
        with open('./files/file1.txt', 'a') as f:
            f.write(f'| {request.get("id")} | {request.get("receive_time")} | {request.get("write_time")} |\n')


def callback(ch, method, properties, body):
    request = body.decode('utf-8')
    request_data = load_data(request)
    write_file(request_data)


def writer():
    while True:
        request = channel.basic_consume(queue='handler_writer', on_message_callback=callback, auto_ack=True)
        request = channel.basic_consume(queue='writer', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    writer()
