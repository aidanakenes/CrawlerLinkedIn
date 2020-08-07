import json

import requests
from typing import Optional, Dict, List
from pydantic.error_wrappers import ValidationError

from src.models.user import User
from src.models.education import Education
from src.models.experience import Experience
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError, NotFoundError
from src.utils.conf import HEADERS, COOKIES, USER_PARAMS, SEARCH_PARAMS

logger = get_logger(__name__)


class LIUserCrawler:

    def __init__(self):
        self.li_user_home = 'https://www.linkedin.com/in/'
        self._request_url = 'https://www.linkedin.com/voyager/api/identity/dash/profiles'
        self._request_search = 'https://www.linkedin.com/voyager/api/search/blended'

    def _extract_user_json_(self, user_id: str):
        USER_PARAMS['memberIdentity'] = user_id
        try:
            logger.info(f'Extracting data for {user_id}')
            r = requests.get(
                self._request_url,
                headers=HEADERS,
                params=USER_PARAMS,
                cookies=COOKIES,
                timeout=10
            )
            if r.ok:
                return json.loads(r.text).get('included')
        except TimeoutError as e:
            logger.error(f'Failed to find user {user_id}: {type(e)}')
            raise NotFoundError()
        except ConnectionError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise NotFoundError()

    def _extract_users_json_(self, fullname: str):
        SEARCH_PARAMS['keywords'] = fullname
        SEARCH_PARAMS['start'] = 0
        user_json = []
        try:
            res_data = json.loads(requests.get(
                        self._request_search,
                        headers=HEADERS,
                        params=SEARCH_PARAMS,
                        cookies=COOKIES,
                        timeout=10
                    ).text)['data']['metadata']
            if 'totalResultCount' not in res_data.keys():
                raise NotFoundError()
            total = res_data['totalResultCount']
            count = int(SEARCH_PARAMS['count'])
            logger.info(f"Extracting json data for user with fullname {fullname}")
            for start in range(0, total, count):
                r = requests.get(
                    self._request_search,
                    headers=HEADERS,
                    params=SEARCH_PARAMS,
                    cookies=COOKIES,
                    timeout=10
                )
                if r.ok:
                    user_json.append(json.loads(r.text)['included'])
                SEARCH_PARAMS['start'] = str(start)
            return user_json
        except TimeoutError as e:
            logger.error(f'Failed to find users with fullname {fullname}: {type(e)}')
            raise NotFoundError()
        except ConnectionError as e:
            logger.error(f'Failed to connect to LinkedIn: {type(e)}')
            raise ApplicationError()

    @staticmethod
    def _get_profile_pic(data: dict) -> Optional[str]:
        if data.get('profilePicture') is None:
            return
        root_url = data.get('profilePicture').get('displayImageReference').get('vectorImage').get('rootUrl')
        size = data.get('profilePicture').get('displayImageReference').get('vectorImage').get('artifacts')[
            -1].get(
            'fileIdentifyingUrlPathSegment')
        return f'{root_url}{size}'

    def _collect_data_(self, data: dict) -> Dict:
        user_data = {}
        education = []
        experience = []
        skills = []

        try:
            for d in data:
                if 'birthDateOn' in d.keys():
                    user_data['full_name'] = f"{d.get('firstName')} {d.get('lastName')}"
                    user_data['heading'] = d.get('headline')
                    user_data['location'] = d.get('locationName')
                    user_data['profile_pic_url'] = self._get_profile_pic(data=d)
                if 'schoolUrn' in d.keys():
                    date_range = d.get('dateRange')
                    start = end = None
                    if date_range:
                        start = date_range.get('start').get('year') if 'start' in date_range.keys() else None
                        end = date_range.get('end').get('year') if 'end' in date_range.keys() else None
                    education.append(Education(
                        school=d.get('schoolName'),
                        degree=d.get('degreeName'),
                        start=start,
                        end=end
                    ))
                if 'title' in d.keys():
                    company = d.get('companyName')
                    if company:
                        start = d.get('dateRange').get('start') if 'start' in d.keys() else None
                        end = d.get('dateRange').get('end') if 'end' in d.keys() else None
                        experience.append(Experience(
                            company=d.get('companyName'),
                            position=d.get('title'),
                            start=start.get('year') if start else None,
                            end=end.get('year') if end else None
                        ))
                if 'fsd_skill' in d.get('entityUrn'):
                    skills.append(d.get('name'))

                user_data['experience'] = experience
                user_data['education'] = education
                user_data['skills'] = skills
            return user_data
        except AttributeError as e:
            logger.error(f"Failed to parse data: {type(e)}")
            raise ApplicationError()
        except Exception as e:
            logger.error(f'Failed to parse data: {type(e)}')
            raise ApplicationError()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            data = self._extract_user_json_(user_id=user_id)
            if data is None:
                raise NotFoundError()
            user_data = self._collect_data_(data=data)
            user_data['user_id'] = user_id
            user_data['user_url'] = f'{self.li_user_home}{user_id}'
            logger.info(f"Returning the LIUserCrawler's result for user {user_id}")
            return User(**user_data)
        except ValidationError as e:
            logger.error(f'Failed to parse data for {user_id}: {type(e)}')
            raise ApplicationError()

    def get_users(self, fullname: str) -> List[User]:
        data = self._extract_users_json_(fullname=fullname)
        users = []
        for d in data:
            for user in d:
                if user.get('firstName') or user.get('lastName'):
                    users.append(self.get_user_by_id(user.get('publicIdentifier')))
        return users


