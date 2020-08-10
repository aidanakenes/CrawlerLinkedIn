from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String, INT, ForeignKey, VARCHAR
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
        self.table = Table('users', self._metadata,
                           Column('user_id', String, primary_key=True),
                           Column('full_name', String),
                           Column('profile_pic_url', String),
                           Column('location', String),
                           Column('heading', String)
                           )
        self._table_education = Table('education', self._metadata,
                                      Column('user_id', String, ForeignKey("users.user_id"), nullable=False),
                                      Column('school', String),
                                      Column('degree', VARCHAR),
                                      Column('start', INT),
                                      Column('end', INT)
                                      )
        self._table_experience = Table('experience', self._metadata,
                                       Column('user_id', String, ForeignKey("users.user_id"), nullable=False),
                                       Column('company', VARCHAR),
                                       Column('position', VARCHAR),
                                       Column('start', INT),
                                       Column('end', INT)
                                       )
        self._table_skills = Table('skills', self._metadata,
                                   Column('user_id', String, ForeignKey("users.user_id"), nullable=False),
                                   Column('skill_name', String)
                                   )

        if not self._engine.has_table('users'):
            self.table.create()
        if not self._engine.has_table('education'):
            self._table_education.create()
        if not self._engine.has_table('experience'):
            self._table_experience.create()
        if not self._engine.has_table('skills'):
            self._table_skills.create()

    def insert_user(self, user: User):
        try:
            with self._engine.connect() as con:
                stmt = self.table.insert().values(
                    user_id=user.user_id,
                    full_name=user.fullname,
                    profile_pic_url=user.profile_pic_url,
                    location=user.location,
                    heading=user.heading
                )
                logger.info(f'Saving data for {user.user_id} into db')
                con.execute(stmt)
            self.insert_relations(user)
        except OperationalError as e:
            logger.error(f'Failed to save data for {user.user_id}: {type(e)}')
            raise ApplicationError()
        except Exception:
            print('Oops')
            pass

    def insert_relations(self, user: User):
        try:
            with self._engine.connect() as con:
                logger.info(f'Saving education, experience, skills data for {user.user_id} into db')
                for edu in user.education:
                    stmt = self._table_education.insert().values(
                        user_id=user.user_id,
                        school=edu.school,
                        degree=edu.degree,
                        start=edu.start,
                        end=edu.end
                    )
                    con.execute(stmt)
                for exp in user.experience:
                    stmt = self._table_experience.insert().values(
                        user_id=user.user_id,
                        company=exp.company,
                        position=exp.position,
                        start=exp.start,
                        end=exp.end
                    )
                    con.execute(stmt)
                for skill in user.skills:
                    stmt = self._table_skills.insert().values(
                        user_id=user.user_id,
                        skill_name=skill
                    )
                    con.execute(stmt)

        except OperationalError as e:
            logger.error(f'Failed to save education, experience, skills data for {user.user_id}: {type(e)}')
            raise ApplicationError()
        except Exception:
            print('Oops')
            pass
