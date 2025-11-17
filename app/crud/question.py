from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import BaseRepository
from app.models import Question


class QuestionRepository(BaseRepository[Question]):

    def __init__(self, session: AsyncSession):
        return super().__init__(session, Question)

    async def get_with_detail(self, id: int):
        stmt = self._get_stmt().where(self.model.id == id).options(
            selectinload(self.model.answers)
        )
        res = await self.session.scalar(stmt)
        return res

    def _get_stmt(self) -> Select:
        return select(self.model)
