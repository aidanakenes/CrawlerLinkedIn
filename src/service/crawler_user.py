import json

import requests
from typing import Optional, List, Dict

from src.models.user import User
from src.utils.logger import get_logger
from src.utils.conf import HEADERS, COOKIES, USER_PARAMS

logger = get_logger(__name__)


class LIUserCrawler:

    def __init__(self):
        self.li_user_home = 'https://www.linkedin.com/in/'
        self._request_url = 'https://www.linkedin.com/voyager/api/identity/dash/profiles'

    def _get_user_data_(self, user_url: str):
        USER_PARAMS.append(('memberIdentity', user_url[len(self.li_user_home):-1]))
        response = requests.get(
            self._request_url,
            headers=HEADERS,
            params=USER_PARAMS,
            cookies=COOKIES
        )
        return json.loads(response.text)['included']

    @staticmethod
    def _get_education_(data: dict) -> List:
        education = []
        for d in data:
            if 'schoolUrn' in d.keys():
                education.append({
                    'school_name': d.get('schoolName'),
                    'degree_name': d.get('degreeName'),
                    'duration': [
                        d.get('dateRange').get('start').get('year'),
                        d.get('dateRange').get('end').get('year')
                    ]
                })
        return education

    @staticmethod
    def _get_experience_(data: dict) -> List:
        experience = []
        for d in data:
            if 'title' in d.keys():
                company = d.get('companyName')
                if company:
                    start = d.get('dateRange').get('start')
                    end = d.get('dateRange').get('end')
                    experience.append({
                        'company': d.get('companyName'),
                        'job_title': d.get('title'),
                        'duration': [
                            start.get('year') if start else None,
                            end.get('year') if end else None
                        ]
                    })
        return experience

    @staticmethod
    def _get_skills_(data: dict) -> List:
        skills = []
        for d in data:
            if 'fsd_skill' in d.get('entityUrn'):
                skills.append(d.get('name'))
        return skills

    @staticmethod
    def _get_personal_(data: dict) -> Dict:
        personal = {}
        for d in data:
            profile_pic_url = d.get('profilePicture')
            if 'birthDateOn' in d.keys():
                if profile_pic_url:
                    root_url = d.get('profilePicture').get('displayImageReference').get('vectorImage').get('rootUrl')
                    size = d.get('profilePicture').get('displayImageReference').get('vectorImage').get('artifacts')[
                        -1].get(
                        'fileIdentifyingUrlPathSegment')
                    profile_pic_url = f'{root_url}{size}'

                personal = {
                    'full_name': f"{d.get('firstName')}{d.get('lastName')}",
                    'heading': d.get('headline'),
                    'last_name': d.get('lastName'),
                    'location': d.get('locationName'),
                    'profile_pic_url': profile_pic_url
                }
        return personal

    def get_user(self, user_url: str) -> Optional[User]:
        data = self._get_user_data_(user_url=user_url)
        logger.info(f"Returning the LIUserCrawler's result for user {user_url}")
        user_dict = self._get_personal_(data=data)
        user_dict['user_url'] = user_url
        user_dict['education'] = self._get_education_(data=data)
        user_dict['experience'] = self._get_experience_(data=data)
        user_dict['skills'] = self._get_skills_(data=data)
        return User(**user_dict)
