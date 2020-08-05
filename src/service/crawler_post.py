import json
from typing import List

import dateparser
import requests
from pydantic.error_wrappers import ValidationError

from src.utils.conf import HEADERS, COOKIES, POST_PARAMS
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError
from src.models.post import Post

logger = get_logger(__name__)


class LIPostCrawler:
    def __init__(self):
        self._request_url = 'https://www.linkedin.com/voyager/api/organization/updatesV2'

    def _get_post_data_(self, company_id):
        POST_PARAMS[2] = {'companyIdOrUniversalName': company_id}
        try:
            r = requests.get(
                self._request_url,
                headers=HEADERS,
                params=POST_PARAMS,
                cookies=COOKIES,
                timeout=10
            )
            if r.ok:
                return json.loads(r.text).get('included')
        except TimeoutError as e:
            logger.error(f'Failed to parse posts for {company_id}: {type(e)}')
            raise ApplicationError()

    @staticmethod
    def _get_post(data: dict, company_id: str) -> Post:
        return Post(
                    company_id=company_id,
                    date=dateparser.parse(
                        data.get('actor').get('subDescription').get('accessibilityText'),
                        settings={'TIMEZONE': 'Asia/Almaty'},
                        date_formats=['%d %B %Y']
                    ),
                    content=data.get('commentary').get('text').get('text')
                )

    def get_posts(self, company_id: str) -> List[Post]:
        data = self._get_post_data_(company_id=company_id)
        posts = []
        try:
            for d in data:
                if 'annotation' in d.keys():
                    posts.append(self._get_post(data=d, company_id=company_id))
            logger.info(f"Returning the LIPostCrawler's result for posts of {company_id}")
            return posts
        except AttributeError as e:
            logger.error(f'Failed to parse posts: {type(e)}')
            raise ApplicationError()
        except ValidationError as e:
            logger.error(f'Failed to parse posts: {type(e)}')
            raise ApplicationError()
