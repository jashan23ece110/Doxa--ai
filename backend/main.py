"""
Doxa AI Platform Backend Entrypoint.

Initializes FastAPI application instance, registers middleware, global exception handlers,
lifespan startup/shutdown hooks, includes v1 API routers, and defines system health checks.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.config_validator import ConfigValidator
from app.core.logging import logger
from app.core.exceptions import register_exception_handlers
from app.api.middleware.logging_middleware import RequestLoggingMiddleware
from app.api.middleware.correlation_middleware import CorrelationIdMiddleware
from app.api.middleware.request_size_middleware import RequestSizeLimitMiddleware
from app.api.v1.api import api_v1_router
from app.services.timer_service import timer_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Graceful startup and shutdown lifespan context manager."""
    start_time = time.time()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.ENVIRONMENT.upper()} profile)")

    # Execute Fail-Fast Startup Configuration & Permissions Validation
    ConfigValidator.validate_startup_configuration()

    startup_duration = (time.time() - start_time) * 1000
    logger.info(f"Startup completed in {startup_duration:.2f}ms")

    yield

    logger.info("Initiating graceful shutdown sequence...")
    try:
        if timer_service._scheduler.running:
            timer_service._scheduler.shutdown(wait=False)
            logger.info("BackgroundScheduler shutdown complete.")
    except Exception as e:
        logger.error(f"Error shutting down BackgroundScheduler: {e}")
    logger.info("Shutdown sequence finished.")


# Initialize FastAPI application with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Register CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Tracing, Request Size Limit, & Request Logging Middleware
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Register Global Exception Handlers
register_exception_handlers(app)

# Mount API V1 Routers
app.include_router(api_v1_router)


# ---------------------------------------------------------------------------
# Backward Compatibility Aliases for Legacy Imports & Unit Tests
# ---------------------------------------------------------------------------
from app.services.document_service import document_service
from app.services.agent_service import agent_service
from app.services.evaluate_service import evaluate_service
from app.services.llm_service import llm_service

add_document = document_service.add_document
list_documents = document_service.list_documents
delete_document = document_service.delete_document
retrieve_context = document_service.retrieve_context
build_rag_prompt = document_service.build_rag_prompt

run_agent_loop = agent_service.run_agent_loop
get_trace = agent_service.get_trace
call_gemini = llm_service.call_tokenrouter
call_llama = llm_service.call_tokenrouter
call_groq = evaluate_service.call_single_model
