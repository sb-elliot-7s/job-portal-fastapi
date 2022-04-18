from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr

from common_enums import UserTypeEnum


class RefreshToken(BaseModel):
    refresh_token: str


class Token(RefreshToken):
    access_token: str
    token_type: str


class CreateUserTypeSchema(BaseModel):
    user_type_name: UserTypeEnum


class UserTypeSchema(CreateUserTypeSchema):
    id: int


class BaseUserAccountSchema(BaseModel):
    username: Optional[str]
    email: EmailStr


class CreateUserAccountSchema(BaseUserAccountSchema):
    password: str

    @classmethod
    def as_form(cls, username: Optional[str] = Form(None), email: EmailStr = Form(...), password: str = Form(...)):
        return cls(username=username, email=email, password=password)
