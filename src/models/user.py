from typing import Optional, List

from pydantic import BaseModel


class User(BaseModel):
    full_name: str
    user_url: str
    profile_pic_url: Optional[str]
    location: str
    heading: Optional[str]
    education: List[dict]
    experience: List[dict]
    skills: List[str]
