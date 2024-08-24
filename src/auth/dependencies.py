from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import UserService
from src.auth.utils import decode_token
from src.config import Config
from src.db.main import get_session
from src.errors import (
    AccessTokenRequired, 
    InvalidScheme, 
    InvalidToken, 
    RefreshTokenRequired
)


JWT_SECRET = Config.JWT_SECRET
JWT_ALGORITHM = Config.JWT_ALGORITHM

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials
        scheme = credentials.scheme
        token_data = decode_token(token)

        if not scheme == 'Bearer':
            raise InvalidScheme()

        if not self.valid_token(token):
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def valid_token(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()


async def get_current_user(
    token: Annotated[dict, Depends(AccessTokenBearer())],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    username = token.get('sub')
    user = await user_service.get_user_by_username(username, db)

    return user
