from pydantic import BaseModel


class Education(BaseModel):
    school: str
    degree: str
    start: int
    end: int
