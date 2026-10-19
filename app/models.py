from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    source: str
    page: int
    distance: float


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Source]