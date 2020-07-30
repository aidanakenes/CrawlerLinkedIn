from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    full_name: str
    location: str
    heading: Optional[str]
    education: Optional[List[dict]]
    experience: Optional[List[dict]]
    skills: Optional[List[dict]]
    profile_pic_url: Optional[str]
    user_url: str
