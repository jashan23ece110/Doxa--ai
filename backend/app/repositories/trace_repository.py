"""
Trace Repository for Agent Execution Traces with Firestore and Memory Fallback.

Implements ITraceRepository interface.
"""

from typing import Dict, Any, Optional
from app.core.interfaces.trace_repository import ITraceRepository
from app.core.logging import logger

_global_traces: Dict[str, Dict[str, Any]] = {}


class TraceRepository(ITraceRepository):
    """Encapsulates Firestore document operations for agent run traces with memory fallback."""

    def __init__(self):
        self._db = None
        self._firestore_init_attempted = False

    def _get_db(self):
        """Lazy-initializes Firestore Client if credentials/SDK are available."""
        if not self._firestore_init_attempted:
            self._firestore_init_attempted = True
            try:
                from google.cloud import firestore
                self._db = firestore.Client()
                logger.info("Successfully connected to Google Cloud Firestore.")
            except Exception as e:
                logger.info(f"Firestore unavailable ({e}). Falling back to in-memory trace storage.")
                self._db = None
        return self._db

    def save_trace(self, run_id: str, trace: Dict[str, Any]) -> None:
        """Saves execution trace to Firestore or in-memory dictionary."""
        _global_traces[run_id] = trace
        db = self._get_db()
        if db:
            try:
                db.collection("traces").document(run_id).set(trace)
            except Exception as e:
                logger.warning(f"Failed to persist trace {run_id} to Firestore: {e}")

    def get_trace(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves execution trace by run_id."""
        db = self._get_db()
        if db:
            try:
                doc = db.collection("traces").document(run_id).get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                logger.warning(f"Failed to read trace {run_id} from Firestore: {e}")

        return _global_traces.get(run_id)


trace_repository = TraceRepository()
