from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from typing import Annotated

from src.auth.models import User
from src.auth.utils import create_access_token, generate_password_hash, verify_password
from src.db.main import get_session
from src.config import Config
from src.auth.schemas import UserChangePasswordRequest, UserCreateRequest, UserDetailModel, UserLoginModel
from src.auth.service import UserService
from src.auth.dependencies import RefreshTokenBearer, get_current_user
from src.errors import (
    InvalidCredantials,
    InvalidToken,
    PasswordIncorrect,
    PasswordNotMatch,
    UserAlreadyExists
)


auth_router = APIRouter()

db_dependency = Annotated[AsyncSession,
                          Depends(get_session)]
user_service = UserService()


@auth_router.post(
    '/login',
    status_code=status.HTTP_200_OK
)
async def login_for_access_token(
    login_request: UserLoginModel,
    db: db_dependency
):
    user = await user_service.get_user_by_username(login_request.username, db)

    if not user or not verify_password(login_request.password, user.hashed_password):
        raise InvalidCredantials()

    access_token = create_access_token(
        username=user.username,
        role=user.role
    )
    refresh_token = create_access_token(
        username=user.username,
        role=user.role,
        refresh=True,
        expires_delta=timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DATES)
    )

    return JSONResponse(
        content={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer'
        }
    )


@auth_router.post(
    '/signup',
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetailModel
)
async def create_user_account(
    user_request: UserCreateRequest,
    db: db_dependency
):
    email = user_request.email
    username = user_request.username
    user = await user_service.user_exists(
        username, email, db
    )

    if user:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_request, db)

    return new_user


@auth_router.get(
    '/refresh_token',
    status_code=status.HTTP_200_OK
)
async def get_new_access_token(
    token_data: Annotated[dict, Depends(RefreshTokenBearer())]
):
    expiry_time = token_data.get('exp')

    if datetime.fromtimestamp(expiry_time) > datetime.now():
        new_access_token = create_access_token(
            token_data.get('sub'),
            token_data.get('role')
        )

        return JSONResponse(
            content={
                'access_token': new_access_token
            }
        )

    raise InvalidToken()


@auth_router.post(
    '/change_password',
    status_code=status.HTTP_200_OK
)
async def change_account_password(
    user_request: UserChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: db_dependency
):
    old_password = user_request.old_password
    new_password = user_request.new_password
    confirm_new_password = user_request.confirm_new_password

    if not verify_password(old_password, current_user.hashed_password):
        raise PasswordIncorrect()

    if not new_password == confirm_new_password:
        raise PasswordNotMatch()

    hashed_password = generate_password_hash(new_password)
    await user_service.update_user(
        current_user, {'hashed_password': hashed_password}, db
    )

    return JSONResponse(
        content={
            'message': 'Password has been changed successfully',
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=UserDetailModel
)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
