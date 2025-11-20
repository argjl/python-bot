# app/server.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.agent import agent

app = FastAPI(title="Text-only AI Agent", version="0.1.0")

class AgentRequest(BaseModel):
    sessionId: str = Field(..., description="Unique session id (e.g., user or chat id)")
    userMessage: str = Field(..., description="Your text message")

class AgentResponse(BaseModel):
    text: str
    info: dict = {}

@app.post("/agent/invoke", response_model=AgentResponse)
async def invoke(req: AgentRequest):
    # Generate a reply
    reply = agent.generate_reply(req.userMessage)

    # Basic info payload—handy for debugging/logging
    info = {
        "sessionId": req.sessionId,
        "length": len(reply),
        "channel": "web",      # future: telegram/slack/etc.
        "version": "0.1.0"
    }

    return AgentResponse(text=reply, info=info)

@app.get("/")
def health():
    return {"status": "ok", "service": "Text-only AI Agent"}