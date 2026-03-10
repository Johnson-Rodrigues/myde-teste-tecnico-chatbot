from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Implement RAG retrieval
    return {"response": "Assistant message here"}

@app.get("/health")
async def health():
    return {"status": "healthy"}