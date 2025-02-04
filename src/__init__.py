from fastapi import FastAPI

from src.auth.routers import auth_router
from src.blog.routers import blog_router
from src.errors import register_all_errors
from src.reviews.routers import review_router
from src.tags.routers import tags_router


version = 'v1'

app = FastAPI(
    title='Blog',
    description='A REST API for a blog service',
    version=version
)

register_all_errors(app)

app.include_router(
    auth_router,
    prefix=f'/api/{version}/auth',
    tags=['auth']
)

app.include_router(
    blog_router,
    prefix=f'/api/{version}/blog',
    tags=['blog']
)

app.include_router(
    review_router,
    prefix=f'/api/{version}/reviews',
    tags=['reviews']
)

app.include_router(
    tags_router,
    prefix=f'/api/{version}/tags',
    tags=['tags']
)
