from pydantic import BaseModel

class CreateMapSchema(BaseModel):
    focus_question: str
    central_topic: str

class CreateMapSchema(BaseModel):
    focus_question: str
    central_topic: str

class CreateTopicSchema(BaseModel):
    name: str

class UpdateTopicSchema(BaseModel):
    name: str
    
class UpdateTopicPositionSchema(BaseModel):
    x: float
    y: float

class CreatePropositionSchema(BaseModel):
    source: int
    target: int
    label: str

class UpdatePropositionSchema(BaseModel):
    label: str
