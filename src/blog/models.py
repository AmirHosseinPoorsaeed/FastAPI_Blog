import uuid
from sqlalchemy import Column, String, Date, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from sqlalchemy.orm import relationship

from src.db.main import Base


User = 'src.auth.models.User'
Review = 'src.reviews.models.Review'


class Blog(Base):
    __tablename__ = 'blogs'

    uid = Column(
        pg.UUID, index=True, primary_key=True, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    publish_date = Column(Date)
    datetime_created = Column(
        pg.TIMESTAMP, default=datetime.now()
    )
    datetime_updated = Column(
        pg.TIMESTAMP, default=datetime.now()
    )

    author_uid = Column(
        pg.UUID, ForeignKey('users.uid'), nullable=False
    )

    author = relationship(User, back_populates='blogs', lazy='selectin')
    reviews =  relationship(Review, back_populates='blog', lazy='selectin')

    def __repr__(self):
        return f'<Book {self.title}>'




