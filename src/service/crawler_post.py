import requests

from src.utils.conf import HEADERS, COOKIES
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LICrawler:
    def __init__(self):
        self.li_home = 'https://www.linkedin.com/uas/login'

    def login(self):
        params = (
            ('companyIdOrUniversalName', '9212433'),
            ('count', '10'),
            ('moduleKey', 'ORGANIZATION_MEMBER_FEED_DESKTOP'),
            ('numComments', '0'),
            ('numLikes', '0'),
            ('paginationToken', '834516713-1596340853617-fa791986bd130276ff6ff2887bac3fc9'),
            ('q', 'companyRelevanceFeed'),
            ('start', '3'),
        )

        response = requests.get('https://www.linkedin.com/voyager/api/organization/updatesV2', headers=HEADERS,
                                params=params, cookies=COOKIES)
        print(response.text)

