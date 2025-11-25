from app.llm.client import run_ollama
from app.llm.prompts import identify_topic_prompt, expand_topic_prompt
import re
import json

DEFAULT_MODEL = "llama3.2:1b-instruct-q4_0"

def identify_topic(user_prompt: str) -> str:
    prompt = identify_topic_prompt(user_prompt)
    result = run_ollama(DEFAULT_MODEL, prompt)
    return result.split("\n")[0].strip()

def expand_topic(topic: str) -> list[str]:
    prompt = expand_topic_prompt(topic)
    raw = run_ollama(DEFAULT_MODEL, prompt)
    
    match = re.search(r'\[.*\]', raw, re.DOTALL)
    if not match:
        raise ValueError("LLM não retornou array JSON")
    
    topics = json.loads(match.group(0))
    return [t.strip().capitalize() for t in topics if t.strip()]