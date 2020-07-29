from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    full_name: str
    location: str
    heading: Optional[str]
    education: Optional[list]
    experience: Optional[list]
    skills: Optional[list]
    profile_pic_url: Optional[str]
    user_url: str
