from app.schemas import QuestionBase, QuestionCreate, QuestionDetail
from app.utils.unitofwork import UnitOfWork


class QuestionService:

    async def get_question(
        self, uow: UnitOfWork, question_id: int
    ) -> QuestionDetail:
        async with uow:
            detail_question = await uow.questions.get_with_detail(
                id=question_id
            )
            return QuestionDetail.model_validate(detail_question)

    async def create_question(
        self,
        uow: UnitOfWork,
        question_data: QuestionCreate
    ) -> QuestionBase:
        async with uow:
            question = await uow.questions.add_one(question_data.model_dump())
            await uow.commit()
            return QuestionBase.model_validate(question)

    async def get_questions(self, uow: UnitOfWork) -> list[QuestionBase]:
        async with uow:
            questions = await uow.questions.get_all()
            return [
                QuestionBase.model_validate(question) for question in questions
            ]

    async def delete_question(self, uow: UnitOfWork, question_id: int):
        async with uow:
            question = await uow.questions.get_one(id=question_id)
            if not question:
                return
            await uow.questions.delete_one(question)
            await uow.commit()
