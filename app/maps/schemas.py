from pydantic import BaseModel

class CreateMapSchema(BaseModel):
    focus_question: str
    central_topic: str
