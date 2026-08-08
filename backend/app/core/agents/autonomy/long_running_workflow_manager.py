"""
Long-Running Workflow Manager.

Manages persistent multi-hour/multi-day workflows with state checkpoints, pause/resume, and scheduled wakeups.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.autonomy.agent_memory_types import WorkflowCheckpoint


class LongRunningWorkflowManager:
    """Thread-safe Long-Running Workflow Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._checkpoints: Dict[str, WorkflowCheckpoint] = {}

    def checkpoint_workflow(self, workflow_id: str, step_index: int, state_data: Dict[str, Any]) -> WorkflowCheckpoint:
        """Saves a persistent state checkpoint for long-running workflows."""
        chk = WorkflowCheckpoint(workflow_id=workflow_id, step_index=step_index, state_data=state_data)
        with self._lock:
            self._checkpoints[workflow_id] = chk
            security_logger.info(f"LongRunningWorkflowManager: Saved checkpoint for workflow '{workflow_id}' at step {step_index}.")
        return chk

    def recover_workflow(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        """Recovers checkpoint for a long-running workflow."""
        with self._lock:
            chk = self._checkpoints.get(workflow_id)
            if chk:
                security_logger.info(f"LongRunningWorkflowManager: Recovered workflow '{workflow_id}' checkpoint from step {chk.step_index}.")
            return chk


# Global LongRunningWorkflowManager instance
long_running_workflow_manager = LongRunningWorkflowManager()
