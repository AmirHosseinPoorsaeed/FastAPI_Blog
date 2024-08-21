from datetime import datetime
import uuid
from pydantic import BaseModel, Field

from src.auth.schemas import UserShowModel
from src.blog.schemas import BlogShowModel


class ReviewShowModel(BaseModel):
    uid: uuid.UUID
    body: str
    rating: int
    datetime_created: datetime


class ReviewDetailModel(ReviewShowModel):
    author: 'UserShowModel'
    blog: 'BlogShowModel'


class ReviewCreateRequest(BaseModel):
    body: str
    rating: int = Field(gt=0, le=5)
