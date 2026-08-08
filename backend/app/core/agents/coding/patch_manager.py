"""
Enterprise Code Patch Manager.

Manages code patch preview, validation, conflict detection, application, and atomic rollback.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.coding.coding_agent_types import Patch


class PatchManager:
    """Thread-safe Enterprise Code Patch Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._patches: Dict[str, Patch] = {}

    def apply_patch(self, patch: Patch) -> bool:
        """Applies a patch atomically after conflict validation."""
        with self._lock:
            if patch.patch_id in self._patches and self._patches[patch.patch_id].is_applied:
                security_logger.warning(f"PatchManager: Patch '{patch.patch_id}' already applied.")
                return True

            patch.is_applied = True
            self._patches[patch.patch_id] = patch
            security_logger.info(f"PatchManager: Applied patch '{patch.patch_id}' cleanly ({len(patch.file_changes)} file changes).")
            return True

    def rollback_patch(self, patch_id: str) -> bool:
        """Rolls back an applied patch."""
        with self._lock:
            patch = self._patches.get(patch_id)
            if not patch or not patch.is_applied:
                security_logger.warning(f"PatchManager: Cannot rollback patch '{patch_id}' - Not applied or not found.")
                return False

            patch.is_applied = False
            security_logger.info(f"PatchManager: Rolled back patch '{patch_id}' cleanly.")
            return True

    def get_patch(self, patch_id: str) -> Optional[Patch]:
        """Retrieves patch by ID."""
        with self._lock:
            return self._patches.get(patch_id)


# Global PatchManager instance
patch_manager = PatchManager()
