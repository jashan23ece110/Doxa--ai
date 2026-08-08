"""
Answer Reviser Engine for Enterprise Cognitive Reasoning.

Performs targeted regeneration/refinement of ungrounded or contradictory response sections.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.core.logging import logger
from app.core.reasoning.reflection_engine import reflection_engine


class AnswerReviser:
    """Performs targeted answer revision based on verification & reflection feedback."""

    @staticmethod
    def revise_draft_response(
        draft_response: str,
        query: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
        verification_result: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, int]:
        """
        Refines draft response to correct unsupported claims or contradictions.
        Returns: (revised_response, revision_count)
        """
        if not draft_response or not draft_response.strip():
            return draft_response, 0

        contradictions = verification_result.get("contradictions", []) if verification_result else []
        unsupported = verification_result.get("unsupported_statements", []) if verification_result else []

        if not contradictions and not unsupported:
            return draft_response, 0

        logger.info(f"AnswerReviser triggered: {len(contradictions)} contradictions, {len(unsupported)} unsupported statements.")

        # Execute targeted refinement via ReflectionEngine
        revised = reflection_engine.refine_response_draft(
            draft_response=draft_response,
            query=query,
            contexts=contexts,
            memory_context=memory_context,
            contradictions=contradictions,
        )

        return revised, 1


# Global AnswerReviser instance
answer_reviser = AnswerReviser()
