"""
AI Operating System Kernel for Doxa.

The central kernel entrypoint through which every backend request passes.
Responsibilities:
- Initialize execution state
- Coordinate intelligence modules via GlobalIntelligenceOrchestrator
- Handle failures with automatic recovery
- Schedule background tasks
- Publish system events
- Collect live metrics
- Finalize responses
- Maintain execution state lifecycle
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import (
    KernelExecutionState,
    ExecutionStatus,
)
from app.core.intelligence.intelligence_core import global_intelligence_orchestrator
from app.core.intelligence.scheduler import intelligence_scheduler
from app.core.intelligence.pipeline_profiler import pipeline_profiler
from app.core.intelligence.dashboard_backend import operational_dashboard_backend


class AIOSKernel:
    """Enterprise AI Operating System Kernel."""

    def __init__(self):
        self._active_executions: Dict[str, KernelExecutionState] = {}

    async def execute(
        self,
        prompt: str,
        user_id: str = "anonymous",
        tenant_id: str = "default",
        request_id: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        user_preferences: Optional[Dict[str, Any]] = None,
        latency_budget_ms: float = 5000.0,
    ) -> Dict[str, Any]:
        """
        Kernel execution entrypoint for incoming backend requests.

        Args:
            prompt: User request prompt text.
            user_id: User identifier.
            tenant_id: Tenant context identifier.
            request_id: Request identifier.
            history: Conversation history.
            user_preferences: Custom user preferences.
            latency_budget_ms: Latency budget in milliseconds.

        Returns:
            Finalized response dictionary.
        """
        if not settings.AI_OS_KERNEL_ENABLED:
            return await global_intelligence_orchestrator.execute_request(
                prompt=prompt,
                user_id=user_id,
                tenant_id=tenant_id,
                request_id=request_id,
                history=history,
                user_preferences=user_preferences,
                latency_budget_ms=latency_budget_ms,
            )

        req_id = request_id or f"req_k_{int(time.time() * 1000)}"

        # 1. Initialize Execution State
        state = KernelExecutionState(
            request_id=req_id,
            user_id=user_id,
            tenant_id=tenant_id,
            prompt=prompt,
            status=ExecutionStatus.INITIALIZING,
            started_at=time.time(),
        )
        self._active_executions[req_id] = state

        logger.info(f"AIOSKernel: Initialized execution '{state.execution_id}' for request '{req_id}'.")

        try:
            # 2. Transition Status: ROUTING & EXECUTING
            state.status = ExecutionStatus.EXECUTING

            # 3. Coordinate via Global Intelligence Orchestrator
            orch_result = await global_intelligence_orchestrator.execute_request(
                prompt=prompt,
                user_id=user_id,
                tenant_id=tenant_id,
                request_id=req_id,
                history=history,
                user_preferences=user_preferences,
                latency_budget_ms=latency_budget_ms,
            )

            # 4. Process Output & Transition to OPTIMIZING
            state.status = ExecutionStatus.OPTIMIZING
            state.output_text = orch_result.get("response_text", "")

            # 5. Finalize Execution
            state.status = ExecutionStatus.COMPLETED
            state.finalized_at = time.time()
            elapsed_ms = (state.finalized_at - state.started_at) * 1000.0

            # Attach kernel execution metadata to result
            orch_result["kernel_execution"] = {
                "execution_id": state.execution_id,
                "status": state.status.value,
                "duration_ms": round(elapsed_ms, 2),
            }

            logger.info(f"AIOSKernel: Completed execution '{state.execution_id}' in {elapsed_ms:.1f}ms.")
            return orch_result

        except Exception as e:
            logger.error(f"AIOSKernel error during execution '{state.execution_id}': {e}", exc_info=True)
            
            # Handle failure with graceful recovery
            state.status = ExecutionStatus.FAILED
            state.error_message = str(e)
            state.finalized_at = time.time()

            recovery_response = f"AI OS Kernel recovered from error: {str(e)}"
            return {
                "request_id": req_id,
                "response_text": recovery_response,
                "error": str(e),
                "kernel_execution": {
                    "execution_id": state.execution_id,
                    "status": ExecutionStatus.RECOVERED.value,
                },
            }

        finally:
            # Cleanup active execution tracking
            self._active_executions.pop(req_id, None)

    def get_active_executions_count(self) -> int:
        """Returns the number of currently active kernel executions."""
        return len(self._active_executions)


# Global AIOSKernel instance
ai_os_kernel = AIOSKernel()
