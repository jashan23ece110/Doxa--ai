"""
Enterprise Failure Learning Engine.

Analyzes operational and tool failures to categorize root causes and derive prevention patterns.
"""

from typing import Dict, Any
from app.core.logging import security_logger
from app.core.agents.autonomy.agent_memory_types import FailurePattern


class FailureLearningEngine:
    """Enterprise Failure Learning Engine."""

    def analyze_failure(self, task_id: str, error_message: str) -> FailurePattern:
        """
        Categorizes failure and generates actionable prevention recommendations.

        Args:
            task_id: Task ID string.
            error_message: Log error message string.

        Returns:
            FailurePattern object.
        """
        category = "TOOL_TIMEOUT" if "timeout" in error_message.lower() else "EXECUTION_ERROR"
        fpat = FailurePattern(
            category=category,
            root_cause=f"Error log matched: {error_message[:80]}",
            prevention_recommendation="Increase retry exponential backoff or use cached fallback.",
        )

        security_logger.info(f"FailureLearningEngine: Categorized failure for task '{task_id}' as '{category}'.")
        return fpat


# Global FailureLearningEngine instance
failure_learning_engine = FailureLearningEngine()
