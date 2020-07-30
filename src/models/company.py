from typing import Optional, List

from pydantic import BaseModel

from src.models.post import Post


class Company(BaseModel):
    title: str
    heading: Optional[str]
    external_url: Optional[str]
    location: Optional[str]
    employees_num: Optional[int]
    followers_num: Optional[int]
    posts: List[Post]
    url: str
    profile_pic_url: Optional[str]
