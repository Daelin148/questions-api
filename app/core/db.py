from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

DATABASE_URL = (
    f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@' # noqa
    f'{settings.postgres_server}:5432/{settings.postgres_db}'
)

engine = create_async_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
