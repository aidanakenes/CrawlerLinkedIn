from typing import Optional

from pydantic import BaseModel


class Experience(BaseModel):
    company_id: str
    position: str
    start: int
    end: Optional[int]
