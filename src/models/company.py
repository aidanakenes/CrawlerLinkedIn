from typing import Optional, List

from pydantic import BaseModel


class Company(BaseModel):
    company_id: str
    title: str
    url: str
    external_url: Optional[str]
    logo: Optional[str]
    major: Optional[str]
    employees_num: Optional[int]
    locations: List[str]
    heading: Optional[str]
    about: Optional[str]
