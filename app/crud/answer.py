from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import BaseRepository
from app.models import Answer


class AnswerRepository(BaseRepository[Answer]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Answer)

    async def get_with_detail(self, id: int):
        stmt = self._get_stmt().where(self.model.id == id).options(
            joinedload(self.model.question)
        )
        res = await self.session.scalar(stmt)
        return res

    def _get_stmt(self) -> Select:
        return select(self.model)
