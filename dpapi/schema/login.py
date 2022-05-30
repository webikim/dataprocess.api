from typing import Union

from pydantic import BaseModel


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
