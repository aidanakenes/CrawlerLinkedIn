from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from src.models.user import User, Education, Experience
from src.saver.db.tables import UserTable, EducationTable, ExperienceTable, SkillTable
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
            return User(
                user_id=record['user_id'],
                user_url=record['user_url'],
                fullname=record['fullname'],
                profile_pic_url=record['profile_pic_url'],
                location=record['location'],
                heading=record['heading'],
                education=self.get_education(user_id),
                experience=self.get_experience(user_id),
                skill=self.get_skills(user_id)
            )

    def get_users_by_fullname(self, fullname: str) -> Optional[List[User]]:
        users = []
        fullname = fullname.lower().split()
        records = self.session.query(UserTable.user_id, UserTable.fullname).all()
        for record in records:
            keywords = [word.lower() for word in str(record[1]).split()]
            keywords = " ".join(keywords)
            if all(word in keywords for word in fullname):
                users.append(self.get_user_by_id(record[0]))
        return users

    def get_skills(self, user_id: str) -> Optional[List[str]]:
        skills = []
        records = self.session.query(SkillTable.skill_name).filter(SkillTable.user_id == user_id).all()
        for record in records:
            skills.append(record[0])
        return skills

    def get_education(self, user_id) -> Optional[List[Education]]:
        education = []
        records = self.session.query(EducationTable).filter(EducationTable.user_id == user_id).all()
        for record in records:
            record = record.__dict__
            education.append(Education(
                school=record['school'],
                degree=record['degree'],
                start=record['start'],
                end=record['end']
            ))
        return education

    def get_experience(self, user_id: str) -> Optional[List[Experience]]:
        experience = []
        records = self.session.query(ExperienceTable).filter(ExperienceTable.user_id == user_id).all()
        for record in records:
            record = record.__dict__
            experience.append(Experience(
                company=record['company'],
                position=record['position'],
                start=record['start'],
                end=record['end']
            ))
        return experience
