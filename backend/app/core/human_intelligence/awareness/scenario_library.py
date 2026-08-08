"""
Simulation Scenario Library.

Maintains repository of synthetic security scenarios (phishing, pretexting, impersonation,
QR-code, USB drop awareness, remote work, executive targeting) with versioning and tagging.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.human_intelligence.human_intelligence_types import SocialEngineeringScenario


class ScenarioLibrary:
    """Enterprise Scenario Library Repository."""

    def __init__(self):
        self._scenarios: Dict[str, SocialEngineeringScenario] = {
            "scen_01": SocialEngineeringScenario(
                scenario_id="scen_01",
                title="Synthetic QR Code Sign-In Awareness",
                vector="QR Code",
                difficulty="medium",
                defensive_guidance="Never scan unverified QR codes for corporate sign-ins; navigate directly to official URLs.",
            ),
            "scen_02": SocialEngineeringScenario(
                scenario_id="scen_02",
                title="Executive Impersonation Pretexting Awareness",
                vector="email",
                difficulty="hard",
                defensive_guidance="Verify wire transfer or credential change requests via out-of-band communication channel.",
            ),
        }

    def get_scenario(self, scenario_id: str) -> Optional[SocialEngineeringScenario]:
        """Retrieves scenario definition."""
        return self._scenarios.get(scenario_id)

    def list_scenarios(self) -> List[SocialEngineeringScenario]:
        """Lists all registered educational scenario templates."""
        return list(self._scenarios.values())


# Global ScenarioLibrary instance
scenario_library = ScenarioLibrary()
