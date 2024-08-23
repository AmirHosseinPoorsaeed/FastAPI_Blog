import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime

from src.db.main import Base


Blog = 'src.blog.models.Blog'


class Tag(Base):
    __tablename__ = 'tags'

    uid = Column(
        pg.UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    title = Column(String, unique=True)
    datetime_created = Column(
        pg.TIMESTAMP, default=datetime.now()
    )
    datetime_updated = Column(
        pg.TIMESTAMP, default=datetime.now()
    )

    blogs = relationship(
        Blog, secondary='blog_tags', back_populates='tags', lazy='selectin'
    )

    def __repr__(self):
        return f'<Tag {self.title}>'


class BlogTag(Base):
    __tablename__ = 'blog_tags'

    blog_uid = Column(
        pg.UUID, ForeignKey('blogs.uid'), primary_key=True, default=None
    )
    tag_uid = Column(
        pg.UUID, ForeignKey('tags.uid'), primary_key=True, default=None
    )
