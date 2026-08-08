"""
JSON Mission Repository for Autonomous Mission Control System.

Persists missions, goals, milestones, progress snapshots, and recovery events to disk
(./mission_data/missions.json) across application restarts.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.missions.mission_models import Mission


class JSONMissionRepository:
    """Thread-safe JSON repository for mission persistence."""

    def __init__(self, file_path: str = "./mission_data/missions.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._missions: Dict[str, Mission] = {}
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads missions from disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                m = Mission.model_validate(item)
                self._missions[m.mission_id] = m

            logger.info(f"Loaded {len(self._missions)} missions from disk ({self.file_path}).")
        except Exception as e:
            logger.error(f"Failed to load missions from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves missions to disk."""
        try:
            data = [m.model_dump() for m in self._missions.values()]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save missions to disk: {e}")

    def save_mission(self, mission: Mission) -> None:
        """Saves or updates a mission in repository."""
        with self._lock:
            self._missions[mission.mission_id] = mission
            limit = getattr(settings, "MAX_ACTIVE_MISSIONS", 500)
            if len(self._missions) > limit:
                # Evict oldest completed mission
                oldest = min(self._missions.keys(), key=lambda k: self._missions[k].created_at)
                del self._missions[oldest]
            self._save_to_disk()

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Retrieves a mission by ID."""
        with self._lock:
            return self._missions.get(mission_id)

    def list_missions(self, user_id: Optional[str] = None) -> List[Mission]:
        """Lists missions for a user."""
        with self._lock:
            if not user_id:
                return list(self._missions.values())
            return [m for m in self._missions.values() if m.user_id == user_id]


# Global JSONMissionRepository instance
mission_repository = JSONMissionRepository()
