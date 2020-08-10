import json

import requests

from src.utils.conf import HEADERS, COOKIES, SEARCH_PARAMS
from src.utils.logger import get_logger
from src.utils.err_utils import NotFound, ApplicationError

logger = get_logger(__name__)


class IDCollector:
    def __init__(self):
        self._request_search = 'https://www.linkedin.com/voyager/api/search/blended'

    def collect_id(self, fullname: str):
        """
        Return list of users' id with the given fullname
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
        SEARCH_PARAMS['keywords'] = fullname
        total = self._get_results_num()
        logger.info(f"Extracting raw json data for users with fullname {fullname}, total: {total}")
        SEARCH_PARAMS['start'] = 0
        for start in range(0, total, int(SEARCH_PARAMS['count'])):
            yield self._extract_raw_json()
            SEARCH_PARAMS['start'] = str(start)

    def _get_results_num(self) -> int:
        """
        Return total number of results
        """
        try:
            response = self._make_request()
            response_json = json.loads(response.text)['data']['metadata']
            if 'totalResultCount' not in response_json.keys():
                raise NotFound()
            return response_json['totalResultCount']
        except ConnectionError or TimeoutError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise ApplicationError()

    def _make_request(self):
        """
        Send GET request to search users
        """
        try:
            return requests.get(
                self._request_search,
                headers=HEADERS,
                params=SEARCH_PARAMS,
                cookies=COOKIES,
                timeout=10
            )
        except TimeoutError as e:
            logger.error(f'Failed to find users: {type(e)}')
            raise NotFound()
        except ConnectionError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise ApplicationError()

    def _extract_raw_json(self):
        """
        Extract raw json data of users
        """
        response = self._make_request()
        if response.ok:
            return json.loads(response.text)['included']


