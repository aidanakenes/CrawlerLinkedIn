import json
import time

import requests
from typing import Optional, Dict, List
from pydantic.error_wrappers import ValidationError

from src.models.user import User, Education, Experience
from src.utils.logger import get_logger
from src.utils.retry_deco import retry
from src.utils.err_utils import ApplicationError, DoesNotExist
from src.utils.conf import UserRequest

logger = get_logger(__name__)


class LICrawler:

    def __init__(self):
        self.li_home = 'https://www.linkedin.com/in/'
        self.headers = UserRequest.HEADERS
        self.cookies = UserRequest.COOKIES
        self._request_url = UserRequest.URL
        self.params = UserRequest.PARAMS

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
            Get user's profile data by public id
            and return User object
        """
        raw_data = self._extract_raw_json(user_id=user_id)
        if raw_data is None:
            raise DoesNotExist()
        user_data = self._collect_data(data=raw_data, user_id=user_id)
        logger.info(f"Returning the LIUserCrawler's result for user {user_id}")
        return User(**user_data)

    def _extract_raw_json(self, user_id: str) -> Optional[Dict]:
        """
            Extract user's raw json
        """
        self.params['memberIdentity'] = user_id
        time.sleep(2)
        response = self._make_request()
        logger.info(f'Extracting data for {user_id}')
        if response:
            return json.loads(response.text).get('included')

    @retry(logger=logger, exc_to_check=(ConnectionError, TimeoutError), tries=2, delay=2)
    def _make_request(self):
        """
            Send GET request to user's page
        """
        try:
            response = requests.get(
                self._request_url,
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
        return response

    def _collect_data(self, data: dict, user_id: str) -> Dict:
        """
            Collect all necessary data for user from raw json
        """
        user_data = {}
        education = []
        experience = []
        skill = []

        try:
            for d in data:
                if 'birthDateOn' in d.keys():
                    user_data['fullname'] = f"{d.get('firstName').lower().capitalize()} " \
                                            f"{d.get('lastName').lower().capitalize()}"
                    user_data['heading'] = d.get('headline')
                    user_data['location'] = d.get('locationName')
                    user_data['profile_pic_url'] = self._get_profile_pic(data=d)
                if 'schoolUrn' in d.keys():
                    school = d.get('schoolName')
                    if school:
                        date_range = d.get('dateRange')
                        start = end = None
                        if date_range:
                            start = date_range['start']['year'] if 'start' in date_range.keys() else None
                            end = date_range['end']['year'] if 'end' in date_range.keys() else None
                        education.append(Education(
                            school=school,
                            degree=d.get('degreeName'),
                            start=start,
                            end=end
                        ))
                if 'title' in d.keys():
                    company = d.get('companyName')
                    if company:
                        date_range = d.get('dateRange')
                        start = end = None
                        if date_range:
                            start = date_range['start']['year'] if 'start' in date_range.keys() else None
                            end = date_range['end']['year'] if 'end' in date_range.keys() else None
                        experience.append(Experience(
                            company=d.get('companyName'),
                            position=d.get('title'),
                            start=start,
                            end=end
                        ))
                if 'fsd_skill' in d['entityUrn']:
                    skill.append(d.get('name'))

                user_data['experience'] = experience
                user_data['education'] = education
                user_data['skill'] = skill

            user_data['user_id'] = user_id
            user_data['user_url'] = f"{self.li_home}{user_id}"
            return user_data
        except AttributeError or Exception as e:
            logger.error(f"Failed to parse data: {type(e)}")
            raise ApplicationError()

    @staticmethod
    def _get_profile_pic(data: dict) -> Optional[str]:
        """
            Extract profile picture with the highest quality
        """
        if data.get('profilePicture') is None:
            return
        picture = data['profilePicture']['displayImageReference']['vectorImage']
        root_url = picture['rootUrl']
        size = picture['artifacts'][-1].get('fileIdentifyingUrlPathSegment')
        return f'{root_url}{size}'
