import json
from typing import Optional

import requests
from pydantic.error_wrappers import ValidationError

from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError
from src.models.company import Company
from src.utils.conf import HEADERS, COOKIES, COMPANY_PARAMS

logger = get_logger(__name__)


class LICompanyCrawler:

    def __init__(self):
        self.li_comp_home = 'https://www.linkedin.com/company/'
        self._request_url = 'https://www.linkedin.com/voyager/api/organization/companies'

    def _get_company_data_(self, company_url: str):
        COMPANY_PARAMS.append(('universalName', company_url[len(self.li_comp_home):-1]))
        try:
            r = requests.get(
                self._request_url,
                headers=HEADERS,
                params=COMPANY_PARAMS,
                cookies=COOKIES,
                timeout=10
            )
            del COMPANY_PARAMS[-1]
            if r.ok:
                return json.loads(r.text).get('included')
        except TimeoutError as e:
            logger.error(f'Failed to parse for company {company_url}: {type(e)}')
            raise ApplicationError()

    def get_company(self, company_url: str) -> Optional[Company]:
        data = self._get_company_data_(company_url=company_url)
        try:
            for d in data:
                major = d.get('localizedName') if 'localizedName' in d.keys() else None

                if 'staffCount' in d.keys():
                    pic_root_url = d.get('logo').get('image').get('rootUrl')
                    pic_size = d.get('logo').get('image').get('artifacts')[-1].get('fileIdentifyingUrlPathSegment')

                    logger.info(f"Returning the LICompanyCrawler's result for company {company_url}")
                    return Company(
                        title=d.get('name'),
                        url=company_url,
                        external_url=d.get('companyPageUrl'),
                        logo=f'{pic_root_url}{pic_size}',
                        major=major,
                        employees_num=d.get('staffCount'),
                        locations=[
                            f"{loc.get('country')}, {loc.get('geographicArea')}, {loc.get('line1')}"
                            for loc in d.get('confirmedLocations')
                        ],
                        heading=d.get('tagline'),
                        about=d.get('description')
                    )
        except AttributeError as e:
            logger.error(f'Failed to parse company: {type(e)}')
            raise ApplicationError()
        except ValidationError as e:
            logger.error(f'Failed to parse company: {type(e)}')
            raise ApplicationError()


if __name__ == '__main__':
    c = LICompanyCrawler()
    print(json.dumps(c.get_company('https://www.linkedin.com/company/kolesagroup/').dict(), indent=4, ensure_ascii=False))
    print(json.dumps(c.get_company('https://www.linkedin.com/company/astana-it-university/').dict(), indent=4, ensure_ascii=False))
    print(json.dumps(c.get_company('https://www.linkedin.com/company/kolesagroup/').dict(), indent=4, ensure_ascii=False))