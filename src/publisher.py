import pika

from src.utils.conf import RABBIT_CONF, RABBIT_AUTH, RABBITMQ_CRAWLER_QUEUE
from src.service.collector import IDCollector


class Publisher:
    def __init__(self):
        credentials = pika.PlainCredentials(**RABBIT_AUTH)
        parameters = pika.ConnectionParameters(
            **RABBIT_CONF,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters=parameters)
        self.channel = self.connection.channel()

    def publish_to_crawler_queue(self, fullname: str):
        users_id = IDCollector().collect_id(fullname=fullname)
        for user_id in users_id:
            self.channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_CRAWLER_QUEUE,
                body=user_id
            )
        self.connection.close()


if __name__ == '__main__':
    Publisher().publish_to_crawler_queue('aidana ken')
