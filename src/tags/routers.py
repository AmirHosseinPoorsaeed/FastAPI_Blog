from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List

from src.db.main import get_session
from src.tags.schemas import TagAddRequest, TagCreateRequest, TagShowModel
from src.tags.service import TagService


tags_router = APIRouter()
tag_service = TagService()
db_dependency = Annotated[AsyncSession, Depends(get_session)]


@tags_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[TagShowModel]
)
async def get_all_tags(
    db: db_dependency
):
    tags = await tag_service.get_tags(db)
    return tags


@tags_router.get(
    '/{tag_uid}',
    status_code=status.HTTP_200_OK,
    response_model=TagShowModel
)
async def get_tag(
    tag_uid: str,
    db: db_dependency
):
    tag = await tag_service.get_tag_by_uid(tag_uid, db)
    return tag


@tags_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TagShowModel
)
async def create_tag(
    tag_request: TagCreateRequest,
    db: db_dependency
):
    new_tag = await tag_service.create_tag(tag_request, db)
    return new_tag


@tags_router.post(
    'blogs/{blog_slug}/tags',
    status_code=status.HTTP_201_CREATED,
)
async def add_tag_to_blog(
    blog_slug: str,
    tag_request: TagAddRequest,
    db: db_dependency
):
    blog_with_tag = await tag_service.add_tag_to_blog(
        blog_slug, tag_request, db
    )

    return blog_with_tag


@tags_router.put(
    '/{tag_uid}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TagShowModel
)
async def update_tag(
    tag_uid: str,
    tag_update_request: TagCreateRequest,
    db: db_dependency
):
    tag = await tag_service.update_tag(tag_uid, tag_update_request, db)
    return tag


@tags_router.delete(
    '/{tag_uid}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_tag(
    tag_uid: str,
    db: db_dependency
):
    await tag_service.delete_tag(tag_uid, db)
    return JSONResponse(
        content={
            'message': 'Tag successfully deleted'
        }
    )
