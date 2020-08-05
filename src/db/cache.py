import json
from typing import List

import redis

from src.utils.conf import RedisConfig
from src.models.user import User
from src.models.company import Company
from src.models.post import Post
from src.utils.logger import get_logger
from src.utils.conf import REDIS_TTL

logger = get_logger(__name__)


class Cache:
    def __init__(self):
        self.my_redis = redis.Redis(**RedisConfig)

    def save_cache_user(self, user: User):
        logger.info(f"Caching the result for {user.user_id}")
        self.my_redis.setex(
            name=f"user_{user.user_id}",
            time=REDIS_TTL,
            value=user.json()
        )

    def get_cached_user(self, user_id: str) -> User:
        cached = self.my_redis.get(f"user_{user_id}")
        if cached is not None:
            logger.info(f"Returning the cached result for username {user_id}")
            return User(**json.loads(cached))

    def save_cache_company(self, company: Company):
        logger.info(f"Caching the result for {company.company_id}")
        self.my_redis.setex(
            name=f"company_{company.company_id}",
            time=REDIS_TTL,
            value=company.json()
        )

    def get_cached_company(self, company_id: str) -> Company:
        cached = self.my_redis.get(f"company_{company_id}")
        if cached is not None:
            logger.info(f"Returning the cached result for {company_id}")
            return Company(**json.loads(cached))

    def save_cache_posts(self, posts: List[Post], company_id: str):
        logger.info(f"Caching the posts for {company_id}")
        self.my_redis.setex(
            name=f"posts_{company_id}",
            time=REDIS_TTL,
            value=str([post.dict() for post in posts])
        )

    def get_cached_posts(self, company_id: str):
        cached = self.my_redis.get(f"posts_{company_id}")
        if cached is not None:
            logger.info(f"Returning the cached posts for {company_id}")
            return json.dumps(cached, ensure_ascii=False)

    def save_cache_users(self, users: List[User], fullname: str):
        logger.info(f"Caching the users with fullname {fullname}")
        self.my_redis.setex(
            name=f"users_{fullname}",
            time=REDIS_TTL,
            value=str([user.dict() for user in users])
        )

    def get_cached_users(self, fullname: str):
        cached = self.my_redis.get(f"users_{fullname}")
        if cached is not None:
            logger.info(f"Returning the cached users with {fullname}")
            return json.dumps(cached, ensure_ascii=False)
