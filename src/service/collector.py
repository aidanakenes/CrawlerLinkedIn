import json

import requests

from src.utils.conf import HEADERS, COOKIES, SEARCH_PARAMS
from src.utils.logger import get_logger
from src.utils.err_utils import NotFound, ApplicationError

logger = get_logger(__name__)


class IDCollector:
    def __init__(self):
        self._request_search = 'https://www.linkedin.com/voyager/api/search/blended'

    def _get_results_num(self) -> int:
        try:
            response_json = json.loads(self._make_request().text)['data']['metadata']
            if 'totalResultCount' not in response_json.keys():
                raise NotFound()
            return response_json['totalResultCount']
        except ConnectionError or TimeoutError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise ApplicationError()

    def _make_request(self):
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

    def _extract_raw_json(self, fullname: str):
        SEARCH_PARAMS['keywords'] = fullname
        SEARCH_PARAMS['start'] = 0
        raw_users_data = []
        total = self._get_results_num()
        logger.info(f"Extracting raw json data for users with fullname {fullname}, total: {total}")
        for start in range(0, total, int(SEARCH_PARAMS['count'])):
            response = self._make_request()
            if response.ok:
                raw_users_data.append(json.loads(response.text)['included'])
            SEARCH_PARAMS['start'] = str(start)
        return raw_users_data

    def collect_id(self, fullname: str):
        raw_users_data = self._extract_raw_json(fullname)
        users_data = []
        for data in raw_users_data:
            for user in data:
                if user.get('firstName') or user.get('lastName'):
                    users_data.append(user.get('publicIdentifier'))
        return users_data
