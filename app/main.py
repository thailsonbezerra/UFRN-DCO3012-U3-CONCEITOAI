import re
import json
import time
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from app.database.connection import query
from app.schemas import PromptRequest
from app.prompts import identify_topic_prompt, expand_topic_prompt
from app.llm_service import run_ollama

app = FastAPI(title="conceitoai", version="1.0.0")

@app.post("/analyze")
def analyze_prompt(data: PromptRequest):
    start_time = time.time()
    prompt = data.prompt.strip()

    try:
        identify_prompt = identify_topic_prompt(prompt)
        topic = run_ollama("llama3.2:1b-instruct-q4_0", identify_prompt).split("\n")[0].strip()
        print(f"Identificar: {time.time() - start_time:.2f}s")

        expand_prompt = expand_topic_prompt(topic)
        related_raw = run_ollama("llama3.2:1b-instruct-q4_0", expand_prompt)
        print(f"Expandir: {time.time() - start_time:.2f}s")

        match = re.search(r'\[.*\]', related_raw, re.DOTALL)
        if not match:
            raise ValueError("Não foi encontrado um array JSON na resposta.")
        json_str = match.group(0)

        related_topics = json.loads(json_str)
        related_topics = [t.strip().capitalize() for t in related_topics if isinstance(t, str) and t.strip()]

        return {
            "topic": topic,
            "related_topics": related_topics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/maps", response_model=List[Dict])
def listar_maps():
    sql = """
        SELECT uuid, focus_question, m.created,
               t.name AS topic_central_name
        FROM maps m
        JOIN topics t ON t.id = m.topic_id_central
        ORDER BY created DESC
    """
    return query(sql)
    