from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: date

