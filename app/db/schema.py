from pydantic import BaseModel, EmailStr

from typing import Optional


class MainPageSchema(BaseModel):
    page_name: str  #: Text above menu
    title: str
    text: str


class FeatureSchema(BaseModel):
    title: str
    text: str
    tags: Optional[list]


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class CreateUserSchema(UserSchema):
    password: str
    is_admin: Optional[bool] = True


class LogInUser(BaseModel):
    user_id: str
    is_admin: bool
    password: str


class ContactsSchema(BaseModel):
    email: EmailStr
    phone_number: str
    address: str
