from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    company_name: str
    date: datetime
    content: str
