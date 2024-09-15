from typing import Optional, TypeVar
from pydantic import BaseModel
from datetime import date


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


class Description(BaseModel):
    cod_description: int
    description: str


class Images(BaseModel):
    cod_image: Optional[int]
    cod_ubi: int
    image: str
    uploadedat: int
    ubication: Ubication
    uploaded: Dates


class User(BaseModel):
    cod_user: Optional[int]
    cod_ubi: int
    cod_state: int
    username: str
    email: str
    password: str
    birthdate: date


class User_Dates(BaseModel):
    cod_date: int
    cod_user: int
    cod_description: int
    description: Description


class User_Retrieve(User):
    ubication: Ubication
    User_Dates: list[User_Dates]


class User_Images(BaseModel):
    cod_image: int
    cod_user: int
    description: Optional[int]
    images: Images


class UserImagesD(BaseModel):
    cod_user: int
    cod_image: int


class SignIn(BaseModel):
    username: str
    password: str


class UserSimple(BaseModel):
    cod_user: Optional[int]
    username: str
    email: str


class SignToken(BaseModel):
    token: str
    user: UserSimple
