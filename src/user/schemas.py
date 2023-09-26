from typing import Optional
from pydantic import BaseModel
from datetime import date

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: date

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

