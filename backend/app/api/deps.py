"""
FastAPI Dependency Injection Provider Container.

Provides injectable factory functions for services, repositories,
and settings across all API endpoints, enabling easy unit testing
and mock overrides via app.dependency_overrides.
"""

from app.core.config import settings, Settings
from app.repositories.trace_repository import trace_repository, TraceRepository
from app.repositories.vector_repository import vector_repository, VectorRepository
from app.services.llm_service import llm_service, LLMService
from app.services.document_service import document_service, DocumentService
from app.services.evaluate_service import evaluate_service, EvaluateService
from app.services.agent_service import agent_service, AgentService
from app.services.timer_service import timer_service, TimerService
from app.services.auth_service import auth_service, AuthService


def get_settings() -> Settings:
    """Provides application settings dependency."""
    return settings


def get_trace_repository() -> TraceRepository:
    """Provides trace repository dependency."""
    return trace_repository


def get_vector_repository() -> VectorRepository:
    """Provides vector repository dependency."""
    return vector_repository


def get_llm_service() -> LLMService:
    """Provides LLM service dependency."""
    return llm_service


def get_document_service() -> DocumentService:
    """Provides document service dependency."""
    return document_service


def get_evaluate_service() -> EvaluateService:
    """Provides evaluation service dependency."""
    return evaluate_service


def get_agent_service() -> AgentService:
    """Provides agent service dependency."""
    return agent_service


def get_timer_service() -> TimerService:
    """Provides timer service dependency."""
    return timer_service


def get_auth_service() -> AuthService:
    """Provides auth service dependency."""
    return auth_service
