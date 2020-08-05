from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    company_id: str
    date: datetime
    content: str
