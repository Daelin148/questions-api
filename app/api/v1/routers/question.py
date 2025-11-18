from typing import Annotated

from fastapi import APIRouter, Path, status

from app.api.v1.dependencies import QuestionDep, UOWDep, QuestionId
from app.schemas import (AnswerCreate, QuestionBase, QuestionCreate,
                         QuestionDetail)
from app.services import AnswerService, QuestionService

router = APIRouter()


@router.get('/', response_model=list[QuestionBase])
async def get_questions(
    uow: UOWDep
) -> list[QuestionBase]:
    """Вывод информации о вопросах."""
    questions = await QuestionService().get_questions(uow)
    return questions


@router.post(
    '/', response_model=QuestionBase, status_code=status.HTTP_201_CREATED
)
async def create_question(
    uow: UOWDep,
    question_data: QuestionCreate
) -> QuestionBase:
    """Создание вопроса."""
    question = await QuestionService().create_question(uow, question_data)
    return question


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    id: QuestionId,
    uow: UOWDep
):
    """Удаление вопроса."""
    await QuestionService().delete_question(uow, id)


@router.post(
    '/{id}/answers', status_code=status.HTTP_201_CREATED
)
async def create_answer(
    question_db: QuestionDep,
    answer_data: AnswerCreate,
    id: QuestionId,
    uow: UOWDep,
):
    """Создание ответа к вопросу."""
    answer = await AnswerService().create_answer(uow, id, answer_data)
    return answer


@router.get('/{id}', response_model=QuestionDetail)
async def get_question(
    id: QuestionId,
    uow: UOWDep,
    question_db: QuestionDep
) -> QuestionDetail:
    """Вывод информации о вопросе."""
    question = await QuestionService().get_question(uow, id)
    return question
