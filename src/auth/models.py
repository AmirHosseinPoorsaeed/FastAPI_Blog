import uuid
from sqlalchemy import Column, String, Boolean
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from sqlalchemy.orm import relationship

from src.db.main import Base


Blog = 'src.blog.models.Blog'


class User(Base):
    __tablename__ = 'users'

    uid = Column(
        pg.UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(String, default='user')
    datetime_created = Column(
        pg.TIMESTAMP, default=datetime.now()
    )
    datetime_updated = Column(
        pg.TIMESTAMP, default=datetime.now()
    )

    blogs = relationship(Blog, back_populates='author', lazy='selectin')

    def __repr__(self):
        return f'<User {self.username}>'
