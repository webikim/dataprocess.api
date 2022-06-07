from pydantic import BaseModel
from typing import Union


class Login(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    email: str
    full_name: Union[str, None] = None


class UserCreate(UserBase):
    password: str


class UserCheck(UserBase):
    disabled: Union[bool, None] = None


class UserInDB(UserBase):
    hashed_password: str
    disabled: Union[bool, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
