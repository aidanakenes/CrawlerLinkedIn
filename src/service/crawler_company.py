import json
from typing import Optional, List

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

    def _get_company_data_(self, company_id: str):
        COMPANY_PARAMS['universalName'] = company_id
        try:
            r = requests.get(
                self._request_url,
                headers=HEADERS,
                params=COMPANY_PARAMS,
                cookies=COOKIES,
                timeout=10
            )
            if r.ok:
                return json.loads(r.text).get('included')
        except TimeoutError as e:
            logger.error(f'Failed to parse for company {company_id}: {type(e)}')
            raise ApplicationError()

    @staticmethod
    def _get_logo(data: dict) -> Optional[str]:
        root_url = data.get('logo').get('image').get('rootUrl')
        size = data.get('logo').get('image').get('artifacts')[-1].get('fileIdentifyingUrlPathSegment')
        return f'{root_url}{size}'

    @staticmethod
    def _get_locations(data: dict) -> List:
        locations = []
        for loc in data.get('confirmedLocations'):
            locations.append(f"{loc.get('country')}, "
                             f"{loc.get('geographicArea')}, "
                             f"{loc.get('line1')}")
        return locations

    def get_company(self, company_id: str) -> Optional[Company]:
        data = self._get_company_data_(company_id=company_id)
        try:
            for d in data:
                major = d.get('localizedName') if 'localizedName' in d.keys() else None
                if 'staffCount' in d.keys():
                    logger.info(f"Returning the LICompanyCrawler's result for company {company_id}")
                    return Company(
                        company_id=company_id,
                        title=d.get('name'),
                        url=f'{self.li_comp_home}{company_id}',
                        external_url=d.get('companyPageUrl'),
                        logo=self._get_logo(data=d),
                        major=major,
                        employees_num=d.get('staffCount'),
                        locations=self._get_locations(data=d),
                        heading=d.get('tagline'),
                        about=d.get('description')
                    )
        except AttributeError as e:
            logger.error(f'Failed to parse company: {type(e)}')
            raise ApplicationError()
        except ValidationError as e:
            logger.error(f'Failed to parse company: {type(e)}')
            raise ApplicationError()
