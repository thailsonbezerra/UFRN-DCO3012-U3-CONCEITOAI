from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.llm.router import router as llm_router
from app.maps.router import router as maps_router

app = FastAPI(title="ConceitoAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_router)
app.include_router(maps_router)

@app.get("/health")
def root():
    return {"message": "ConceitoAI is healthy!"}