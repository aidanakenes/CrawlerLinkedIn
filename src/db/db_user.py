from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, String, INT, ForeignKey, VARCHAR
from sqlalchemy.exc import OperationalError, IntegrityError

from src.models.user import User
from src.db.tables import UserTable, EducationTable, ExperienceTable, SkillTable
from src.utils.conf import ENGINE
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError

logger = get_logger(__name__)


class DBUser:

    def __init__(self):
        self._engine = create_engine(ENGINE, client_encoding='utf8')
        self._metadata = MetaData(self._engine)
        self._table_user = UserTable
        self._table_education = EducationTable
        self._table_experience = ExperienceTable
        self._table_skills = SkillTable

        if not self._engine.has_table('user'):
            self._table_user.__table__.create(self._engine)
        if not self._engine.has_table('education'):
            self._table_education.__table__.create(self._engine)
        if not self._engine.has_table('experience'):
            self._table_experience.__table__.create(self._engine)
        if not self._engine.has_table('skill'):
            self._table_skills.__table__.create(self._engine)

    def insert_user(self, user: User):
        try:
            with self._engine.connect() as con:
                stmt = self._table_user.__table__.insert().values(
                    user_id=user.user_id,
                    fullname=user.fullname,
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
        except IntegrityError:
            logger.warn(f'User {user.user_id} has already exist in the database')
            pass

    def insert_relations(self, user: User):
        try:
            with self._engine.connect() as con:
                logger.info(f'Saving education, experience, skills data for {user.user_id} into db')
                for edu in user.education:
                    stmt = self._table_education.__table__.insert().values(
                        user_id=user.user_id,
                        school=edu.school,
                        degree=edu.degree,
                        start=edu.start,
                        end=edu.end
                    )
                    con.execute(stmt)
                for exp in user.experience:
                    stmt = self._table_experience.__table__.insert().values(
                        user_id=user.user_id,
                        company=exp.company,
                        position=exp.position,
                        start=exp.start,
                        end=exp.end
                    )
                    con.execute(stmt)
                for skill in user.skill:
                    stmt = self._table_skills.__table__.insert().values(
                        user_id=user.user_id,
                        skill_name=skill
                    )
                    con.execute(stmt)

        except OperationalError as e:
            logger.error(f'Failed to save education, experience, skills data for {user.user_id}: {type(e)}')
            raise ApplicationError()


