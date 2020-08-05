from typing import Optional

from pydantic import BaseModel


class Education(BaseModel):
    school: Optional[str]
    degree: Optional[str]
    start: Optional[int]
    end: Optional[int]
