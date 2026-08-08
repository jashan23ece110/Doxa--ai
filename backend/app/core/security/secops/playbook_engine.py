"""
Security Playbook Engine.

Supports incident response playbooks, investigation workflows, evidence collection procedures,
analyst guidance, automation triggers, and workflow versioning.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class PlaybookStep(BaseModel):
    step_number: int
    name: str
    description: str
    automation_trigger: Optional[str] = None
    is_automated: bool = True


class SecOpsPlaybook(BaseModel):
    playbook_id: str
    name: str
    version: str = "1.0.0"
    target_category: str  # malware, phishing, privilege_escalation, data_exfiltration
    steps: List[PlaybookStep] = Field(default_factory=list)


class SecOpsPlaybookEngine:
    """Enterprise Security Playbook Engine."""

    def __init__(self):
        self._playbooks: Dict[str, SecOpsPlaybook] = {
            "malware_triage": SecOpsPlaybook(
                playbook_id="pb_malware_01",
                name="Malware_Triage_and_Containment",
                version="1.1.0",
                target_category="malware",
                steps=[
                    PlaybookStep(step_number=1, name="Isolate Host", description="Isolate affected host from enterprise VLAN.", automation_trigger="network_isolate"),
                    PlaybookStep(step_number=2, name="Quarantine Payload", description="Move payload binary to secure evidence vault.", automation_trigger="file_quarantine"),
                    PlaybookStep(step_number=3, name="Memory Dump", description="Capture memory dump for volatile data extraction.", automation_trigger="memory_capture"),
                ],
            )
        }

    def get_playbook(self, category: str = "malware") -> SecOpsPlaybook:
        """Retrieves default playbook for category."""
        return self._playbooks.get(f"{category}_triage") or self._playbooks["malware_triage"]


# Global SecOpsPlaybookEngine instance
secops_playbook_engine = SecOpsPlaybookEngine()
