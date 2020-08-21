from http import HTTPStatus
import json
from typing import Optional

import redis
from pydantic import BaseModel

from src.utils.conf import Redis
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Task(BaseModel):
    task_id: str
    status: str
    last: Optional[str]


class TaskManager:
    def __init__(self):
        self.my_redis = redis.Redis(**Redis.RedisConfig)

    def save_task(self, task: Task):
        logger.info(f'Caching the task')
        self.my_redis.setex(
            name=task.task_id,
            value=task.json(),
            time=Redis.REDIS_TTL
        )

    def get_task(self, task_id: str):
        cached = self.my_redis.get(task_id)
        if cached is not None:
            return Task(**json.loads(cached))

    def update_status(self, task: Task, status: str):
        task.status = status
        self.save_task(task)
