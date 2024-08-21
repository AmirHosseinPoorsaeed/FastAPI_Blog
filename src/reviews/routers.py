from fastapi import APIRouter, status, HTTPException, Depends
from typing import Annotated, List
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.db.main import get_session
from src.reviews.schemas import ReviewCreateRequest, ReviewDetailModel, ReviewShowModel
from src.reviews.service import ReviewService


review_router = APIRouter()

db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[User, Depends(get_current_user)]
review_service = ReviewService()


@review_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ReviewDetailModel]
)
async def get_all_reviews(
    db: db_dependency
):
    reviews = await review_service.get_all_reviews(db)
    return reviews


@review_router.get(
    '/{review_uid}',
    status_code=status.HTTP_200_OK,
    response_model=ReviewDetailModel
)
async def get_review(
    review_uid: str,
    db: db_dependency
):
    review = await review_service.get_review_by_uid(review_uid, db)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Review not found'
        )

    return review


@review_router.post(
    '/blogs/{blog_slug}',
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewShowModel
)
async def create_review_for_blog(
    blog_slug: str,
    review_request: ReviewCreateRequest,
    user: user_dependency,
    db: db_dependency
):
    new_review = await review_service.add_review_to_blog(
        review_request, blog_slug, user, db
    )
    return new_review


@review_router.delete(
    '/{review_uid}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_review(
    review_uid: str,
    user: user_dependency,
    db: db_dependency
):
    await review_service.delete_review(
        review_uid, user, db
    )
    return JSONResponse(
        content={
            'message': 'Review successfully deleted.'
        }
    )
