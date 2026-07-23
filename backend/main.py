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
from agent import run_agent_loop

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

from agent import get_trace
import json
from fastapi.responses import StreamingResponse

class AgentRequest(BaseModel):
    goal: str
    language: str = "english"
    mode: str = "normal"
    history: list = []

@app.post("/agent/start")
async def start_agent(req: AgentRequest, background_tasks: BackgroundTasks):
    """Start an agent run in the background."""
    run_id = str(uuid.uuid4())
    background_tasks.add_task(run_agent_loop, run_id, req.goal, req.language, req.mode, req.history)
    return {"run_id": run_id, "status": "started"}

@app.get("/agent/status/{run_id}")
def get_agent_status(run_id: str):
    """Get the current state/trace of an agent run."""
    trace = get_trace(run_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return trace

@app.get("/agent/stream/{run_id}")
async def stream_agent(run_id: str):
    """Yields Server-Sent Events (SSE) detailing the trace and chunks of the response."""
    async def event_generator():
        last_idx = 0
        last_step_count = 0
        while True:
            trace = get_trace(run_id)
            if not trace:
                yield "data: " + json.dumps({"status": "not_found"}) + "\n\n"
                break
            
            current_steps = trace.get("steps", [])
            plan = trace.get("plan", [])
            status = trace.get("status", "running")
            final_res = trace.get("final_result", "") or ""
            
            payload = {
                "status": status,
                "plan": plan,
                "steps": current_steps,
                "self_check": trace.get("self_check", None),
                "sentiment": trace.get("sentiment", "neutral"),
                "error": trace.get("error", None)
            }
            
            # Yield new final result tokens if any have been streamed
            if len(final_res) > last_idx:
                payload["chunk"] = final_res[last_idx:]
                last_idx = len(final_res)
                yield f"data: {json.dumps(payload)}\n\n"
            # If no new final result tokens, check if new steps are completed
            elif len(current_steps) > last_step_count or status != "running":
                last_step_count = len(current_steps)
                yield f"data: {json.dumps(payload)}\n\n"
                
            if status in ("completed", "failed"):
                break
                
            await asyncio.sleep(0.18)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

from tools.timer_manager import notification_queues

@app.get("/notifications/stream")
async def notifications_stream():
    """
    SSE endpoint pushing real-time timer completion alerts to the frontend.
    """
    async def event_generator():
        queue = asyncio.Queue()
        notification_queues.append(queue)
        try:
            while True:
                alert = await queue.get()
                yield f"data: {json.dumps(alert)}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            if queue in notification_queues:
                notification_queues.remove(queue)
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")

class TimerRequest(BaseModel):
    title: str
    seconds: int

@app.post("/timers")
def create_timer(req: TimerRequest):
    from tools.timer_manager import schedule_timer
    msg = schedule_timer(req.title, req.seconds)
    return {"status": "ok", "message": msg}

@app.get("/google/connect")
def google_connect():
    """
    Generates Google OAuth authorization URL.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="Google Calendar OAuth credentials not configured in backend.")
        
    try:
        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth2callback")
        flow.redirect_uri = redirect_uri
        
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true"
        )
        return {"authorization_url": authorization_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google OAuth initialization failed: {e}")

@app.get("/oauth2callback")
def oauth2callback(code: str):
    """
    Google OAuth callback code exchange handler.
    """
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="Credentials missing.")
        
    try:
        from google_auth_oauthlib.flow import Flow
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth2callback")
        flow.redirect_uri = redirect_uri
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Save to token.json
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
            
        return {"status": "success", "message": "Google Calendar connected successfully! You can close this window now."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google OAuth callback exchange failed: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}
