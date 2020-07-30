from selenium import webdriver

from src.utils.conf import USER_EMAIL, USER_PASS, DRIVER_PATH
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError, AuthenticationError

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
