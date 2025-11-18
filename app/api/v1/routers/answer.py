from typing import Annotated

from fastapi import APIRouter, Path, status

from app.api.v1.dependencies import AnswerDep, UOWDep, AnswerId
from app.schemas import AnswerDetail
from app.services import AnswerService

router = APIRouter()


@router.get('/{id}', response_model=AnswerDetail)
async def get_answer(
    id: AnswerId,
    answer_db: AnswerDep,
    uow: UOWDep
) -> AnswerDetail:
    """Вывод информации об ответе."""
    answer = await AnswerService().get_answer(uow, id)
    return answer


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    id: AnswerId,
    uow: UOWDep
):
    await AnswerService().delete_answer(uow, id)
