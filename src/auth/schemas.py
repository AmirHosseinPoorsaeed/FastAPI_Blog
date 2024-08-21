import uuid
from pydantic import BaseModel, Field


class UserShowModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class UserDetailModel(UserShowModel):
    uid: uuid.UUID
    role: str
    is_active: bool


class UserCreateRequest(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=15)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6, exclude=True)


class UserChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str
