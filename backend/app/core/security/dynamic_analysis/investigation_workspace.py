"""
Investigation Workspace.

Manages investigation sessions, assigned analysts, evidence artifacts, notes,
timelines, linked binaries, related investigations, and case status lifecycle.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class InvestigationCase(BaseModel):
    case_id: str
    title: str
    assigned_analyst: str = "analyst_1"
    status: str = "open"  # open, investigating, resolved, closed
    linked_binary_ids: List[str] = Field(default_factory=list)
    linked_evidence_ids: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class InvestigationWorkspace:
    """Thread-safe Investigation Workspace Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cases: Dict[str, InvestigationCase] = {}

    def create_case(self, case_id: str, title: str, binary_id: str, analyst: str = "analyst_1") -> InvestigationCase:
        """Creates a new security investigation case."""
        case = InvestigationCase(
            case_id=case_id,
            title=title,
            assigned_analyst=analyst,
            linked_binary_ids=[binary_id],
        )
        with self._lock:
            self._cases[case_id] = case
            security_logger.info(f"InvestigationWorkspace: Created case '{title}' ({case_id}).")
        return case

    def link_evidence(self, case_id: str, artifact_id: str) -> bool:
        """Links a forensic evidence artifact to a case."""
        with self._lock:
            case = self._cases.get(case_id)
            if case and artifact_id not in case.linked_evidence_ids:
                case.linked_evidence_ids.append(artifact_id)
                security_logger.info(f"InvestigationWorkspace: Linked evidence '{artifact_id}' to case '{case_id}'.")
                return True
        return False

    def get_case(self, case_id: str) -> Optional[InvestigationCase]:
        """Retrieves investigation case details."""
        with self._lock:
            return self._cases.get(case_id)


# Global InvestigationWorkspace instance
investigation_workspace = InvestigationWorkspace()
