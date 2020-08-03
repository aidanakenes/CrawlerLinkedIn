from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.exc import OperationalError

from src.models.user import User
from src.utils.conf import ENGINE
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError

logger = get_logger(__name__)


class DBUser:

    def __init__(self):
        self._engine = create_engine(ENGINE, client_encoding='utf8')
        self._metadata = MetaData(self._engine)
        self._table = Table('users', self._metadata,
                            Column('user_id', String, primary_key=True),
                            Column('full_name', String),
                            Column('profile_pic_url', String),
                            Column('location', String),
                            Column('heading', String)
                            )
        if not self._engine.has_table('users'):
            self._table.create()

    def insert_user(self, _user: User):
        try:
            with self._engine.connect() as con:
                stmt = self._table.insert().values(
                    user_id=_user.user_id,
                    full_name=_user.full_name,
                    profile_pic_url=_user.profile_pic_url,
                    location=_user.location,
                    heading=_user.heading
                )
                logger.info(f'Saving data for {_user.user_id} into db')
                con.execute(stmt)
        except OperationalError as e:
            logger.error(f'Failed to save data for {_user.user_id}: {type(e)}')
            raise ApplicationError()


