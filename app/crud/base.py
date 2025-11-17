from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy import Select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta

T = TypeVar('T', bound=DeclarativeMeta)


class BaseRepository(Generic[T], ABC):

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.model = model
        self.session = session

    async def add_one(self, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_one(self, **kwargs) -> T | None:
        res = await self.session.scalar(
            self._get_stmt().filter_by(**kwargs)
        )
        return res

    async def filter_by(self, **kwargs) -> list[T]:
        res = await self.session.scalars(
            self._get_stmt().filter_by(**kwargs)
        )
        return res.all()

    async def get_all(self) -> list[T]:
        res = await self.session.scalars(
            self._get_stmt()
        )
        return res.all()

    async def delete_one(self, obj: T) -> None:
        await self.session.delete(obj)

    @abstractmethod
    def _get_stmt(self) -> Select:
        pass
