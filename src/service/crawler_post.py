import json
from typing import List

import dateparser
import requests

from src.utils.conf import HEADERS, COOKIES, POST_PARAMS
from src.utils.logger import get_logger
from src.models.post import Post

logger = get_logger(__name__)


class LIPostCrawler:
    def __init__(self):
        self._request_url = 'https://www.linkedin.com/voyager/api/organization/updatesV2'

    def _get_post_data_(self, company_id):
        POST_PARAMS.append(('companyIdOrUniversalName', company_id))
        response = requests.get(
            self._request_url,
            headers=HEADERS,
            params=POST_PARAMS,
            cookies=COOKIES
        )
        return json.loads(response.text).get('included')

    def get_post(self, company_id: str) -> List[Post]:
        data = self._get_post_data_(company_id=company_id)
        posts = []
        for d in data:
            if 'annotation' in d.keys():
                posts.append(
                    Post(
                        company_name=company_id,
                        date=dateparser.parse(
                            d.get('actor').get('subDescription').get('accessibilityText'),
                            settings={'TIMEZONE': 'Asia/Almaty'},
                            date_formats=['%d %B %Y']
                        ),
                        content=d.get('commentary').get('text').get('text')
                    )
                )
        logger.info(f"Returning the LIPostCrawler's result for user {company_id}")
        return posts


if __name__ == '__main__':
    c = LIPostCrawler()
    print(len(c.get_post(company_id='kolesagroup')))
