from pydantic import BaseModel
from datetime import date

class Entry(BaseModel):
    id:int
    name: str
    title: str
    description: str
    submission_date: date
    user_id: int
    