"""
Insider Risk Case Workspace Manager.

Manages insider risk investigation cases, analyst notes, evidence references,
linked assessments, recommendations, investigation history, and case lifecycles.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class InsiderCaseNote(BaseModel):
    note_id: str
    author: str = "secops_analyst"
    content: str
    timestamp: float = Field(default_factory=time.time)


class InsiderInvestigationCase(BaseModel):
    case_id: str
    employee_id: str
    status: str = "open"  # open, triaged, investigating, resolved, closed
    lead_analyst: str = "secops_analyst"
    notes: List[InsiderCaseNote] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class InsiderCaseManager:
    """Thread-safe Insider Risk Case Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._cases: Dict[str, InsiderInvestigationCase] = {}

    def create_case(self, case_id: str, employee_id: str, lead_analyst: str = "secops_analyst") -> InsiderInvestigationCase:
        """Creates a new insider risk investigation case."""
        case = InsiderInvestigationCase(case_id=case_id, employee_id=employee_id, lead_analyst=lead_analyst)
        with self._lock:
            self._cases[case_id] = case
            security_logger.info(f"InsiderCaseManager: Created insider case '{case_id}' for employee '{employee_id}'.")
        return case

    def add_note(self, case_id: str, content: str, author: str = "secops_analyst") -> Optional[InsiderCaseNote]:
        """Adds an analyst note to the case."""
        with self._lock:
            case = self._cases.get(case_id)
            if case:
                note = InsiderCaseNote(note_id=f"icn_{len(case.notes) + 1}", author=author, content=content)
                case.notes.append(note)
                security_logger.info(f"InsiderCaseManager: Added note to insider case '{case_id}'.")
                return note
        return None

    def get_case(self, case_id: str) -> Optional[InsiderInvestigationCase]:
        """Retrieves investigation case."""
        with self._lock:
            return self._cases.get(case_id)


# Global InsiderCaseManager instance
insider_case_manager = InsiderCaseManager()
