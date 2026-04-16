from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import tempfile
import os
import shutil
from collections import defaultdict

from rag.ingestor import ingest_file
from agents.router import route_query
from agents.doc_agent import answer_doc_query
from agents.data_agent import answer_data_query

app = FastAPI(title="Project Intelligence Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSION_HISTORY: dict[str, list[dict]] = defaultdict(list)
MAX_TURNS = 6

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    agent_used: str
    sources: list[str]
    confidence: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed = {".pdf", ".csv", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(400, f"File type {ext} not supported. Use: {allowed}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = ingest_file(tmp_path, original_filename=file.filename)
        return {
            "status": "success",
            "filename": file.filename,
            "chunks_stored": result["chunks"],
            "doc_id": result["doc_id"],
        }
    finally:
        os.unlink(tmp_path)

def build_query_with_history(session_id: str, query: str) -> str:
    history = SESSION_HISTORY.get(session_id, [])
    if not history:
        return query

    recent = history[-MAX_TURNS:]
    history_text = "\n".join(
        f"{item['role'].upper()}: {item['content']}" for item in recent
    )
    return f"""Conversation history:
{history_text}

Current user question:
{query}
"""

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.query.strip():
        raise HTTPException(400, "Query cannot be empty")

    session_id = req.session_id or "default"
    enriched_query = build_query_with_history(session_id, req.query)

    agent_type = route_query(req.query)

    if agent_type == "data":
        result = answer_data_query(enriched_query)
    else:
        result = answer_doc_query(enriched_query)

    SESSION_HISTORY[session_id].append({"role": "user", "content": req.query})
    SESSION_HISTORY[session_id].append({"role": "assistant", "content": result["answer"]})
    SESSION_HISTORY[session_id] = SESSION_HISTORY[session_id][-MAX_TURNS:]

    return ChatResponse(
        answer=result["answer"],
        agent_used=agent_type,
        sources=result.get("sources", []),
        confidence=result.get("confidence", "medium"),
    )