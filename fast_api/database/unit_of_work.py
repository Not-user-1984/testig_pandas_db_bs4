from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .models.trading import Base
from core.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# @asynccontextmanager
# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

class UnitOfWork:
    def __init__(self):
        self.session_maker = async_session

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
