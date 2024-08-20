from typing import Annotated
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import UserService
from src.auth.utils import decode_token
from src.config import Config
from src.db.main import get_session


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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme."
            )

        if not self.valid_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token is invalid or expired'
            )

        print(token_data)

        self.verify_token_data(token_data)

        return token_data

    def valid_token(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please provide a valid access token'
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please provide a valid refresh token'
            )


async def get_current_user(
    token: Annotated[dict, Depends(AccessTokenBearer())],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    print(token)
    username = token.get('sub')
    user = await user_service.get_user_by_username(username, db)

    return user
