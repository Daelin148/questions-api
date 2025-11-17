from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class AnswerCreate(BaseModel):
    user_id: Annotated[
        UUID, Field(..., description='Идентификатор пользователя')
    ]
    text: Annotated[str, Field(..., min_length=5, description='Текст ответа')]


class AnswerBase(AnswerCreate):
    id: Annotated[int, Field(description='Идентификатор ответа')]
    created_at: Annotated[datetime, Field(..., description='Дата создания')]
    question_id: Annotated[PositiveInt, Field(
        ..., description='Идентификатор вопроса'
    )]

    model_config = ConfigDict(
        from_attributes=True
    )


class AnswerDetail(AnswerBase):
    question: Annotated['QuestionBase', Field(description='Вопрос')]
