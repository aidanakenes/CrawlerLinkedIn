import json

import requests

from src.utils.conf import HEADERS, COOKIES, SEARCH_PARAMS
from src.utils.logger import get_logger
from src.utils.err_utils import DoesNotExist, ApplicationError

logger = get_logger(__name__)


class IDCollector:
    def __init__(self):
        self._request_search = 'https://www.linkedin.com/voyager/api/search/blended'
        self.params = SEARCH_PARAMS

    def collect_id(self, fullname: str):
        """
        Return list of users' id according to the given fullname
        """
        users_data = []
        for data in self._get_all_results(fullname):
            for user in data:
                if user.get('firstName') or user.get('lastName'):
                    users_data.append(user.get('publicIdentifier'))
        return users_data

    def _get_all_results(self, fullname: str):
        """
        Go through all pages and get users' data
        """
        self.params['keywords'] = fullname
        self.params['start'] = 0
        self.params['count'] = 49
        total = self.params['count'] + 1
        logger.info(f"Extracting raw json data for users with fullname {fullname}")
        try:
            while self.params['start'] < total:
                response = self._make_request()
                response_json = json.loads(response.text)
                total = response_json['data']['metadata']['totalResultCount']
                yield response_json['included']
                self.params['start'] += self.params['count']
        except KeyError:
            raise DoesNotExist()

    def _make_request(self):
        """
        Send GET request to search users
        """
        try:
            retries = 3
            while retries:
                response = requests.get(
                    self._request_search,
                    headers=HEADERS,
                    params=self.params,
                    cookies=COOKIES,
                    timeout=10
                )
                if response.ok:
                    return response
                retries -= 1
        except TimeoutError or ConnectionError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise ApplicationError()



