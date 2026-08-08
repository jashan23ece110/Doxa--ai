"""
Enterprise Training Engine.

Manages security awareness training modules, learning paths, role-based content,
completion tracking, certification history, and refresher scheduling.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import SecurityTrainingRecord


class TrainingModule(BaseModel):
    module_id: str
    title: str
    category: str  # phishing, password_security, remote_work, social_engineering
    duration_minutes: int = 15
    role_target: str = "all"


class EnterpriseTrainingEngine:
    """Enterprise Training Engine."""

    def __init__(self):
        self._records: Dict[str, List[SecurityTrainingRecord]] = {}  # employee_id -> records

    def assign_training(self, employee_id: str, course_name: str) -> SecurityTrainingRecord:
        """Assigns a training module to an employee."""
        rec = SecurityTrainingRecord(
            employee_id=employee_id,
            course_name=course_name,
            status="assigned",
        )
        if employee_id not in self._records:
            self._records[employee_id] = []
        self._records[employee_id].append(rec)
        security_logger.info(f"EnterpriseTrainingEngine: Assigned training '{course_name}' to employee '{employee_id}'.")
        return rec

    def complete_training(self, record_id: str, employee_id: str) -> Optional[SecurityTrainingRecord]:
        """Marks training record as completed."""
        records = self._records.get(employee_id, [])
        for r in records:
            if r.record_id == record_id:
                r.status = "completed"
                r.completion_date = time.time()
                security_logger.info(f"EnterpriseTrainingEngine: Employee '{employee_id}' completed training record '{record_id}'.")
                return r
        return None


# Global EnterpriseTrainingEngine instance
enterprise_training_engine = EnterpriseTrainingEngine()
