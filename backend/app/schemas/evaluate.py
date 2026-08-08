"""
Pydantic Schemas for Model Evaluation Endpoints.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    prompt: str = Field(..., description="Prompt to evaluate against models")
    groq_model: str = Field(default="moonshotai/kimi-k3-free", description="First model identifier")
    groq_model_2: str = Field(default="moonshotai/kimi-k3-free", description="Second model identifier")
    use_rag: bool = Field(default=False, description="Whether to augment prompt with RAG context")


class ModelResult(BaseModel):
    model: str
    content: Optional[str] = None
    error: Optional[str] = None
    latency_ms: float


class EvaluateResponse(BaseModel):
    prompt: str
    results: Dict[str, ModelResult]
    use_rag: bool
    retrieved_context: Optional[List[Dict[str, Any]]] = None
