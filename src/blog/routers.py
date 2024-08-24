from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.blog.schemas import BlogCreateRequest, BlogDetailModel, BlogUpdateRequest, BlogShowModel
from src.blog.service import BlogService
from src.db.main import get_session
from src.errors import BlogNotFound


blog_router = APIRouter()

blog_service = BlogService()
db_dependency = Annotated[AsyncSession, Depends(get_session)]
user_dependency = Annotated[User, Depends(get_current_user)]


@blog_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[BlogDetailModel]
)
async def get_all_blogs(
    db: db_dependency
):
    blogs = await blog_service.get_all_blogs(db)
    return blogs


@blog_router.get(
    '/user_blogs',
    status_code=status.HTTP_200_OK,
    response_model=List[BlogDetailModel]
)
async def get_user_blogs(
    db: db_dependency,
    user: user_dependency
):
    blogs = await blog_service.get_user_blogs(user, db)
    return blogs


@blog_router.get(
    '/{blog_slug}',
    status_code=status.HTTP_200_OK,
    response_model=BlogDetailModel
)
async def get_blog(
    blog_slug: str,
    db: db_dependency
):
    blog = await blog_service.get_blog_by_slug(blog_slug, db)

    if not blog:
        raise BlogNotFound()

    return blog


@blog_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=BlogDetailModel
)
async def create_blog(
    blog_request: BlogCreateRequest,
    user: user_dependency,
    db: db_dependency,
):
    blog = await blog_service.create_blog(
        blog_request, user.uid, db
    )
    return blog


@blog_router.put(
    '/{blog_slug}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BlogDetailModel
)
async def update_blog(
    blog_slug: str,
    blog_update_request: BlogUpdateRequest,
    user: user_dependency,
    db: db_dependency,
):
    blog = await blog_service.update_blog(
        blog_slug, blog_update_request, db
    )

    if not blog:
        raise BlogNotFound()

    return blog


@blog_router.delete(
    '/{blog_slug}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_blog(
    blog_slug: str,
    user: user_dependency,
    db: db_dependency
):
    await blog_service.delete_blog(blog_slug, db)

    return JSONResponse(
        content={
            'message': 'Blog successfully deleted'
        }
    )
