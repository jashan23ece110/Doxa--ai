"""
Persistent Workflow State Manager.

Tracks multi-agent workflow checkpoints and execution states supporting failure recovery.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.collaboration.collaboration_types import WorkflowState, WorkflowCheckpoint


class WorkflowStateManager:
    """Thread-safe Persistent Workflow State Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._states: Dict[str, WorkflowState] = {}

    def get_or_create_state(self, workflow_id: str) -> WorkflowState:
        """Retrieves or creates WorkflowState for workflow tracking."""
        with self._lock:
            if workflow_id not in self._states:
                self._states[workflow_id] = WorkflowState(workflow_id=workflow_id)
                security_logger.info(f"WorkflowStateManager: Created workflow state for '{workflow_id}'.")
            return self._states[workflow_id]

    def create_checkpoint(self, workflow_id: str, step_name: str, snapshot: Dict[str, Any]) -> WorkflowCheckpoint:
        """Creates a workflow checkpoint for fault recovery."""
        state = self.get_or_create_state(workflow_id)
        chk = WorkflowCheckpoint(workflow_id=workflow_id, step_name=step_name, state_snapshot=snapshot)
        with self._lock:
            state.checkpoints.append(chk)
            state.current_step = step_name
            state.updated_at = time.time()
            security_logger.info(f"WorkflowStateManager: Checkpointed workflow '{workflow_id}' at step '{step_name}'.")
        return chk


# Global WorkflowStateManager instance
workflow_state_manager = WorkflowStateManager()
