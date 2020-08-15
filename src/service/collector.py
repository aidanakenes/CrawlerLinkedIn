import json

import requests

from src.utils.conf import HEADERS, COOKIES, SEARCH_REQUEST_PARAMS, SEARCH_REQUEST_URL
from src.utils.logger import get_logger
from src.utils.decorators import retry
from src.utils.err_utils import ApplicationError, DoesNotExist

logger = get_logger(__name__)


class IDCollector:
    def __init__(self):
        self._request_search = SEARCH_REQUEST_URL
        self.params = SEARCH_REQUEST_PARAMS
        self.headers = HEADERS
        self.cookies = COOKIES

    def collect_id(self, fullname: str):
        """
        Return generator of user' id filtered by the given fullname
        """
        for users in self._get_all_results(fullname):
            for user in users:
                if user.get('publicIdentifier'):
                    yield user.get('publicIdentifier')

    def _get_all_results(self, fullname: str):
        """
        Go through all pages and get users' data
        """
        self._prepare_params(fullname)
        self.params['start'], self.params['count'] = 0, 49
        total = self.params['count'] + 1
        logger.info(f"Extracting raw json data for users with fullname {fullname}")
        while self.params['start'] < total:
            response = self._make_request()
            if response is None:
                raise DoesNotExist()
            response_json = json.loads(response.text)
            total = response_json['data']['metadata']['totalResultCount']
            yield response_json['included']
            self.params['start'] += self.params['count']

    def _prepare_params(self, fullname: str):
        """
            Put fullname into search filter
        """
        self.params['keywords'] = fullname
        first_name, *rest = fullname.split()
        last_name = " ".join(rest)
        self.params['filters'] = self.params['filters'].format(first_name=first_name, last_name=last_name)

    @retry(logger=logger, exc_to_check=(ConnectionError, TimeoutError), tries=3, delay=2)
    def _make_request(self):
        """
            Send GET request to search users
        """
        response = requests.get(
            self._request_search,
            headers=self.headers,
            cookies=self.cookies,
            params=self.params,
            timeout=10
        )
        if response.status_code == 429:
            logger.error('Authorization failed')
            raise ApplicationError()
        if response.ok:
            return response


