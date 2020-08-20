from http import HTTPStatus
import json
from typing import Optional

import redis
from pydantic import BaseModel

from src.utils.conf import Redis
from src.utils.logger import get_logger
from src.utils.err_utils import DoesNotExist, CustomException

logger = get_logger(__name__)


class Task(BaseModel):
    keywords: str
    endpoint: str
    status: str
    last: Optional[str]


class TaskManager:
    def __init__(self):
        self.my_redis = redis.Redis(**Redis.RedisConfig)

    def save_task(self, task: Task):
        self.my_redis.setex(
            name=f'{task.endpoint}_{task.keywords}',
            value=task.json(),
            time=Redis.REDIS_TTL
        )

    def get_task(self, endpoint: str, keywords: str):
        cached = self.my_redis.get(f'{endpoint}_{keywords}')
        if cached is not None:
            return Task(**json.loads(cached))

    def update_status(self, task: Task, status: str):
        task.status = status
        self.save_task(task)

    @staticmethod
    def task_status(task):
        if task.status == 'no':
            return DoesNotExist().code, {'message': DoesNotExist().message}
        if task.status == 'failed':
            return CustomException().code, {'message': CustomException().message}
        if task.status == 'in_progress':
            return HTTPStatus.CREATED, {'message': 'Keep calm, response in progress!'}
