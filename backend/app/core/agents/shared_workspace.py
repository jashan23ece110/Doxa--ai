"""
Shared Workspace for Enterprise Multi-Agent Operating System.

Versioned, thread-safe enterprise shared memory supporting documents, reasoning,
plans, artifacts, tool outputs, temporary notes, citations, and execution metadata.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.agents.metrics import agent_metrics_tracker


class WorkspaceArtifact(BaseModel):
    """Versioned artifact stored in shared workspace."""

    key: str
    version: int
    author_agent: str
    content: Any
    category: str = "general"  # documents, reasoning, plans, artifacts, tool_outputs, notes, citations
    timestamp: float = Field(default_factory=time.time)


class SharedWorkspace:
    """Thread-safe versioned enterprise shared workspace memory."""

    def __init__(self):
        self._lock = threading.Lock()
        self._storage: Dict[str, List[WorkspaceArtifact]] = {}

    def write(self, key: str, content: Any, author_agent: str = "system", category: str = "general") -> WorkspaceArtifact:
        """Writes a versioned artifact to the workspace."""
        with self._lock:
            history = self._storage.get(key, [])
            version = len(history) + 1
            artifact = WorkspaceArtifact(
                key=key,
                version=version,
                author_agent=author_agent,
                content=content,
                category=category,
            )
            history.append(artifact)
            self._storage[key] = history
            agent_metrics_tracker.workspace_objects_count = len(self._storage)
            return artifact

    def read(self, key: str, version: Optional[int] = None) -> Optional[WorkspaceArtifact]:
        """Reads latest artifact (or specific version) from workspace."""
        with self._lock:
            history = self._storage.get(key)
            if not history:
                return None

            if version is not None:
                for art in history:
                    if art.version == version:
                        return art
                return None

            return history[-1]

    def list_keys(self) -> List[str]:
        """Lists all keys in shared workspace."""
        with self._lock:
            return list(self._storage.keys())


# Global SharedWorkspace instance
shared_workspace = SharedWorkspace()
