"""
Enterprise Human Intelligence Manager.

Central orchestrator for the Human Intelligence & Social Engineering Defense Platform.
Coordinates profile lifecycles, risk aggregation, assessment processing, training recommendations,
domain event publishing, health checks, and metrics collection.
Integrated with AI OS Kernel, RAG, Memory, and Stage 6 Security Platform.
"""

import time
import threading
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import (
    EmployeeProfile,
    HumanRiskProfile,
    AwarenessAssessment,
    HumanDashboardState,
    HumanRiskLevel,
)
from app.core.human_intelligence.human_pipeline import human_intelligence_pipeline, HumanPipelineResult
from app.core.human_intelligence.human_events import publish_human_event, HumanEventType
from app.core.human_intelligence.human_metrics import human_metrics_tracker


class EnterpriseHumanIntelligenceManager:
    """Master Orchestrator for Enterprise Human Intelligence Platform."""

    def __init__(self):
        self._lock = threading.Lock()
        self._profiles: Dict[str, EmployeeProfile] = {}
        self._risk_profiles: Dict[str, HumanRiskProfile] = {}

    def register_employee_profile(self, name: str, email: str, department: str, role: str) -> EmployeeProfile:
        """Registers a new employee profile in the human intelligence database."""
        profile = EmployeeProfile(name=name, email=email, department=department, role=role)
        with self._lock:
            self._profiles[profile.employee_id] = profile
            self._risk_profiles[profile.employee_id] = HumanRiskProfile(employee_id=profile.employee_id)
        
        human_metrics_tracker.record_profile_created()
        security_logger.info(f"EnterpriseHumanIntelligenceManager: Registered employee '{name}' ({profile.employee_id}).")
        return profile

    async def analyze_human_security_risk(self, employee_id: str) -> HumanPipelineResult:
        """
        Executes full human risk assessment pipeline for an employee.

        Args:
            employee_id: Unique Employee ID.

        Returns:
            HumanPipelineResult object.
        """
        with self._lock:
            profile = self._profiles.get(employee_id)
            if not profile:
                profile = EmployeeProfile(employee_id=employee_id, name="Unknown Employee", email="unknown@doxa.internal", department="General", role="Staff")
                self._profiles[employee_id] = profile

        result = await human_intelligence_pipeline.execute_pipeline(profile)

        with self._lock:
            self._risk_profiles[employee_id] = result.risk_profile

        await publish_human_event(
            event_type=HumanEventType.RISK_SCORE_UPDATED,
            target_id=employee_id,
            data={"risk_score": result.risk_profile.overall_risk_score},
        )

        return result

    def get_dashboard_state(self) -> HumanDashboardState:
        """Retrieves real-time Human Intelligence Dashboard State."""
        metrics = human_metrics_tracker.get_metrics()
        with self._lock:
            metrics.total_employees_monitored = len(self._profiles)
        return HumanDashboardState(metrics=metrics)


# Global EnterpriseHumanIntelligenceManager instance
enterprise_human_intelligence_manager = EnterpriseHumanIntelligenceManager()
