"""
Critic Agent Implementation.

Audits gathered evidence for hallucinations, contradictions, and factual validity.
"""

from typing import Dict, Any
from app.core.agents.base import BaseAgent
from app.core.agents.workspace import SharedWorkingMemory
from app.core.reasoning.evidence_verifier import evidence_verifier


class CriticAgent(BaseAgent):
    """Audits evidence and challenges assumptions for factual consistency."""

    def __init__(self):
        super().__init__(
            role_name="critic",
            description="Audits gathered evidence for hallucinations, missing details, and contradictions.",
        )

    async def _run_agent_logic(
        self,
        task: Dict[str, Any],
        workspace: SharedWorkingMemory,
    ) -> Dict[str, Any]:
        evidence = workspace.get_all_evidence()
        all_outputs = workspace.get_all_outputs()

        researcher_output = all_outputs.get("researcher", {}).get("output", "")
        contexts = all_outputs.get("researcher", {}).get("evidence", [])

        # Run internal EvidenceVerifier pass
        verification = evidence_verifier.verify_draft_evidence(
            draft_response=researcher_output,
            contexts=contexts,
        )

        return {
            "role": self.role_name,
            "status": "completed",
            "support_status": verification.get("support_status", "supported"),
            "grounded_ratio": verification.get("grounded_ratio", 1.0),
            "output": f"Factual audit completed: support_status={verification.get('support_status')}.",
            "confidence": 0.90,
        }
