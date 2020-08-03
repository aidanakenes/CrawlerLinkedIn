from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String, INT
from sqlalchemy.exc import OperationalError

from src.models.company import Company
from src.utils.conf import ENGINE
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError

logger = get_logger(__name__)


class DBCompany:

    def __init__(self):
        self._engine = create_engine(ENGINE, client_encoding='utf8')
        self._metadata = MetaData(self._engine)
        self._table = Table('companies', self._metadata,
                            Column('company_id', String, primary_key=True),
                            Column('title', String),
                            Column('url', String),
                            Column('external_url', String),
                            Column('logo', String),
                            Column('major', String),
                            Column('employees_num', INT),
                            Column('heading', String),
                            Column('about', String)
                            )
        if not self._engine.has_table('companies'):
            self._table.create()

    def insert_company(self, _company: Company):
        try:
            with self._engine.connect() as con:
                stmt = self._table.insert().values(
                    company_id=_company.company_id,
                    title=_company.title,
                    url=_company.url,
                    external_url=_company.external_url,
                    logo=_company.logo,
                    major=_company.major,
                    employees_num=_company.employees_num,
                    heading=_company.heading,
                    about=_company.about
                )
                logger.info(f'Saving data for {_company.company_id} into db')
                con.execute(stmt)
        except OperationalError as e:
            logger.error(f'Failed to save data for {_company.company_id}: {type(e)}')
            raise ApplicationError()


