import json
import time

import requests

from src.utils.conf import SearchRequest
from src.utils.logger import get_logger
from src.utils.decorators import retry
from src.utils.err_utils import ApplicationError, DoesNotExist

logger = get_logger(__name__)


class IDCollector:
    def __init__(self):
        self._request_search = SearchRequest.URL
        self.params = SearchRequest.PARAMS
        self.headers = SearchRequest.HEADERS
        self.cookies = SearchRequest.COOKIES

    def collect_id(self, fullname: str):
        """
            Return generator of user' id filtered by the given fullname
        """
        for users in self._get_all_results(fullname):
            for user in users:
                pub_id = user.get('publicIdentifier')
                if pub_id and pub_id != 'UNKNOWN':
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
            time.sleep(2)
            response_json = json.loads(response.text)
            total = response_json['data']['metadata'].get('totalResultCount')
            if total is None:
                raise DoesNotExist()
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
        try:
            response = requests.get(
                self._request_search,
                headers=self.headers,
                cookies=self.cookies,
                params=self.params,
                timeout=10
            )
        except requests.exceptions.TooManyRedirects as e:
            logger.error(f'Problems with cookies and headers')
            raise ApplicationError()
        if response.status_code == 429:
            logger.error('Authorization failed')
            raise ApplicationError()
        if response.ok:
            return response
