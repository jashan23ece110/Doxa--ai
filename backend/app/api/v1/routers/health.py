"""
Comprehensive Production Health, Readiness, and Version Probe API Router.
"""

import time
from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.core.config import settings
from app.core.metrics import metrics_collector
from app.api.deps import get_vector_repository, get_trace_repository, get_timer_service
from app.repositories.vector_repository import VectorRepository
from app.repositories.trace_repository import TraceRepository
from app.services.timer_service import TimerService

router = APIRouter(tags=["Health & Probes"])


@router.get("/health")
@router.get("/live")
def liveness_probe() -> Dict[str, Any]:
    """Basic liveness probe checking if application process is running."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@router.get("/ready")
async def readiness_probe(
    vec_repo: VectorRepository = Depends(get_vector_repository),
    tr_repo: TraceRepository = Depends(get_trace_repository),
    tm_service: TimerService = Depends(get_timer_service),
) -> Dict[str, Any]:
    """
    Comprehensive readiness probe verifying vector store, Firestore/trace DB,
    LLM API credentials, background scheduler, and security limits.
    """
    checks: Dict[str, Any] = {}

    # Probe 1: Vector Store
    try:
        col = vec_repo.get_collection()
        doc_count = col.count()
        checks["vector_db"] = {"status": "ready", "items_count": doc_count}
    except Exception as e:
        checks["vector_db"] = {"status": "unhealthy", "error": str(e)}

    # Probe 2: Trace DB / Storage
    try:
        db = tr_repo._get_db()
        checks["trace_storage"] = {
            "type": "firestore" if db else "memory_fallback",
            "status": "ready",
        }
    except Exception as e:
        checks["trace_storage"] = {"status": "unhealthy", "error": str(e)}

    # Probe 3: LLM Provider Credentials
    has_tokenrouter = bool(settings.TOKENROUTER_API_KEY)
    checks["llm_provider"] = {
        "status": "configured" if has_tokenrouter else "warning_unconfigured_key",
        "model": settings.DEFAULT_MODEL,
    }

    # Probe 4: Background Scheduler
    scheduler_running = tm_service._scheduler.running
    checks["background_scheduler"] = {
        "status": "running" if scheduler_running else "stopped",
    }

    # Probe 5: Resource Protection Limits
    checks["security_limits"] = {
        "status": "active",
        "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024),
        "max_request_body_mb": settings.MAX_REQUEST_BODY_SIZE // (1024 * 1024),
        "max_stored_docs": settings.MAX_DOCUMENT_COUNT,
    }

    is_overall_healthy = all(
        c.get("status") in ("ready", "configured", "warning_unconfigured_key", "running", "active")
        for c in checks.values()
    )

    return {
        "status": "ready" if is_overall_healthy else "degraded",
        "checks": checks,
    }


@router.get("/version")
def version_info() -> Dict[str, Any]:
    """Returns application build metadata, environment profile, uptime, and metrics summary."""
    uptime_seconds = round(time.time() - settings.PROCESS_START_TIME, 2)

    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "debug_mode": settings.DEBUG,
        "metrics_summary": metrics_collector.get_metrics_summary(),
    }
