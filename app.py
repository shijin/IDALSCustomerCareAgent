from fastapi import FastAPI
from pydantic import BaseModel
from agent import get_agent

app = FastAPI(title="IDALS Customer Care Agent")

agent = get_agent()


class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None  # optional (future-ready)


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def health_check():
    return {"status": "ok", "service": "IDALS Agent"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Main chat endpoint
    """
    reply = agent(req.message)
    return ChatResponse(reply=reply)
