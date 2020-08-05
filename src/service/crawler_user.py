import json

import requests
from typing import Optional, Dict
from pydantic.error_wrappers import ValidationError

from src.models.user import User
from src.models.education import Education
from src.models.experience import Experience
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError
from src.utils.conf import HEADERS, COOKIES, USER_PARAMS

logger = get_logger(__name__)


class LIUserCrawler:

    def __init__(self):
        self.li_user_home = 'https://www.linkedin.com/in/'
        self._request_url = 'https://www.linkedin.com/voyager/api/identity/dash/profiles'

    def _get_user_data_(self, user_id: str):
        USER_PARAMS[2] = {'memberIdentity': user_id}
        try:
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
            logger.error(f'Failed to parse user {user_id}: {type(e)}')
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
                    education.append(Education(
                        school=d.get('schoolName'),
                        degree=d.get('degreeName'),
                        start=d.get('dateRange').get('start').get('year'),
                        end=d.get('dateRange').get('end').get('year')
                    ))
                if 'title' in d.keys():
                    company = d.get('companyName')
                    if company:
                        start = d.get('dateRange').get('start')
                        end = d.get('dateRange').get('end')
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
            logger.error(f'Failed to parse skills: {type(e)}')
            raise ApplicationError()

    def get_user(self, user_url: str) -> Optional[User]:
        user_id = user_url[len(self.li_user_home):-1]
        try:
            data = self._get_user_data_(user_id=user_id)
            user_data = self._collect_data_(data=data)
            logger.info(f"Returning the LIUserCrawler's result for user {user_id}")
            return User(**user_data)
        except ValidationError as e:
            logger.error(f'Failed to parse data for {user_id}: {type(e)}')
            raise ApplicationError()