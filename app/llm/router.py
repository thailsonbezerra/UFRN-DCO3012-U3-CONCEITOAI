from fastapi import APIRouter, HTTPException
from app.llm.schemas import PromptRequest, AnalyzeResponse
from app.llm.service import identify_topic, expand_topic

router = APIRouter(tags=["IA"])

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_prompt(data: PromptRequest):
    try:
        topic = identify_topic(data.prompt)
        related_topics = expand_topic(topic)
        return AnalyzeResponse(topic=topic, related_topics=related_topics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))