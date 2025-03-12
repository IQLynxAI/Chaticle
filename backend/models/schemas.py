from pydantic import BaseModel

class ContentRequest(BaseModel):
    content: str

class QuestionRequest(BaseModel):
    question: str
