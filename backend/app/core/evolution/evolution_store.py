"""
Evolution Store for Enterprise Self-Optimization Platform.

Persists optimization history, capability evolution, experiment results,
and performance trends to disk (`./evolution_data/store.json`).
"""

import json
import os
import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.evolution.evolution_models import EvolutionSnapshot


class EvolutionStore:
    """Thread-safe disk storage manager for evolution history."""

    def __init__(self, storage_dir: str = "./evolution_data"):
        self.storage_dir = storage_dir
        self.file_path = os.path.join(storage_dir, "store.json")
        self._lock = threading.Lock()
        self._snapshots: Dict[str, EvolutionSnapshot] = {}
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensures storage directory exists and loads existing data."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Loads evolution snapshots from disk."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        snap = EvolutionSnapshot.model_validate(item)
                        self._snapshots[snap.snapshot_id] = snap
                logger.info(
                    f"EvolutionStore loaded {len(self._snapshots)} snapshots from disk."
                )
            except Exception as e:
                logger.error(f"Failed to load evolution store from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves all evolution snapshots to disk."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(
                    [s.model_dump() for s in self._snapshots.values()],
                    f,
                    indent=2,
                    default=str,
                )
        except Exception as e:
            logger.error(f"Failed to save evolution store to disk: {e}")

    def save_snapshot(self, snapshot: EvolutionSnapshot) -> EvolutionSnapshot:
        """Persists an evolution snapshot."""
        with self._lock:
            self._snapshots[snapshot.snapshot_id] = snapshot
            self._save_to_disk()
            logger.info(
                f"EvolutionStore saved snapshot '{snapshot.snapshot_id}': "
                f"Plans={snapshot.optimization_plans_applied}, "
                f"Experiments={len(snapshot.active_experiments)}, "
                f"Insights={snapshot.learning_insights_count}"
            )
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> Optional[EvolutionSnapshot]:
        """Retrieves a specific snapshot by ID."""
        with self._lock:
            return self._snapshots.get(snapshot_id)

    def list_snapshots(self) -> List[EvolutionSnapshot]:
        """Returns all stored snapshots."""
        with self._lock:
            return list(self._snapshots.values())

    def get_latest_snapshot(self) -> Optional[EvolutionSnapshot]:
        """Returns the most recent snapshot."""
        with self._lock:
            if not self._snapshots:
                return None
            return max(self._snapshots.values(), key=lambda s: s.snapshot_at)

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Deletes a snapshot by ID."""
        with self._lock:
            if snapshot_id in self._snapshots:
                del self._snapshots[snapshot_id]
                self._save_to_disk()
                logger.info(f"EvolutionStore deleted snapshot '{snapshot_id}'.")
                return True
            return False


# Global EvolutionStore instance
evolution_store = EvolutionStore()
