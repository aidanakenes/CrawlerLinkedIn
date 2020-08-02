import json
from typing import Optional

import requests

from src.utils.logger import get_logger
from src.models.company import Company
from src.utils.conf import HEADERS, COOKIES, COMPANY_PARAMS

logger = get_logger(__name__)


class LICompanyCrawler:

    def __init__(self):
        self.li_comp_home = 'https://www.linkedin.com/company/'
        self._request_url = 'https://www.linkedin.com/voyager/api/organization/companies'

    def _get_company_data_(self, company_url: str):
        COMPANY_PARAMS.append(('universalName', company_url[len(self.li_comp_home):-1]))
        response = requests.get(
            self._request_url,
            headers=HEADERS,
            params=COMPANY_PARAMS,
            cookies=COOKIES
        )
        return json.loads(response.text)['included']

    def get_company(self, company_url: str) -> Optional[Company]:
        data = self._get_company_data_(company_url=company_url)
        for d in data:
            major = d.get('localizedName') if 'localizedName' in d.keys() else None

            if 'staffCount' in d.keys():
                pic_root_url = d.get('logo').get('image').get('rootUrl')
                pic_size = d.get('logo').get('image').get('artifacts')[-1].get('fileIdentifyingUrlPathSegment')

                logger.info(f"Returning the LICompanyCrawler's result for user {company_url}")
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


if __name__ == '__main__':
    c = LICompanyCrawler()
    print(json.dumps(c.get_company(
        company_url='https://www.linkedin.com/company/kolesagroup/').dict(),
        ensure_ascii=False,
        indent=4
    ))
