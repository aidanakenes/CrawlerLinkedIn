from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError, IntegrityError

from src.models.user import User, Education, Experience
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
                    user_url=user.user_url,
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

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        with self._engine.connect() as con:
            stmt = self._table_user.__table__.select().where(self._table_user.user_id == user_id)
            result = con.execute(stmt)
            if result is None:
                return
            result = result.fetchall()[0]
            return User(
                user_id=user_id,
                user_url=result[1],
                fullname=result[2],
                profile_pic_url=result[3],
                location=result[4],
                heading=result[5],
                education=self.get_education(user_id),
                experience=self.get_experience(user_id),
                skill=self.get_skills(user_id)
            )

    def get_users_by_fullname(self, fullname: str) -> Optional[List[User]]:
        users = []
        fullname = [fn.lower().capitalize() for fn in fullname.split()]
        fullname = " ".join(fullname)
        with self._engine.connect() as con:
            stmt = self._table_user.__table__.select().where(
                self._table_user.fullname == fullname
            )
            result = con.execute(stmt)
            if result is None:
                return
            result = result.fetchall()
            for user in result:
                users.append(self.get_user_by_id(user[0]))
        return users

    def get_skills(self, user_id: str) -> Optional[List[str]]:
        with self._engine.connect() as con:
            stmt = self._table_user.__table__.join(
                self._table_skills,
                self._table_user.user_id == self._table_skills.user_id
            ).select().where(self._table_user.user_id == user_id)
            result = con.execute(stmt)
            result = result.fetchall()
            skills = [skill[-1] for skill in result]
        return skills

    def get_education(self, user_id) -> Optional[List[Education]]:
        education = []
        with self._engine.connect() as con:
            stmt = self._table_user.__table__.join(
                self._table_education,
                self._table_user.user_id == self._table_education.user_id
            ).select().where(self._table_user.user_id == user_id)
            result = con.execute(stmt)
            for edu in result:
                education.append(Education(
                    school=edu[-4],
                    degree=edu[-3],
                    start=edu[-2],
                    end=edu[-1]
                ))
        return education

    def get_experience(self, user_id: str) -> Optional[List[Experience]]:
        experience = []
        with self._engine.connect() as con:
            stmt = self._table_user.__table__.join(
                self._table_experience,
                self._table_user.user_id == self._table_experience.user_id
            ).select().where(self._table_user.user_id == user_id)
            result = con.execute(stmt)
            for exp in result:
                experience.append(Experience(
                    company=exp[-4],
                    position=exp[-3],
                    start=exp[-2],
                    end=exp[-1]
                ))
        return experience
