from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists

from app.core.config import settings
from app.models.base import Base

engine_test = create_async_engine(settings.test_url_for_engine, poolclass=NullPool)

if not database_exists(settings.test_url):
    create_database(settings.test_url)

async_session_maker = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()
