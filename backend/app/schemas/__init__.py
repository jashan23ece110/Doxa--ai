"""Package initialization for schemas."""
from app.schemas.evaluate import EvaluateRequest, EvaluateResponse, ModelResult
from app.schemas.document import DocumentItem, DocumentUploadResponse, DocumentListResponse, DocumentDeleteResponse
from app.schemas.agent import AgentRequest, AgentStartResponse, AgentStatusResponse, SuggestionRequest, SuggestionResponse
from app.schemas.timer import TimerRequest, TimerResponse
from app.schemas.auth import OAuthConnectResponse, OAuthCallbackResponse

__all__ = [
    "EvaluateRequest", "EvaluateResponse", "ModelResult",
    "DocumentItem", "DocumentUploadResponse", "DocumentListResponse", "DocumentDeleteResponse",
    "AgentRequest", "AgentStartResponse", "AgentStatusResponse", "SuggestionRequest", "SuggestionResponse",
    "TimerRequest", "TimerResponse",
    "OAuthConnectResponse", "OAuthCallbackResponse"
]
