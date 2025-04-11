import pika
import time
import logging

#from app.routes.models import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
# Настройка логирования 

connection_params = pika.ConnectionParameters(
    host='rabbitmq',  # Замените на адрес вашего RabbitMQ сервера
    port=5672,          # Порт по умолчанию для RabbitMQ
    virtual_host='/',   # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username='rmuser',  # Имя пользователя по умолчанию
        password='rmpassword'   # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)  # Создание очереди (если не существует)


# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, properties, body):
    # time.sleep(3) # Имитация полезной работы
    logger.info('---------------')
    logger.info(body.decode('utf-8').split('//'))
    model_id, user_id = body.decode('utf-8').split('//')
    logger.info(f'model_id = {model_id} || user_id = {user_id}')

    ##use_model(model_id=model_id, user_id=user_id, session=Depends(get_session))

    logger.info(f"Received: || '{body}'")
    ch.basic_ack(delivery_tag=method.delivery_tag) # Ручное подтверждение обработки сообщения

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False  # Автоматическое подтверждение обработки сообщений
)

logger.info('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()