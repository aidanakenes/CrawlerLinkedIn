import pika

from src.utils.conf import RABBIT_CONF, RABBIT_AUTH, RABBITMQ_CRAWLER_QUEUE
from src.utils.logger import get_logger
from src.service.collector import IDCollector

logger = get_logger(__name__)


class Publisher:
    def __init__(self):
        credentials = pika.PlainCredentials(**RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def __enter__(self):
        return Publisher()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def publish_to_crawler_id(self, user_id: str):
        logger.info(f'[x] Publishing task to crawler_queue')
        self.channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_CRAWLER_QUEUE,
            body=user_id
        )

    def publish_to_crawler_fullname(self, fullname: str):
        logger.info(f'[x] Publishing tasks to crawler_queue')
        for user_id in IDCollector().collect_id(fullname=fullname):
            self.channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_CRAWLER_QUEUE,
                body=user_id
            )

