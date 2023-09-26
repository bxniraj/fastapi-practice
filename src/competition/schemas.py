from pydantic import BaseModel
from datetime import date

class Competition(BaseModel):
    id: int
    name: str
    description: str
    start_date: date
    end_date: date
    prize: bool
    user_id: int
    