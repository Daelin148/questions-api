from .answer import AnswerBase, AnswerCreate, AnswerDetail
from .question import QuestionBase, QuestionCreate, QuestionDetail

__all__ = [
    'AnswerBase',
    'AnswerCreate',
    'AnswerDetail',
    'QuestionBase',
    'QuestionCreate',
    'QuestionDetail'
]

AnswerDetail.model_rebuild()
QuestionDetail.model_rebuild()
