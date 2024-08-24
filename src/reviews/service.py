from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from src.auth.models import User
from src.errors import BlogNotFound, UserNotFound
from src.reviews.models import Review
from src.auth.service import UserService
from src.blog.service import BlogService
from src.reviews.schemas import ReviewCreateRequest


user_service = UserService()
blog_service = BlogService()


class ReviewService:
    async def get_all_reviews(
        self, db: AsyncSession
    ):
        reviews = await db.execute(select(Review))
        return reviews.scalars().all()

    async def get_review_by_uid(
        self, review_uid: str, db: AsyncSession
    ):
        review = await db.execute(select(Review).where(Review.uid == review_uid))
        return review.scalars().first()

    async def add_review_to_blog(
        self,
        review_request: ReviewCreateRequest,
        blog_slug: str,
        user: User,
        db: AsyncSession
    ):
        username = user.username
        blog = await blog_service.get_blog_by_slug(blog_slug, db)
        user = await user_service.get_user_by_username(username, db)

        if not user:
            raise UserNotFound()

        if not blog:
            raise BlogNotFound()

        new_reviewe = Review(
            **review_request.model_dump(),
            author_uid=user.uid,
            blog_uid=blog.uid
        )
        db.add(new_reviewe)
        await db.commit()
        await db.refresh(new_reviewe)
        return new_reviewe

    async def delete_review(
        self, review_uid: str, user: User, db: AsyncSession
    ):
        review = await self.get_review_by_uid(review_uid, db)

        if not review or (review.author != user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Cannot delete this review'
            )

        await db.delete(review)
        await db.commit()
