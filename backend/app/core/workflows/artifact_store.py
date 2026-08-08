"""
Artifact Store for Autonomous Workflow Execution Engine.

Persists versioned documents, generated code, reasoning outputs, reports, logs, images, and structured JSON.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.workflows.workflow_models import WorkflowArtifact


class ArtifactStore:
    """Thread-safe disk persistence for versioned workflow artifacts."""

    def __init__(self, base_dir: str = "./workflow_data/artifacts"):
        self.base_dir = base_dir
        self._lock = threading.Lock()
        self._artifacts: Dict[str, WorkflowArtifact] = {}
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Ensures artifacts storage directory exists."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def save_artifact(self, artifact: WorkflowArtifact) -> WorkflowArtifact:
        """Saves a versioned artifact to disk and memory."""
        with self._lock:
            self._artifacts[artifact.artifact_id] = artifact
            file_path = os.path.join(self.base_dir, f"{artifact.artifact_id}.json")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(artifact.model_dump(), f, indent=2, default=str)
                logger.info(f"Saved workflow artifact '{artifact.artifact_id}' ({artifact.name}) to disk.")
            except Exception as e:
                logger.error(f"Failed to save artifact to disk: {e}")

        return artifact

    def get_artifact(self, artifact_id: str) -> Optional[WorkflowArtifact]:
        """Retrieves an artifact by ID."""
        with self._lock:
            return self._artifacts.get(artifact_id)


# Global ArtifactStore instance
artifact_store = ArtifactStore()
