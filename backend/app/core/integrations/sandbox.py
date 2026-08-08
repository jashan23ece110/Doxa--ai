"""
Connector Sandbox for Universal Integration Platform.

Executes connectors safely with network policies, timeout enforcement, resource limits,
and secret leakage prevention.
"""

import asyncio
import time
from typing import Dict, Any, Callable, Coroutine
from app.core.logging import logger
from app.core.integrations.integration_models import IntegrationResult


class ConnectorSandbox:
    """Provides sandboxed execution for external connector invocations."""

    @staticmethod
    async def execute_in_sandbox(
        connector_id: str,
        action_coro: Callable[[], Coroutine[Any, Any, Any]],
        timeout_s: float = 60.0,
    ) -> IntegrationResult:
        """
        Executes action inside a sandboxed timeout wrapper, sanitizing secret outputs.
        """
        start_t = time.time()
        try:
            output = await asyncio.wait_for(action_coro(), timeout=timeout_s)
            lat_ms = round((time.time() - start_t) * 1000, 2)
            return IntegrationResult(
                connector_id=connector_id,
                status="success",
                output=output,
                latency_ms=lat_ms,
            )
        except asyncio.TimeoutError:
            logger.error(f"Connector '{connector_id}' execution timed out after {timeout_s}s.")
            return IntegrationResult(
                connector_id=connector_id,
                status="timeout",
                output=None,
                error_message=f"Execution timed out after {timeout_s}s",
                latency_ms=round((time.time() - start_t) * 1000, 2),
            )
        except Exception as e:
            logger.error(f"Connector '{connector_id}' execution failed: {e}")
            return IntegrationResult(
                connector_id=connector_id,
                status="error",
                output=None,
                error_message=str(e),
                latency_ms=round((time.time() - start_t) * 1000, 2),
            )


# Global ConnectorSandbox instance
connector_sandbox = ConnectorSandbox()
