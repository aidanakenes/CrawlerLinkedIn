import pika

from src.utils.conf import RabbitMQ
from src.utils.logger import get_logger
from src.collector.collector import IDCollector
from src.utils.task_manager import TaskManager, Task

logger = get_logger(__name__)

results_count = 0


class Publisher:
    def __init__(self):
        credentials = pika.PlainCredentials(**RabbitMQ.RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RabbitMQ.RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def publish_to_crawler_id(self, user_id):
        self.channel.basic_publish(
            exchange='',
            routing_key=RabbitMQ.RABBITMQ_CRAWLER_QUEUE,
            body=user_id
        )

    def publish_to_crawler_fullname(self, fullname: str):
        logger.info(f'[x] Publishing tasks to crawler_queue')
        global results_count
        for user_id in IDCollector().collect_id(fullname=fullname):
            results_count += 1
            self.publish_to_crawler_id(user_id=user_id)
        TaskManager().save_task(task=Task(
            keywords=fullname,
            endpoint='search',
            status='in_progress',
            amount=results_count
        ))

