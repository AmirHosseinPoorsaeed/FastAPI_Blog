from fastapi import FastAPI

from src.auth.routers import auth_router


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
