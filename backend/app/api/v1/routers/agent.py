"""
Agent Execution and Proactive Suggestions API Router with Security & Connection Hardening.
"""

import json
import uuid
import asyncio
import time
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse
from app.schemas.agent import (
    AgentRequest,
    AgentStartResponse,
    AgentStatusResponse,
    SuggestionRequest,
    SuggestionResponse,
)
from app.services.agent_service import AgentService
from app.api.deps import get_agent_service
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.core.security import PromptSanitizer

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/start", response_model=AgentStartResponse)
async def start_agent(
    req: AgentRequest,
    background_tasks: BackgroundTasks,
    ag_service: AgentService = Depends(get_agent_service),
):
    """Start an autonomous agent run in the background with sanitized prompt input."""
    run_id = str(uuid.uuid4())
    sanitized_goal = PromptSanitizer.sanitize_user_input(req.goal)

    background_tasks.add_task(
        ag_service.run_agent_loop,
        run_id,
        sanitized_goal,
        req.language,
        req.mode,
        req.history,
    )
    return {"run_id": run_id, "status": "started"}


@router.get("/status/{run_id}", response_model=AgentStatusResponse)
def get_agent_status(
    run_id: str,
    ag_service: AgentService = Depends(get_agent_service),
):
    """Get the current execution trace of an agent run."""
    if not run_id or not run_id.strip():
        raise NotFoundError("Run ID cannot be empty.")
    trace = ag_service.get_trace(run_id)
    if not trace:
        raise NotFoundError(f"Run ID '{run_id}' not found.")
    return trace


@router.get("/stream/{run_id}")
async def stream_agent(
    run_id: str,
    ag_service: AgentService = Depends(get_agent_service),
):
    """Yields Server-Sent Events (SSE) detailing trace chunks with connection lifetime bounds."""

    async def event_generator():
        last_idx = 0
        last_step_count = 0
        start_time = time.time()
        max_lifetime = settings.MAX_SSE_STREAM_LIFETIME_SECONDS

        try:
            while True:
                # 1. Connection Lifetime Timeout Check
                if time.time() - start_time > max_lifetime:
                    yield f"data: {json.dumps({'status': 'timeout', 'error': 'Maximum streaming connection duration exceeded.'})}\n\n"
                    break

                trace = ag_service.get_trace(run_id)
                if not trace:
                    yield f"data: {json.dumps({'status': 'not_found'})}\n\n"
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
                    "is_debating": trace.get("is_debating", False),
                    "debate_a": trace.get("debate_a", ""),
                    "debate_b": trace.get("debate_b", ""),
                    "error": trace.get("error", None),
                }

                if len(final_res) > last_idx:
                    payload["chunk"] = final_res[last_idx:]
                    last_idx = len(final_res)
                    yield f"data: {json.dumps(payload)}\n\n"
                elif len(current_steps) > last_step_count or status != "running":
                    last_step_count = len(current_steps)
                    yield f"data: {json.dumps(payload)}\n\n"

                if status in ("completed", "failed"):
                    break

                await asyncio.sleep(0.18)
        except asyncio.CancelledError:
            # Client disconnected
            pass

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/proactive_suggestions", response_model=SuggestionResponse)
async def get_proactive_suggestions(
    req: SuggestionRequest,
    ag_service: AgentService = Depends(get_agent_service),
):
    """Generate 1-2 proactive questions or insights based on recent history."""
    result = await ag_service.generate_proactive_suggestions(
        history=req.history,
        language=req.language,
    )
    return result
