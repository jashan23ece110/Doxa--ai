"""
Task Router for Enterprise Multi-Agent Framework.

Classifies query task types and maps them to optimal agent execution teams.
"""

from typing import List, Tuple, Dict, Any


class TaskRouter:
    """Routes user queries to specialized agent teams."""

    @staticmethod
    def route_task(prompt: str) -> Tuple[str, List[str]]:
        """
        Analyzes prompt and selects agent team.
        Returns: (task_category, list_of_agent_names)
        """
        if not prompt or not prompt.strip():
            return "simple", ["WriterAgent"]

        clean = prompt.strip().lower()
        word_count = len(clean.split())

        # Research Questions
        if any(kw in clean for kw in ["search", "find", "who is", "what is", "where", "latest"]):
            return "research", ["ResearcherAgent", "RetrieverAgent", "VerifierAgent", "WriterAgent"]

        # Coding Questions
        if any(kw in clean for kw in ["code", "python", "function", "bug", "refactor", "api", "schema"]):
            return "coding", ["PlannerAgent", "ReasoningAgent", "CriticAgent", "WriterAgent"]

        # Complex Reports
        if word_count > 12 or any(kw in clean for kw in ["analyze", "compare", "plan", "strategy", "roadmap"]):
            return "complex", [
                "PlannerAgent",
                "RetrieverAgent",
                "ResearcherAgent",
                "ReasoningAgent",
                "CriticAgent",
                "VerifierAgent",
                "WriterAgent",
                "SynthesizerAgent",
            ]

        # Simple Query
        return "simple", ["RetrieverAgent", "WriterAgent"]


# Global TaskRouter instance
task_router = TaskRouter()
