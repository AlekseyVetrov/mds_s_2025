from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .database import save_message, get_history, clear_history
from .pollinations_client import ask_pollinations

app = FastAPI(title="AI Assistant API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    user_id: str
    prompt: str

class AskResponse(BaseModel):
    response: str
    history: List[dict]

class ClearRequest(BaseModel):
    user_id: str

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    user_id = request.user_id
    prompt = request.prompt
    
    history = get_history(user_id, limit=10)
    
    save_message(user_id, "user", prompt)
    
    answer = ask_pollinations(prompt, history)
    
    save_message(user_id, "assistant", answer)
    
    updated_history = get_history(user_id, limit=10)
    return AskResponse(response=answer, history=updated_history)

@app.get("history/{user_id}")
async def history(user_id: str):
    history = get_history(user_id, limit=20)
    return {"user_id": user_id, "history": history}

@app.post("clear")
async def clear(request: ClearRequest):
    clear_history(request.user_id)
    return {"status": "ok", "message": "История очищена"}

@app.get("health")
async def health():
    return {"status": "OK"}