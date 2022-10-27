from typing import Optional

from pydantic import BaseModel, validator
from sanic import exceptions


class UserSignUpSchema(BaseModel):
    username: str
    password1: str
    password2: str

    @validator("username")
    def empty_username(cls, username):
        if not username:
            raise exceptions.BadRequest("Username cannot be empty")
        return username

    @validator("password1")
    def empty_password(cls, password1):
        if not password1:
            raise exceptions.BadRequest("Password cannot be empty")
        return password1

    @validator("password2")
    def passwords_match(cls, password2, values):
        if password2 != values["password1"]:
            raise exceptions.BadRequest("Passwords do not match")
        return password2


class UserSignInSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
