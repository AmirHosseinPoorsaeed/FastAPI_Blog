from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.blog.service import BlogService
from src.errors import BlogNotFound, TagAlreadyExists, TagNotFound
from src.tags.models import Tag
from src.tags.schemas import TagAddRequest, TagCreateRequest


blog_service = BlogService()


class TagService:
    async def get_tags(
        self, db: AsyncSession
    ):
        tags = await db.execute(select(Tag))
        return tags.scalars().all()

    async def get_tag_by_uid(
        self, tag_uid: str, db: AsyncSession
    ):
        tag = await db.execute(select(Tag).where(Tag.uid == tag_uid))
        return tag.scalars().first()

    async def create_tag(
        self, tag_request: TagCreateRequest, db: AsyncSession
    ):
        result = await db.execute(
            select(Tag).where(Tag.title == tag_request.title)
        )
        tag = result.scalars().first()

        if tag:
            raise TagAlreadyExists()

        new_tag = Tag(**tag_request.model_dump())
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)
        return new_tag

    async def add_tag_to_blog(
        self, blog_slug: str, tag_request: TagAddRequest, db: AsyncSession
    ):
        blog = await blog_service.get_blog_by_slug(blog_slug, db)

        if not blog:
            raise BlogNotFound()

        for tag_item in tag_request.tags:
            result = await db.execute(
                select(Tag).where(Tag.title == tag_item.title)
            )
            tag = result.scalars().first()

            if not tag:
                tag = Tag(title=tag_item.title)

            blog.tags.append(tag)

        db.add(blog)
        await db.commit()
        await db.refresh(blog)
        return blog

    async def update_tag(
        self, tag_uid: str, tag_update_request: TagCreateRequest, db: AsyncSession
    ):
        tag = await self.get_tag_by_uid(tag_uid, db)

        if not tag:
            raise TagNotFound()

        update_data_dict = tag_update_request.model_dump()

        for k, v in update_data_dict.items():
            setattr(tag, k, v)

            await db.commit()
            await db.refresh(tag)

        return tag

    async def delete_tag(
        self, tag_uid: str, db: AsyncSession
    ):
        tag = await self.get_tag_by_uid(tag_uid, db)

        if not tag:
            raise TagNotFound()

        await db.delete(tag)
        await db.commit()
