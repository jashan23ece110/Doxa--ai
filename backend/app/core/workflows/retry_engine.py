"""
Retry Engine for Autonomous Workflow Execution Engine.

Handles automated node retries using exponential backoff, jitter, fixed retry, and classification.
"""

import asyncio
import random
import time
from typing import Dict, Any, Callable, Coroutine
from app.core.config import settings
from app.core.logging import logger
from app.core.workflows.workflow_models import WorkflowNode


class RetryEngine:
    """Executes node actions with exponential backoff and jitter."""

    @staticmethod
    async def execute_with_retry(
        node: WorkflowNode,
        coro_func: Callable[[], Coroutine[Any, Any, Any]],
        max_retries: int = 3,
        initial_delay_s: float = 0.5,
        backoff_factor: float = 2.0,
    ) -> Any:
        """
        Executes action with exponential backoff retry.
        Formula: delay = initial * (backoff_factor ** retries) + random_jitter
        """
        limit = getattr(settings, "DEFAULT_RETRY_LIMIT", max_retries)
        last_exception = None

        for attempt in range(limit + 1):
            try:
                return await coro_func()
            except Exception as e:
                last_exception = e
                node.retry_count = attempt + 1
                if attempt < limit:
                    jitter = random.uniform(0.05, 0.20)
                    delay = (initial_delay_s * (backoff_factor ** attempt)) + jitter
                    logger.warning(
                        f"Node '{node.node_id}' failed (Attempt {attempt + 1}/{limit + 1}): {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Node '{node.node_id}' exhausted all {limit} retry attempts.")
                    raise last_exception


# Global RetryEngine instance
retry_engine = RetryEngine()
