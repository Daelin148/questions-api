from app.schemas import AnswerBase, AnswerCreate, AnswerDetail
from app.utils.unitofwork import UnitOfWork


class AnswerService:

    async def get_answer(
        self, uow: UnitOfWork, answer_id: int
    ) -> AnswerDetail:
        async with uow:
            answer = await uow.answers.get_with_detail(id=answer_id)
            return AnswerDetail.model_validate(answer)

    async def create_answer(
        self,
        uow: UnitOfWork,
        question_id: int,
        answer_data: AnswerCreate
    ) -> AnswerBase:
        async with uow:
            answer_data = answer_data.model_dump()
            answer_data['question_id'] = question_id
            answer = await uow.answers.add_one(answer_data)
            await uow.commit()
            return AnswerBase.model_validate(answer)

    async def delete_answer(self, uow: UnitOfWork, answer_id: int):
        async with uow:
            answer = await uow.answers.get_one(id=answer_id)
            if not answer:
                return
            await uow.answers.delete_one(answer)
            await uow.commit()
