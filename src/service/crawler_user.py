import re
import json

from typing import Optional, List
from bs4 import BeautifulSoup

from src.service.crawler import LICrawler
from src.models.user import User
from src.utils.logger import get_logger
from src.utils.err_utils import RegexError, BeautifulSoupError

logger = get_logger(__name__)


class LIUserCrawler(LICrawler):

    def __init__(self):
        super().__init__()
        self.li_user_home = 'https://www.linkedin.com/in/'
        self.driver = super().login()

    @staticmethod
    def get_education(soup: BeautifulSoup) -> List[dict]:
        education = []
        blocks = soup.findAll('li', attrs={'class': 'pv-education-entity'})
        if blocks:
            for block in blocks:
                soup = BeautifulSoup(str(block), 'lxml')
                school_name = soup.find('h3', attrs={'class': 'pv-entity__school-name t-16 t-black t-bold'})
                degree_name = soup.find('span', attrs={'class': 'pv-entity__comma-item'})

                school_name = str(school_name.text).strip() if school_name else None
                degree_name = str(degree_name.text).strip() if degree_name else None

                date_range = []
                time = soup.findAll('time')
                if time:
                    date_range = [str(year).strip('<time></time>') for year in soup.findAll('time')]

                education.append({
                    'school_name': school_name,
                    'degree_name': degree_name,
                    'date_range': date_range
                })
        return education

    @staticmethod
    def get_experience(html_page: str) -> List[dict]:
        regex = r'(?<="dateRange":\{"start":).*(?=,{"\*profilePositionInPositionGroup")'
        try:
            regex_res = re.findall(pattern=regex, string=html_page)
            if regex_res:
                regex_res = json.loads('[{"dateRange":{"start":' + regex_res[0] + ']')
        except Exception as e:
            logger.info(f'Cannot parse experience: {type(e)}')
            raise RegexError()

        experience = []
        for r in regex_res:
            if r.get('companyName'):
                date_range = r.get('dateRange')
                start = date_range.get('start').get('year') if 'start' in date_range.keys() else None
                end = date_range.get('end').get('year') if 'end' in date_range.keys() else None
                experience.append({
                    'company_name': r.get('companyName'),
                    'job_title': r.get('title'),
                    'date_range': {
                        'start': start,
                        'end': end
                    }
                })

        return experience

    @staticmethod
    def get_skills(html_page: str) -> List[str]:
        skills = []
        regex = r'(?<={"entityUrn":"urn:li:fsd_skill:).*(?=Skill"\},)'
        try:
            regex_res = re.findall(pattern=regex, string=html_page)
            if regex_res:
                regex_res = json.loads('[{"entityUrn":"urn:li:fsd_skill:' + regex_res[0] + 'Skill"}]')
        except Exception as e:
            logger.info(f'Cannot parse skills: {type(e)}')
            raise RegexError()

        for skill in regex_res:
            skills.append(skill.get('name'))
        return skills

    def get_user(self, username: str) -> Optional[User]:
        user_url = f'{self.li_user_home}{username}'
        self.driver.get(url=user_url)
        html_page = self.driver.page_source
        self.driver.close()

        logger.info(f"Starting the LIUserCrawler for user {user_url}")
        try:
            soup = BeautifulSoup(html_page, 'lxml')
            profile_pic_url: str = soup.find('img', attrs={'class': 'EntityPhoto-circle-9'})['src']

            logger.info(f"Returning the LIUserCrawler's result for user {user_url}")
            return User(
                full_name=str(
                    soup.find('li', attrs={'class': 'inline t-24 t-black t-normal break-words'}).text
                ).strip(),
                location=str(soup.find('li', attrs={'class': 't-16 t-black t-normal inline-block'}).text).strip(),
                heading=str(soup.find('h2', attrs={'class': 'mt1'}).text).strip(),
                education=self.get_education(soup=soup),
                experience=self.get_experience(html_page=html_page),
                skills=self.get_skills(html_page=html_page),
                profile_pic_url=None if 'data:image' in profile_pic_url else profile_pic_url,
                user_url=user_url
            )
        except TypeError as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise e
        except Exception as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise BeautifulSoupError()

