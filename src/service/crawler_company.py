from typing import Optional

from src.service.crawler import LICrawler
from src.utils.logger import get_logger
from src.models.company import Company


logger = get_logger(__name__)


class LICompanyCrawler(LICrawler):

    def __init__(self):
        super().__init__()
        self.driver = super().login()

    def get_company(self, company_link: str) -> Optional[Company]:
        pass
