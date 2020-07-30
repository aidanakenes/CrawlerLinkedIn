from bs4 import BeautifulSoup


from src.service.crawler import LICrawler
from src.utils.logger import get_logger
from src.models.company import Company
from src.models.post import Post
from src.utils.err_utils import BeautifulSoupError

logger = get_logger(__name__)


class LICompanyCrawler(LICrawler):

    def __init__(self):
        super().__init__()
        self.driver = super().login()

    def get_company(self, company_url: str):
        self.driver.get(url=company_url)
        html_page = self.driver.page_source
        self.driver.close()

        logger.info(f"Starting the LICompanyCrawler for user {company_url}")
        try:
            soup = BeautifulSoup(html_page, 'lxml')
            logger.info(f"Returning the LICompanyCrawler's result for company {company_url}")
            return Company(
                title='',
                heading='',
                external_url=' ',
                location='',
                employees_num=0,
                followers_num=0,
                posts=[Post()],
                url=company_url,
                profile_pic_url=''
            )
        except TypeError as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise e
        except Exception as e:
            logger.info(f'Cannot parse page: {type(e)}')
            raise BeautifulSoupError()

