import os
import sys
import pytest
import asyncio
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

app_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app'
)
sys.path.insert(0, app_dir)


from app import models
from app.core.db import Base
from app.crud import AnswerRepository, QuestionRepository
from app.api.v1.dependencies import get_uow

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Тестовый движок БД"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Тестовая сессия"""
    async_session = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    yield async_session

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest.fixture
def test_app():
    from app.api.v1.router import api_router

    test_app = FastAPI()
    test_app.include_router(api_router)
    return test_app


@pytest.fixture
async def client(test_session, test_app):

    class TestUnitOfWork:
        def __init__(self):
            self.session_factory = test_session

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

    def get_test_uow():
        return TestUnitOfWork()

    test_app.dependency_overrides[get_uow] = get_test_uow

    with TestClient(app=test_app) as client:
        yield client
