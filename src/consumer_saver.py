import json

import pika

from src.utils.conf import RABBIT_CONF, RABBIT_AUTH, RABBITMQ_SAVER_QUEUE
from src.utils.logger import get_logger
from src.db.db_user import DBUser
from src.models.user import User

logger = get_logger(__name__)


class Consumer:
    def __init__(self):
        credentials = pika.PlainCredentials(**RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def consume_from_saver_queue(self):
        self.channel.basic_consume(RABBITMQ_SAVER_QUEUE, self.callback, auto_ack=False)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("[x] May the force be with you!")

    @staticmethod
    def callback(ch, method, properties, body):
        user = json.loads(json.loads(body))
        logger.info(f"[x] Received {user.get('user_id')}")
        DBUser().insert_user(User(**user))
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    Consumer().consume_from_saver_queue()
