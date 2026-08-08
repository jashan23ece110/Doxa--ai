"""
JSON Workflow Repository for Enterprise Autonomous Workflow Engine.

Persists workflow state and checkpoints to disk (./workflow_data/workflows.json)
so long-running workflows survive application restarts.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowState


class JSONWorkflowRepository:
    """Thread-safe JSON repository for persisting workflow state."""

    def __init__(self, file_path: str = "./workflow_data/workflows.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._workflows: Dict[str, WorkflowInstance] = {}
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads workflows from JSON file on disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for wf_id, wf_dict in data.items():
                self._workflows[wf_id] = WorkflowInstance.model_validate(wf_dict)

            logger.info(f"Loaded {len(self._workflows)} workflows from disk ({self.file_path}).")
        except Exception as e:
            logger.error(f"Failed to load workflows from disk ({e}). Initializing empty repository.")

    def _save_to_disk(self) -> None:
        """Saves workflows to JSON file on disk."""
        try:
            data = {
                wf_id: wf.model_dump()
                for wf_id, wf in self._workflows.items()
            }
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save workflows to disk: {e}")

    def save(self, workflow: WorkflowInstance) -> None:
        """Saves or updates a workflow instance."""
        with self._lock:
            workflow.update_timestamp()
            self._workflows[workflow.workflow_id] = workflow
            self._save_to_disk()

    def get(self, workflow_id: str) -> Optional[WorkflowInstance]:
        """Retrieves a workflow by ID."""
        with self._lock:
            return self._workflows.get(workflow_id)

    def list_all(self, user_id: Optional[str] = None) -> List[WorkflowInstance]:
        """Lists all workflows, optionally filtered by user_id."""
        with self._lock:
            if user_id:
                return [wf for wf in self._workflows.values() if wf.user_id == user_id]
            return list(self._workflows.values())

    def delete(self, workflow_id: str) -> bool:
        """Deletes a workflow instance."""
        with self._lock:
            if workflow_id in self._workflows:
                del self._workflows[workflow_id]
                self._save_to_disk()
                return True
            return False


# Global JSONWorkflowRepository instance
workflow_repository = JSONWorkflowRepository()
