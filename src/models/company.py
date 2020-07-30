from pydantic import BaseModel
from typing import List, Optional
from src.models.post import Post


class Company(BaseModel):
    title: str
    heading: Optional[str]
    external_url: Optional[str]
    location: Optional[str]
    employees: Optional[int]
    followers: Optional[int]
    posts: List[Post]
    url: str
    profile_pic_url: Optional[str]
