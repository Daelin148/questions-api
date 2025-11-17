from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from app.utils.unitofwork import UnitOfWork


async def get_uow() -> UnitOfWork:
    """Зависимость для получения UnitOfWork"""
    return UnitOfWork()


UOWDep = Annotated[UnitOfWork, Depends(get_uow)]


async def valid_question_id(
    uow: UOWDep,
    id: Annotated[int, Path(gt=0, description='Идентификатор вопроса')]
) -> int:
    async with uow:
        question = await uow.questions.get_one(id=id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Вопрос с идентификатором {id} не найден'
            )
        return question.id


async def valid_answer_id(
    uow: UOWDep,
    id: Annotated[int, Path(gt=0, description='Идентификатор ответа')]
) -> int:
    async with uow:
        answer = await uow.answers.get_one(id=id)
        if not answer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Ответ с идентификатором {id} не найден'
            )
        return answer.id


QuestionDep = Annotated[int, Depends(valid_question_id)]

AnswerDep = Annotated[int, Depends(valid_answer_id)]
