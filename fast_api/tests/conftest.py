import pytest_asyncio
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database.unit_of_work import DATABASE_URL


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
        )
    async with async_session() as session:
        yield session
