from fastapi import FastAPI
from app.llm.router import router as llm_router
from app.maps.router import router as maps_router

app = FastAPI(title="ConceitoAI")

app.include_router(llm_router)
app.include_router(maps_router)

@app.get("/health")
def root():
    return {"message": "ConceitoAI is healthy!"}