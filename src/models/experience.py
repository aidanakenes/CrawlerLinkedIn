from typing import Optional

from pydantic import BaseModel


class Experience(BaseModel):
    company: str
    position: str
    start: Optional[int]
    end: Optional[int]
