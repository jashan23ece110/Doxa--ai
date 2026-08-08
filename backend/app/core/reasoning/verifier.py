"""
Verification Engine for Enterprise Cognitive Reasoning.

Validates draft responses against retrieved document context, user memory, and tool execution outputs.
"""

from typing import List, Dict, Any, Optional
from app.core.reasoning.contradiction_detector import contradiction_detector
from app.core.reasoning.evidence_verifier import evidence_verifier


class VerificationEngine:
    """Validates claims, evidence support, and checks for contradictions."""

    @staticmethod
    def verify_response_evidence(
        draft_response: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
    ) -> Dict[str, Any]:
        """Runs full verification checks on draft response."""
        # 1. Evidence Grounding Verification
        evidence_result = evidence_verifier.verify_draft_evidence(
            draft_response, contexts, memory_context
        )

        # 2. Contradiction Detection
        contradictions = contradiction_detector.detect_contradictions(
            draft_response, memory_context
        )

        is_verified = (
            evidence_result.get("support_status") in ["supported", "weak"]
            and len(contradictions) == 0
        )

        return {
            "verified": is_verified,
            "support_status": evidence_result.get("support_status", "supported"),
            "grounded_ratio": evidence_result.get("grounded_ratio", 1.0),
            "unsupported_statements": evidence_result.get("unsupported_statements", []),
            "contradictions": contradictions,
        }


# Global VerificationEngine instance
verification_engine = VerificationEngine()
