import json

import pika

from src.utils.conf import RABBIT_CONF, RABBIT_AUTH, RABBITMQ_CRAWLER_QUEUE, RABBITMQ_SAVER_QUEUE
from src.utils.logger import get_logger
from src.service.crawler_user import LICrawler

logger = get_logger(__name__)


class Worker:
    def __init__(self):
        credentials = pika.PlainCredentials(**RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=RABBITMQ_CRAWLER_QUEUE)
        self.channel.queue_declare(queue=RABBITMQ_SAVER_QUEUE)

    def consume_from_crawler_queue(self):
        self.channel.basic_consume(RABBITMQ_CRAWLER_QUEUE, self.publish_to_saver_queue, auto_ack=False)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("[x] May the force be with you!")

    def publish_to_saver_queue(self, ch, method, properties, body):
        user_id = body.decode('utf-8')
        logger.info(f'[x] Received {user_id}')
        logger.info(f'[x] Publishing tasks to saver_queue')
        user = LICrawler().get_user_by_id(user_id=user_id)
        self.channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_SAVER_QUEUE,
            body=json.dumps(json.dumps(user.dict(), ensure_ascii=False))
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    Worker().consume_from_crawler_queue()
