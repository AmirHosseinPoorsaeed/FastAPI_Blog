from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.models import User
from src.blog.models import Blog
from src.blog.schemas import BlogCreateRequest, BlogUpdateRequest
from src.errors import BlogAlreadyExists, BlogNotFound


class BlogService:
    async def get_all_blogs(
        self, db: AsyncSession
    ):
        blogs = await db.execute(select(Blog))
        return blogs.scalars().all()

    async def get_blog_by_slug(
        self, slug: str, db: AsyncSession
    ):
        blog = await db.execute(
            select(Blog).where(Blog.slug == slug)
        )
        return blog.scalars().first()

    async def get_user_blogs(
        self, user: User, db: AsyncSession
    ):
        blogs = await db.execute(
            select(Blog).where(Blog.author_uid == user.uid)
        )
        return blogs.scalars().all()

    async def create_blog(
        self, blog_request: BlogCreateRequest, user_uid: str, db: AsyncSession
    ):
        blog = await self.get_blog_by_slug(blog_request.slug, db)

        if blog:
            raise BlogAlreadyExists()

        blog_data_dict = blog_request.model_dump()
        new_blog = Blog(
            **blog_data_dict,
            author_uid=user_uid,
        )
        new_blog.publish_date = datetime.strptime(
            blog_data_dict['publish_date'], '%Y-%m-%d'
        )

        db.add(new_blog)
        await db.commit()
        await db.refresh(new_blog)
        return new_blog

    async def update_blog(
            self, slug: str, blog_update_request: BlogUpdateRequest, db: AsyncSession
    ):
        blog = await self.get_blog_by_slug(slug, db)

        if not blog:
            raise BlogNotFound()

        blog_update_dict = blog_update_request.model_dump()

        for k, v in blog_update_dict.items():
            setattr(blog, k, v)

        db.add(blog)
        await db.commit()
        await db.refresh(blog)
        return blog

    async def delete_blog(
        self, slug: str, db: AsyncSession
    ):
        blog = await self.get_blog_by_slug(slug, db)

        if not blog:
            raise BlogNotFound()

        if blog is not None:
            await db.delete(blog)
            await db.commit()
            return {}
        else:
            return None
