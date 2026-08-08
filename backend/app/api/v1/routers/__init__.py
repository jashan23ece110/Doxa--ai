"""Routers package initialization."""
from app.api.v1.routers.evaluate import router as evaluate_router
from app.api.v1.routers.documents import router as documents_router
from app.api.v1.routers.agent import router as agent_router
from app.api.v1.routers.timers import router as timers_router
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.health import router as health_router

__all__ = [
    "evaluate_router",
    "documents_router",
    "agent_router",
    "timers_router",
    "auth_router",
    "health_router",
]
