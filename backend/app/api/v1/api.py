"""
API V1 Main Router Aggregator.
"""

from fastapi import APIRouter
from app.api.v1.routers.evaluate import router as evaluate_router
from app.api.v1.routers.documents import router as documents_router
from app.api.v1.routers.agent import router as agent_router
from app.api.v1.routers.timers import router as timers_router
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.health import router as health_router
from app.api.v1.routers.memory import router as memory_router

api_v1_router = APIRouter()

# Include all sub-routers
api_v1_router.include_router(health_router)
api_v1_router.include_router(evaluate_router)
api_v1_router.include_router(documents_router)
api_v1_router.include_router(agent_router)
api_v1_router.include_router(timers_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(memory_router)
