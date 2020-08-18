import json

import pika

from src.utils.conf import RabbitMQ
from src.utils.logger import get_logger
from src.db.db_user import DBSaver
from src.models.user import User

logger = get_logger(__name__)


class Consumer:
    def __init__(self):
        credentials = pika.PlainCredentials(**RabbitMQ.RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RabbitMQ.RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def consume_from_saver_queue(self):
        self.channel.basic_consume(RabbitMQ.RABBITMQ_SAVER_QUEUE, self.callback, auto_ack=False)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("[x] May the force be with you!")

    @staticmethod
    def callback(ch, method, properties, body):
        task = json.loads(body)
        user = User(**task.get('body'))
        logger.info(f"[x] Received {user.user_id}")
        DBSaver().insert_user(user)
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    Consumer().consume_from_saver_queue()
