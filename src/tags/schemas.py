import uuid
from datetime import datetime
from typing import List
from pydantic import BaseModel


class TagShowModel(BaseModel):
    uid: uuid.UUID
    title: str
    datetime_created: datetime


class TagCreateRequest(BaseModel):
    title: str


class TagAddRequest(BaseModel):
    tags: List[TagCreateRequest]
