import os
import time
import asyncio
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
import uuid
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from groq import AsyncGroq

from rag import (
    add_document,
    list_documents,
    delete_document,
    retrieve_context,
    build_rag_prompt,
)
from agent import run_agent_loop, global_traces

# Load environment variables
load_dotenv()

# Initialize API clients
# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

print(f"DEBUG Startup - GROQ_API_KEY (first 10 chars): {GROQ_API_KEY[:10] if GROQ_API_KEY else '[NOT SET]'}")

try:
    groq_client = AsyncGroq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Warning: Failed to initialize Groq client: {e}")
    groq_client = None

# Second model config will reuse groq_client

app = FastAPI(title="AI Evaluation Pipeline")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluateRequest(BaseModel):
    prompt: str
    groq_model: str = "llama-3.1-8b-instant"
    groq_model_2: str = "llama-3.3-70b-versatile"
    use_rag: bool = False

async def call_groq(prompt: str, model: str) -> dict:
    if not groq_client:
        return {"error": "Groq client not initialized", "latency_ms": 0}
    
    start_time = time.time()
    try:
        response = await groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        error = None
    except Exception as e:
        content = None
        error = str(e)
    
    latency_ms = (time.time() - start_time) * 1000
    
    return {
        "model": model,
        "content": content,
        "error": error,
        "latency_ms": round(latency_ms, 2)
    }

@app.post("/evaluate")
async def evaluate_prompt(req: EvaluateRequest):
    """
    Evaluates a prompt against two Groq models simultaneously,
    measuring latency and returning the results.

    When use_rag is True, retrieves relevant context from stored
    documents and augments the prompt before sending to models.
    """
    effective_prompt = req.prompt
    retrieved_context = None

    if req.use_rag:
        contexts = retrieve_context(req.prompt, n_results=3)
        retrieved_context = contexts
        if contexts:
            effective_prompt = build_rag_prompt(req.prompt, contexts)

    # Run both API calls concurrently
    groq_task_1 = call_groq(effective_prompt, req.groq_model)
    groq_task_2 = call_groq(effective_prompt, req.groq_model_2)
    
    results = await asyncio.gather(groq_task_1, groq_task_2)
    
    response = {
        "prompt": req.prompt,
        "results": {
            "groq_1": results[0],
            "groq_2": results[1]
        },
        "use_rag": req.use_rag,
    }

    if retrieved_context is not None:
        response["retrieved_context"] = retrieved_context

    return response


# ---------------------------------------------------------------------------
# Document management endpoints
# ---------------------------------------------------------------------------

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (.txt or .pdf) to the RAG knowledge base."""
    try:
        content_bytes = await file.read()
        result = add_document(file.filename, content_bytes)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {e}")


@app.get("/documents")
def get_documents():
    """List all documents in the RAG knowledge base."""
    return {"documents": list_documents()}


@app.delete("/documents/{doc_id}")
def remove_document(doc_id: str):
    """Delete a document and all its chunks from the knowledge base."""
    try:
        result = delete_document(doc_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {e}")

# ---------------------------------------------------------------------------
# Agent endpoints
# ---------------------------------------------------------------------------

class AgentRequest(BaseModel):
    goal: str
    language: str = "english"
    mode: str = "normal"

@app.post("/agent/start")
async def start_agent(req: AgentRequest, background_tasks: BackgroundTasks):
    """Start an agent run in the background."""
    run_id = str(uuid.uuid4())
    background_tasks.add_task(run_agent_loop, run_id, req.goal, req.language, req.mode)
    return {"run_id": run_id, "status": "started"}

@app.get("/agent/status/{run_id}")
def get_agent_status(run_id: str):
    """Get the current state/trace of an agent run."""
    trace = global_traces.get(run_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return trace

@app.get("/health")
def health_check():
    return {"status": "ok"}
