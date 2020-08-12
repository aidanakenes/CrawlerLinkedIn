from typing import Optional, List

from pydantic import BaseModel


class Education(BaseModel):
    school: Optional[str]
    degree: Optional[str]
    start: Optional[int]
    end: Optional[int]


class Experience(BaseModel):
    company: str
    position: Optional[str]
    start: Optional[int]
    end: Optional[int]


class User(BaseModel):
    user_id: str
    fullname: str
    user_url: str
    profile_pic_url: Optional[str]
    location: Optional[str]
    heading: Optional[str]
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
