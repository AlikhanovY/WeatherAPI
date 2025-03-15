from datetime import datetime
from enum import nonmember

from pydantic import BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict


class WeatherModel(BaseModel):
    name: str|None
    temp: float|None
    description: str|None
    created_at: datetime|None

class UsersModel(BaseModel):

    username: str
    password: bytes
    email: EmailStr| None = None
    active: bool|None = True

class RegisterModel(BaseModel):
    username: str
    password: str
