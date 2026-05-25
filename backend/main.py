from fastapi import FastAPI
from pydantic import BaseModel

# =========================
# AGENT CORE
# =========================

from backend.agent.agent_core import process_prompt

# =========================
# MEMORY
# =========================

from backend.memory.persistent_memory import init_db


# =========================
# APP
# =========================

app = FastAPI(title="Jarvis Core")

# Inicializar SQLite
init_db()


# =========================================================
# MODELS
# =========================================================


class AgentRequest(BaseModel):
    prompt: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "status": "Jarvis online"
    }


# =========================================================
# AGENT CHAT
# =========================================================

@app.post("/agent/chat")
def agent_chat(req: AgentRequest):

    return process_prompt(req.prompt)
