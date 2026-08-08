"""
Model Evaluation API Router with Dependency Injection.
"""

from fastapi import APIRouter, Depends
from app.schemas.evaluate import EvaluateRequest, EvaluateResponse
from app.services.evaluate_service import EvaluateService
from app.api.deps import get_evaluate_service

router = APIRouter(tags=["Evaluation"])


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_prompt(
    req: EvaluateRequest,
    eval_service: EvaluateService = Depends(get_evaluate_service),
):
    """
    Evaluates a prompt against two LLM models simultaneously,
    measuring latency and returning comparative results.

    When use_rag is True, retrieves relevant context from stored
    documents and augments the prompt before sending to models.
    """
    result = await eval_service.evaluate(
        prompt=req.prompt,
        groq_model=req.groq_model,
        groq_model_2=req.groq_model_2,
        use_rag=req.use_rag,
    )
    return result
