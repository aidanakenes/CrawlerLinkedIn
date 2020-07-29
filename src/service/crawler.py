import re
import json

from typing import Optional
from bs4 import BeautifulSoup
from selenium import webdriver

from src.utils.conf import USER_EMAIL, USER_PASS, DRIVER_PATH
from src.models.user import User
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError, RegexError, AuthenticationError, BeautifulSoupError

logger = get_logger(__name__)


class LICrawler:
    def __init__(self):
        self.li_link = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

    def login(self):
        try:
            driver = webdriver.Firefox(executable_path=DRIVER_PATH)
            driver.get(self.li_link)
            driver.find_element_by_id('username').send_keys(USER_EMAIL)
            driver.find_element_by_id('password').send_keys(USER_PASS)
            driver.find_element_by_class_name('btn__primary--large').click()
            return driver
        except ApplicationError as e:
            logger.info(f'Cannot login: {type(e)}')
            raise AuthenticationError()

    @staticmethod
    def get_education(soup) -> Optional[list]:
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
    def get_experience(html_page: str) -> Optional[list]:
        regex = r'(?<="dateRange":\{"start":).*(?=,{"\*profilePositionInPositionGroup")'
        try:
            regex_res = re.findall(pattern=regex, string=html_page)
            if regex_res:
                regex_res = json.loads('[{"dateRange":{"start":' + regex_res[0] + ']')
        except ApplicationError as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise RegexError()

        experience = []
        for r in regex_res:
            if r.get('companyName'):
                start = end = None
                date_range = r.get('dateRange')
                if 'start' in date_range.keys():
                    start = date_range.get('start').get('year')
                if 'end' in date_range.keys():
                    end = date_range.get('end').get('year')
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
    def get_skills(html_page) -> Optional[list]:
        skills = []
        regex = r'(?<={"entityUrn":"urn:li:fsd_skill:).*(?=Skill"\},)'
        try:
            regex_res = re.findall(pattern=regex, string=html_page)
            if regex_res:
                regex_res = json.loads('[{"entityUrn":"urn:li:fsd_skill:' + regex_res[0] + 'Skill"}]')
        except ApplicationError as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise RegexError()

        for skill in regex_res:
            skills.append(skill.get('name'))
        return skills

    def get_user(self, user_url: str) -> Optional[User]:
        # driver = self.login()
        # driver.get(url=user_url)
        # html_page = driver.page_source
        # driver.close()
        with open(user_url) as f:
            html_page = f.read()
        logger.info(f"Starting the LIParser for user {user_url}")
        try:
            soup = BeautifulSoup(html_page, 'lxml')
            profile_pic_url: str = soup.find('img', attrs={'class': 'EntityPhoto-circle-9'})['src']

            logger.info(f"Returning the LIParser's result for user {user_url}")
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
        except ApplicationError as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise BeautifulSoupError()


if __name__ == '__main__':
    p = LICrawler()
    print('--------------------------')
    print(json.dumps(p.get_user('./drafts/testD.txt').dict(), indent=4, ensure_ascii=False))
    print('--------------------------')
    print(json.dumps(p.get_user('./drafts/testM.txt').dict(), indent=4, ensure_ascii=False))
    print('--------------------------')
    print(json.dumps(p.get_user('./drafts/testT.txt').dict(), indent=4, ensure_ascii=False))
    print('--------------------------')
    print(json.dumps(p.get_user('./drafts/testJ.txt').dict(), indent=4, ensure_ascii=False))
    print('--------------------------')
    print(json.dumps(p.get_user('./drafts/test.txt').dict(), indent=4, ensure_ascii=False))

    # print(p.get_user('https://www.linkedin.com/in/mark-zuckerberg-7b1b9071/'))
    # print(p.get_user('https://www.linkedin.com/in/almat-amirseitov-704988169/'))
    # print(p.get_user('https://www.linkedin.com/in/yedilkhan/'))
    # print(p.get_user('https://www.linkedin.com/in/temirlan-ashimov-42076816b/'))
    # print(p.get_user('https://www.linkedin.com/in/steve-jobson/'))
