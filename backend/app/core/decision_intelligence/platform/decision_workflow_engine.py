"""
Global Decision Workflow Engine.

Manages dynamic decision graph execution, approval checkpoints, and workflow state transitions.
"""

import threading
import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class DecisionWorkflowState(BaseModel):
    workflow_id: str = Field(default_factory=lambda: f"dwork_{int(time.time() * 1000)}")
    decision_title: str
    current_stage: str = "INITIATED"  # INITIATED, ANALYZING, GOVERNANCE_CHECK, WAITING_APPROVAL, COMPLETED
    executed_nodes: List[str] = Field(default_factory=list)
    status: str = "RUNNING"


class DecisionWorkflowEngine:
    """Thread-safe Global Decision Workflow Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._workflows: Dict[str, DecisionWorkflowState] = {}

    def create_workflow(self, decision_title: str) -> DecisionWorkflowState:
        """Creates a new decision workflow instance."""
        wf = DecisionWorkflowState(decision_title=decision_title)
        with self._lock:
            self._workflows[wf.workflow_id] = wf
            security_logger.info(f"DecisionWorkflowEngine: Created decision workflow '{wf.workflow_id}' for '{decision_title}'.")
        return wf

    def advance_workflow_stage(self, workflow_id: str, new_stage: str, node_executed: str) -> DecisionWorkflowState:
        """Advances workflow stage and records executed node."""
        with self._lock:
            if workflow_id in self._workflows:
                wf = self._workflows[workflow_id]
                wf.current_stage = new_stage
                wf.executed_nodes.append(node_executed)
                if new_stage == "COMPLETED":
                    wf.status = "COMPLETED"
                security_logger.info(f"DecisionWorkflowEngine: Advanced workflow '{workflow_id}' to '{new_stage}'.")
                return wf
            wf_dummy = DecisionWorkflowState(decision_title="Unknown", current_stage=new_stage, status="COMPLETED")
            return wf_dummy


# Global DecisionWorkflowEngine instance
decision_workflow_engine = DecisionWorkflowEngine()
