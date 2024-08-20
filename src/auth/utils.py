import jwt
from fastapi import Depends
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime

from src.config import Config
from src.db.main import get_session


JWT_SECRET = Config.JWT_SECRET
JWT_ALGORITHM = Config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
db_dependency = Annotated[AsyncSession, Depends(get_session)]


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_hash(password: str):
    return pwd_context.hash(password)


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    
    except jwt.PyJWTError as e:
        return None


def create_access_token(
    username: str, role: str, refresh: bool = False, expires_delta: timedelta | None = None
) -> str:
    
    payload = {'sub': username, 'role': role, 'refresh': refresh}
    if expires_delta:
        expires = datetime.now() + expires_delta
    else:
        expires = datetime.now() + timedelta(minutes=15)
    payload.update({'exp': expires})
    token = jwt.encode(
        payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM
    )
    return token

