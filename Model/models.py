from datetime import date
from pydantic import BaseModel
from typing import Optional, TypeVar

T = TypeVar("T")

class Ubication(BaseModel):
    cod_ubi: int
    country: str


class State(BaseModel):
    cod_state: int
    state: str


class Dates(BaseModel):
    cod_date: int
    year: int
    month: int
    day: date

class Images(BaseModel):
    cod_image: int
    cod_ubi: int
    image: str
    
class User(BaseModel):
    cod_user: Optional[T] = None
    cod_ubi: int
    cod_state: int
    username: str
    email: str
    password: str
