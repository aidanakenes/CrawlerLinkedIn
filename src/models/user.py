from typing import Optional, List

from pydantic import BaseModel

from src.models.education import Education
from src.models.experience import Experience


class User(BaseModel):
    user_id: str
    full_name: str
    user_url: str
    profile_pic_url: Optional[str]
    location: str
    heading: Optional[str]
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
