from fastapi import APIRouter

from app.api.v1.routers import answer, question

api_router = APIRouter()

api_router.include_router(
    answer.router,
    prefix='/answers',
    tags=['answers']
)

api_router.include_router(
    question.router,
    prefix='/questions',
    tags=['questions']
)
