"""
Enterprise Phishing Simulation Engine.

Provides safe, synthetic security awareness simulations (email, SMS, QR-code, voice/social engineering, fake login).
Evaluates mock employee responses for educational scoring.
Contains ZERO credential collection and ZERO outbound network email delivery.
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import PhishingSimulation


class MockSimulationResult(BaseModel):
    simulation_id: str
    employee_id: str
    scenario_type: str  # email_awareness, qr_code_awareness, sms_awareness
    recognized_indicator: bool = True
    reported_to_secops: bool = True
    educational_feedback: str


class PhishingSimulationEngine:
    """Enterprise Safe Phishing Simulation Engine."""

    def evaluate_mock_interaction(
        self,
        employee_id: str,
        scenario_type: str,
        user_reported: bool = True,
        user_clicked_link: bool = False,
    ) -> MockSimulationResult:
        """
        Evaluates a synthetic educational awareness interaction.

        Args:
            employee_id: Target employee ID.
            scenario_type: Scenario category string.
            user_reported: Whether employee correctly reported the simulated test.
            user_clicked_link: Whether employee clicked simulated link.

        Returns:
            MockSimulationResult model.
        """
        recognized = user_reported and not user_clicked_link
        feedback = "Excellent security awareness! Promptly reported suspicious indicator to SecOps." if recognized else "Educational Note: Verify unexpected domain names and sender headers before clicking links."

        res = MockSimulationResult(
            simulation_id=f"psim_eval_{int(time.time() * 1000)}",
            employee_id=employee_id,
            scenario_type=scenario_type,
            recognized_indicator=recognized,
            reported_to_secops=user_reported,
            educational_feedback=feedback,
        )

        security_logger.info(f"PhishingSimulationEngine: Evaluated mock simulation for employee '{employee_id}': Recognized={recognized}")
        return res


# Global PhishingSimulationEngine instance
phishing_simulation_engine = PhishingSimulationEngine()
