import contextlib
from typing import Any, AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base

from src.config import Config


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initilized')
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None
    
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('DatabaseSessionManager is not initilized')
        
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise
    
    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncConnection]:
        if self._sessionmaker is None:
            raise Exception('DatabaseSessionManager is not initilized')

        session = self._sessionmaker()

        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    Config.DATABASE_URL,
    {'echo': Config.DATABASE_ECHO}
)


async def get_session():
    async with sessionmanager.session() as session:
        yield session


Base = declarative_base()
