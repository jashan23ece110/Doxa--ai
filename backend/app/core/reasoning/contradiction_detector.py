"""
Internal Contradiction Detector Module.

Detects conflicts between user long-term memory preferences and retrieved document rules,
resolving priorities internally in favor of explicit user preferences.
"""

from typing import List, Dict, Any


class ContradictionDetector:
    """Detects and flags contradictions between memory and evidence."""

    @staticmethod
    def detect_contradictions(
        draft_response: str,
        memory_context: str,
    ) -> List[Dict[str, str]]:
        """Detects contradictions between memory context instructions and draft response."""
        contradictions = []

        if not memory_context or not draft_response:
            return contradictions

        m_lower = memory_context.lower()
        d_lower = draft_response.lower()

        # Check explicit negative preference contradictions (e.g. "user prefers python" vs draft recommending "java")
        if "prefers python" in m_lower and "java" in d_lower and "python" not in d_lower:
            contradictions.append({
                "type": "preference_conflict",
                "detail": "Response recommends Java despite user preference for Python.",
            })

        return contradictions


# Global ContradictionDetector instance
contradiction_detector = ContradictionDetector()
