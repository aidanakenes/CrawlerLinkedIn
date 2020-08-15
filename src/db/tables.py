from sqlalchemy import Column, String, INT, ForeignKey, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    fullname = Column(String)
    profile_pic_url = Column(String)
    location = Column(String)
    heading = Column(String)


class EducationTable(Base):
    __tablename__ = 'education'
    no_pk = Column(INT, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    school = Column(String)
    degree = Column(VARCHAR)
    start = Column(INT)
    end = Column(INT)


class ExperienceTable(Base):
    __tablename__ = 'experience'
    no_pk = Column(INT, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    company = Column(String)
    position = Column(VARCHAR)
    start = Column(INT)
    end = Column(INT)


class SkillTable(Base):
    __tablename__ = 'skill'
    no_pk = Column(INT, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    skill_name = Column(String)
