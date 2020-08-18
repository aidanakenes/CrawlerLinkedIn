from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.exc import OperationalError, IntegrityError

from src.models.user import User
from src.saver.db.tables import UserTable, EducationTable, ExperienceTable, SkillTable, Base
from src.utils.conf import Postgres
from src.utils.logger import get_logger
from src.utils.err_utils import ApplicationError

logger = get_logger(__name__)
Session = sessionmaker()


class Saver:

    def __init__(self):
        self._engine = create_engine(Postgres.ENGINE)
        self._meta = MetaData(self._engine)
        Session.configure(bind=self._engine)
        self.session = Session()

        self._table_user = UserTable
        self._table_education = EducationTable
        self._table_experience = ExperienceTable
        self._table_skills = SkillTable
        Base.metadata.create_all(self._engine, Base.metadata.tables.values(), checkfirst=True)

    def insert_user(self, user: User):
        try:
            stmt = UserTable(
                user_id=user.user_id,
                user_url=user.user_url,
                fullname=user.fullname,
                profile_pic_url=user.profile_pic_url,
                location=user.location,
                heading=user.heading
            )
            self.session.add(stmt)
            logger.info(f'Saving data for {user.user_id} into db')
            self.session.commit()
            self.insert_relation(EducationTable, user.user_id, user.education)
            self.insert_relation(ExperienceTable, user.user_id, user.experience)
            self.insert_relation(SkillTable, user.user_id, user.skill)
        except OperationalError as e:
            logger.error(f'Failed to save data for {user.user_id}: {type(e)}')
            raise ApplicationError()
        except IntegrityError:
            logger.warn(f'User {user.user_id} has already exist in the database')
            pass

    def insert_relation(self, table: Base, user_id: str, records: List):
        print(table)
        if table is SkillTable:
            rows = [SkillTable(user_id=user_id, skill_name=record) for record in records]
        else:
            rows = [table(user_id=user_id, **record.dict()) for record in records]
        self.session.bulk_save_objects(rows)
        self.session.commit()
