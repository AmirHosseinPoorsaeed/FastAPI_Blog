from datetime import date, datetime
from pydantic import BaseModel

from src.auth.schemas import UserShowModel


class BlogShowModel(BaseModel):
    title: str
    description: str
    slug: str
    publish_date: date
    datetime_created: datetime
    datetime_updated: datetime


class BlogDetailModel(BlogShowModel):
    author: 'UserShowModel'


class BlogCreateRequest(BaseModel):
    title: str
    description: str
    slug: str
    publish_date: str


class BlogUpdateRequest(BaseModel):
    title: str
    description: str
