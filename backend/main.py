import os
import time
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from groq import AsyncGroq

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
    """
    # Run both API calls concurrently
    groq_task_1 = call_groq(req.prompt, req.groq_model)
    groq_task_2 = call_groq(req.prompt, req.groq_model_2)
    
    results = await asyncio.gather(groq_task_1, groq_task_2)
    
    return {
        "prompt": req.prompt,
        "results": {
            "groq_1": results[0],
            "groq_2": results[1]
        }
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
