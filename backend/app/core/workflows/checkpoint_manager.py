"""
Checkpoint Manager for Autonomous Workflow Execution Engine.

Persists execution state snapshots to disk (./workflow_data/checkpoints/) to support
resumable execution after restarts, partial rollbacks, and execution replays.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.workflows.workflow_models import Workflow, WorkflowCheckpoint


class CheckpointManager:
    """Thread-safe disk checkpoint persistence manager."""

    def __init__(self, base_dir: str = "./workflow_data/checkpoints"):
        self.base_dir = base_dir
        self._lock = threading.Lock()
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Ensures checkpoints directory exists."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def create_checkpoint(self, workflow: Workflow) -> WorkflowCheckpoint:
        """Creates and persists a checkpoint snapshot for a workflow."""
        completed_ids = [
            n.node_id for n in workflow.nodes.values()
            if n.status.value in ("completed", "cancelled")
        ]
        outputs = {
            n.node_id: n.output for n in workflow.nodes.values()
            if n.output is not None
        }

        chk = WorkflowCheckpoint(
            workflow_id=workflow.workflow_id,
            completed_node_ids=completed_ids,
            outputs=outputs,
        )

        with self._lock:
            workflow.checkpoints.append(chk)
            file_path = os.path.join(self.base_dir, f"{workflow.workflow_id}_{chk.checkpoint_id}.json")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(chk.model_dump(), f, indent=2, default=str)
                logger.debug(f"Saved checkpoint '{chk.checkpoint_id}' for workflow '{workflow.workflow_id}'.")
            except Exception as e:
                logger.error(f"Failed to save checkpoint to disk: {e}")

        return chk


# Global CheckpointManager instance
checkpoint_manager = CheckpointManager()
