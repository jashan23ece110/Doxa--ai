"""
Enterprise Investigation Case Workspace.

Manages investigation cases, linked security incidents, forensic evidence,
assigned analysts, investigation notes, findings, recommendations, case history, and reporting.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CaseNote(BaseModel):
    note_id: str
    author: str = "analyst_1"
    content: str
    timestamp: float = Field(default_factory=time.time)


class SecOpsInvestigationCase(BaseModel):
    case_id: str
    title: str
    status: str = "open"  # open, triaged, in_review, closed
    lead_analyst: str = "analyst_1"
    linked_incidents: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    notes: List[CaseNote] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class SecOpsCaseManager:
    """Thread-safe SecOps Investigation Workspace Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cases: Dict[str, SecOpsInvestigationCase] = {}

    def create_case(self, case_id: str, title: str, lead_analyst: str = "analyst_1") -> SecOpsInvestigationCase:
        """Creates a new investigation case workspace."""
        case = SecOpsInvestigationCase(case_id=case_id, title=title, lead_analyst=lead_analyst)
        with self._lock:
            self._cases[case_id] = case
            security_logger.info(f"SecOpsCaseManager: Created investigation case '{title}' ({case_id}).")
        return case

    def add_note(self, case_id: str, content: str, author: str = "analyst_1") -> Optional[CaseNote]:
        """Adds an analyst note to the case."""
        with self._lock:
            case = self._cases.get(case_id)
            if case:
                note = CaseNote(note_id=f"cn_{len(case.notes) + 1}", author=author, content=content)
                case.notes.append(note)
                security_logger.info(f"SecOpsCaseManager: Added note to case '{case_id}'.")
                return note
        return None

    def get_case(self, case_id: str) -> Optional[SecOpsInvestigationCase]:
        """Retrieves investigation case."""
        with self._lock:
            return self._cases.get(case_id)


# Global SecOpsCaseManager instance
secops_case_manager = SecOpsCaseManager()
