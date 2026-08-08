"""
Internal Evidence Verifier Module.

Checks factual statements in draft responses against retrieved document evidence and memory,
classifying support levels internally (supported, weak, unsupported) without exposing CoT traces.
"""

from typing import List, Dict, Any


class EvidenceVerifier:
    """Verifies response claims against evidence blocks internally."""

    @staticmethod
    def verify_draft_evidence(
        draft_response: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
    ) -> Dict[str, Any]:
        """
        Inspects draft response statements and determines internal evidence support level.
        """
        if not draft_response or not draft_response.strip():
            return {"support_status": "unsupported", "grounded_ratio": 0.0}

        if not contexts and not memory_context:
            return {"support_status": "supported", "grounded_ratio": 1.0}

        # Combine evidence text
        evidence_corpus = " ".join([c.get("text", "") for c in contexts]) + " " + memory_context
        evidence_words = set(evidence_corpus.lower().split())

        draft_words = set(draft_response.lower().split())
        if not draft_words:
            return {"support_status": "supported", "grounded_ratio": 1.0}

        matched = draft_words.intersection(evidence_words)
        grounded_ratio = len(matched) / len(draft_words)

        if grounded_ratio >= 0.35:
            status = "supported"
        elif grounded_ratio >= 0.15:
            status = "weak"
        else:
            status = "unsupported"

        return {
            "support_status": status,
            "grounded_ratio": round(grounded_ratio, 2),
        }


# Global EvidenceVerifier instance
evidence_verifier = EvidenceVerifier()
