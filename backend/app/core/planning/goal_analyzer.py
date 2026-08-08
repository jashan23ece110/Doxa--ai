"""
Goal Analyzer for Enterprise Planning & Reasoning Engine.

Analyzes user prompts to extract primary goal, secondary goals, constraints, deadlines,
required tools, required knowledge, complexity, ambiguity score, estimated cost, and confidence.
"""

from typing import Dict, Any, List
from app.core.planning.planning_models import Goal


class GoalAnalyzer:
    """Analyzes prompt intent and constructs structured Goal graph model."""

    @staticmethod
    def analyze_goal(prompt: str) -> Goal:
        """Analyzes a prompt request and builds a structured Goal representation."""
        clean = prompt.strip()
        clean_lower = clean.lower()

        primary = clean[:120]
        secondary: List[str] = []
        constraints: List[str] = []
        required_tools: List[str] = []
        required_knowledge: List[str] = []
        complexity = "medium"
        ambiguity = 0.20
        estimated_cost = 0.05
        confidence = 0.90

        # Detect tool requirements
        if any(kw in clean_lower for kw in ["search", "find", "lookup"]):
            required_tools.append("web_search")
            required_tools.append("document_search")
        if any(kw in clean_lower for kw in ["code", "python", "script", "calculate"]):
            required_tools.append("execute_python_code")

        # Detect complexity
        word_count = len(clean.split())
        if word_count > 100 or "research" in clean_lower or "compare" in clean_lower:
            complexity = "research"
            ambiguity = 0.35
            estimated_cost = 0.15
            secondary.append("Conduct comprehensive domain research")
            secondary.append("Synthesize multi-source insights")
        elif "code" in clean_lower or "build" in clean_lower:
            complexity = "complex"
            estimated_cost = 0.10
            secondary.append("Generate and verify code architecture")
        elif word_count < 15:
            complexity = "simple"
            ambiguity = 0.10
            estimated_cost = 0.01

        # Detect constraints
        if "fast" in clean_lower or "quick" in clean_lower:
            constraints.append("Low latency completion requirement")

        return Goal(
            description=clean,
            primary_objective=primary,
            secondary_objectives=secondary,
            constraints=constraints,
            required_tools=required_tools,
            required_knowledge=required_knowledge,
            complexity=complexity,
            ambiguity_score=ambiguity,
            estimated_cost=estimated_cost,
            confidence=confidence,
        )


# Global GoalAnalyzer instance
goal_analyzer = GoalAnalyzer()
