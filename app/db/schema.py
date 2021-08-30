from pydantic import BaseModel, EmailStr


class MainPageSchema(BaseModel):
    title: str
    text: str


class FeatureSchema(BaseModel):
    title: str
    text: str
    tags: list


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = True  #: By default there are no user`s except of admins


class ContactsSchema(BaseModel):
    email: EmailStr
    phone_number: str
    address: str
