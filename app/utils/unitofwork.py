from app.core.db import AsyncSessionLocal
from app.crud import AnswerRepository, QuestionRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self):
        self.session = self.session_factory()
        self.questions = QuestionRepository(self.session)
        self.answers = AnswerRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
