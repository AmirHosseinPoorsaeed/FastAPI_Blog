from fastapi import FastAPI

from src.auth.routers import auth_router
from src.blog.routers import blog_router
from src.reviews.routers import review_router


version = 'v1'

app = FastAPI(
    title='Blog',
    description='A REST API for a blog service',
    version=version
)

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
    prefix=f'/api/{version}/review',
    tags=['review']
)
