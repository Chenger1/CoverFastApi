from pydantic import BaseModel, EmailStr


class MainPageSchema(BaseModel):
    page_name: str  #: Text above menu
    title: str
    text: str


class FeatureSchema(BaseModel):
    title: str
    text: str
    tags: list


class UserSchema(BaseModel):
    username: str
    email: EmailStr


class CreateUserSchema(UserSchema):
    password: str


class ContactsSchema(BaseModel):
    email: EmailStr
    phone_number: str
    address: str
