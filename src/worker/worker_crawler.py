import json

import pika

from src.utils.conf import RabbitMQ
from src.utils.logger import get_logger
from src.service.crawler_user import LICrawler
from src.utils.err_utils import ApplicationError

logger = get_logger(__name__)


class Worker:
    def __init__(self):
        credentials = pika.PlainCredentials(**RabbitMQ.RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RabbitMQ.RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=RabbitMQ.RABBITMQ_CRAWLER_QUEUE)
        self.channel.queue_declare(queue=RabbitMQ.RABBITMQ_SAVER_QUEUE)

    def consume_from_crawler_queue(self):
        self.channel.basic_consume(RabbitMQ.RABBITMQ_CRAWLER_QUEUE, self.callback, auto_ack=False)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("[x] May the force be with you!")

    def callback(self, ch, method, properties, body):
        user_id = body.decode('utf-8')
        logger.info(f'[x] Received {user_id}')
        try:
            user = LICrawler().get_user_by_id(user_id=user_id)
        except ApplicationError() as e:
            logger.error(f'Failed to parse user {user_id}: {e}')
            return
        logger.info(f'[x] Publishing tasks to saver_queue')
        if user:
            self.channel.basic_publish(
                exchange='',
                routing_key=RabbitMQ.RABBITMQ_SAVER_QUEUE,
                body=json.dumps(user.dict())
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    Worker().consume_from_crawler_queue()
