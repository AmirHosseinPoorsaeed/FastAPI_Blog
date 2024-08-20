from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.schemas import UserCreateRequest
from src.auth.models import User
from src.auth.utils import generate_password_hash


class UserService:
    async def get_user_by_username(
        self, username: str, db: AsyncSession
    ):
        user = await db.execute(
            select(User).where(User.username == username)
        )
        return user.scalars().first()

    async def user_exists(
        self, username: str, email: str, db: AsyncSession
    ):
        user = await db.execute(
            select(User).where(User.username == username, User.email == email)
        )
        return user.scalars().first()

    async def create_user(
        self, user_request: UserCreateRequest, db: AsyncSession
    ):
        user_data_dict = user_request.model_dump()
        new_user = User(
            **user_data_dict,
            hashed_password=generate_password_hash(user_request.password)
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    
    async def update_user(
        self, user: User, user_data: dict, db: AsyncSession
    ):
        for k, v in user_data.items():
            setattr(user, k, v)
        
        await db.commit()
        await db.refresh(user)
        return user 
