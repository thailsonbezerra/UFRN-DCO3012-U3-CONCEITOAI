from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    prompt: str

class AnalyzeResponse(BaseModel):
    topic: str
    related_topics: List[str]