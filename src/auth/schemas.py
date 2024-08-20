from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class UserDetailModel(BaseModel):
    uid: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: str
    role: str
    hashed_password: str
    datetiem_created: datetime
    datetiem_updated: datetime


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
