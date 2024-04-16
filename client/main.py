import pika
import threading
import random
import json
import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

credentials = pika.PlainCredentials('user', 'pass')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',
                                                               port=5672,
                                                               credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='client_consumer')

lock = threading.Lock()

request_id = 1


def send_request(request_value: int, delay_range: tuple[int, int]):
    for i in range(request_value):
        # Отправляем в каждом потоке несколько пакетов
        global request_id
        with lock:
            request = {
                'id': request_id,
                'delay': random.randint(*delay_range)
            }
            request_id += 1
            request_json = json.dumps(request)
            logger.info(f'{datetime.datetime.now().time()} ThreadID {threading.get_ident()} Request: {request}')
            channel.basic_publish(exchange='', routing_key='client_consumer', body=request_json)


def start_client(connection_count: int, connection_value: int, delay_range: tuple[int, int]):
    remainder = connection_value % connection_count
    threads = []
    for i in range(connection_count):
        request_value = connection_value // connection_count
        if remainder:
            request_value += 1
            remainder -= 1
        # Запускаем несколько параллельных обращений к консьюмеру
        t = threading.Thread(target=send_request, args=(request_value, delay_range))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    start_client(5, 20, (1, 5))  # Запускаем 5 потоков, каждый отправляет 20 сообщений с задержкой от 1 до 5 секунд
