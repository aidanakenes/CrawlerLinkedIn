from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from src.models.user import User, Education, Experience
from src.saver.db.scheme import UserTable, EducationTable, ExperienceTable, SkillTable, Base
from src.utils.conf import Postgres
from src.utils.logger import get_logger

logger = get_logger(__name__)
Session = sessionmaker()


class Searcher:

    def __init__(self):
        self._engine = create_engine(Postgres.ENGINE)
        self._meta = MetaData(self._engine)
        Session.configure(bind=self._engine)
        self.session = Session()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        result = self.session.query(UserTable).filter_by(user_id=user_id).first()
        if result:
            record = result.__dict__
            education = []
            experience = []
            skill = []
            for relation_record in self.get_relation(EducationTable, user_id):
                education.append(Education(**relation_record))
            for relation_record in self.get_relation(ExperienceTable, user_id):
                experience.append(Experience(**relation_record))
            for relation_record in self.get_relation(SkillTable, user_id):
                skill.append(relation_record['skill_name'])
            return User(
                user_id=record['user_id'],
                user_url=record['user_url'],
                fullname=record['fullname'],
                profile_pic_url=record['profile_pic_url'],
                location=record['location'],
                heading=record['heading'],
                education=education,
                experience=experience,
                skill=skill
            )

    def get_relation(self, table: Base, user_id: str):
        """
            Get records from the given relational table
        """
        records = self.session.query(table).filter(table.user_id == user_id).all()
        for record in records:
            yield record.__dict__

    def get_users_by_fullname(self, fullname: str) -> Optional[List[User]]:
        users = []
        fullname = fullname.lower().split()
        records = self.session.query(UserTable.user_id, UserTable.fullname).all()
        for record in records:
            fullname_from_db = [word.lower() for word in str(record[1]).split()]
            fullname_from_db = " ".join(fullname_from_db)
            if all(word in fullname_from_db for word in fullname):
                users.append(self.get_user_by_id(record[0]))
        return users

