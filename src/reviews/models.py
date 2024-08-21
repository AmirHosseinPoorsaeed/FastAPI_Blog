from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, CheckConstraint
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.orm import relationship

from src.db.main import Base


User = 'src.auth.models.User'
Blog = 'src.blog.models.Blog'


class Review(Base):
    __tablename__ = 'reviews'

    uid = Column(
        pg.UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    body = Column(String, nullable=False)
    rating = Column(Integer, nullable=True, default=1)
    datetime_created = Column(
        pg.TIMESTAMP, default=datetime.now()
    )
    datetime_updated = Column(
        pg.TIMESTAMP, default=datetime.now()
    )

    author_uid = Column(pg.UUID, ForeignKey('users.uid'), nullable=False)
    blog_uid = Column(pg.UUID, ForeignKey('blogs.uid'), nullable=False)

    author = relationship(User, back_populates='reviews', lazy='selectin')
    blog = relationship(Blog, back_populates='reviews', lazy='selectin')

    __table_args__ = (
        CheckConstraint('rating >= 1', name='check_rating_min'),
        CheckConstraint('rating <= 5', name='check_rating_max'),
    )

    def __repr__(self):
        return f'<Review {self.body} from {self.author_uid} for {self.blog_uid}>'

