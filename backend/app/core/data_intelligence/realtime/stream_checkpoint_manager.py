"""
Checkpoint and Recovery Engine.

Manages periodic stream checkpoints, partition offset persistence, state snapshots,
recovery points, stream event replay, and failure recovery.
"""

import threading
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class StreamCheckpoint(BaseModel):
    checkpoint_id: str
    stream_id: str
    partition_offsets: Dict[int, int] = Field(default_factory=dict)  # partition_id -> offset
    snapshot_state_hash: str = "hash_default"
    checkpointed_at: float = Field(default_factory=time.time)


class StreamCheckpointManager:
    """Thread-safe Stream Checkpoint Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._checkpoints: Dict[str, StreamCheckpoint] = {}

    def create_checkpoint(self, stream_id: str, partition_offsets: Dict[int, int]) -> StreamCheckpoint:
        """Creates a stream processing checkpoint."""
        cp = StreamCheckpoint(
            checkpoint_id=f"cp_strm_{stream_id[:4]}_{int(time.time() * 1000)}",
            stream_id=stream_id,
            partition_offsets=partition_offsets,
        )
        with self._lock:
            self._checkpoints[stream_id] = cp
            security_logger.info(f"StreamCheckpointManager: Created checkpoint '{cp.checkpoint_id}' for stream '{stream_id}'.")
        return cp

    def get_latest_checkpoint(self, stream_id: str) -> Optional[StreamCheckpoint]:
        """Retrieves latest checkpoint for a stream."""
        with self._lock:
            return self._checkpoints.get(stream_id)


# Global StreamCheckpointManager instance
stream_checkpoint_manager = StreamCheckpointManager()
