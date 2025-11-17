from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class QuestionCreate(BaseModel):
    text: Annotated[str, Field(..., min_length=5, description='Текст вопроса')]


class QuestionBase(QuestionCreate):
    id: Annotated[int, Field(description='Идентификатор вопроса')]
    created_at: Annotated[datetime, Field(..., description='Дата создания')]

    model_config = ConfigDict(
        from_attributes=True
    )


class QuestionDetail(QuestionBase):
    answers: Annotated[list['AnswerBase'], Field(description='Ответы')]
