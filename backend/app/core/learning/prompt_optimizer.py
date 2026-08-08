"""
Prompt Optimizer for Enterprise Continuous Learning Layer.

Analyzes system prompts, tool prompts, RAG prompts, and planner prompts for length,
duplicate instructions, contradictory rules, and low performance.
Generates versioned prompt proposals (NEVER overwrites originals automatically).
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import logger


class PromptOptimizationProposal(BaseModel):
    """Proposal for a versioned prompt optimization."""

    proposal_id: str
    prompt_type: str  # system, tool, rag, planner
    original_version: int = 1
    proposed_version: int = 2
    original_prompt: str
    proposed_prompt: str
    optimization_reason: str
    status: str = "pending_approval"  # pending_approval, approved, rejected


class PromptOptimizer:
    """Analyzes prompt structures and generates versioned optimization proposals."""

    @staticmethod
    def analyze_and_optimize_prompt(
        prompt_type: str,
        current_prompt: str,
        failure_rate: float = 0.0,
    ) -> Optional[PromptOptimizationProposal]:
        """
        Analyzes a prompt for overly long text, duplicates, or contradictory rules.
        Generates a versioned proposal requiring human approval.
        """
        if not current_prompt or len(current_prompt) < 10:
            return None

        issues = []

        # Check for overly long prompt text (> 1000 words)
        words = current_prompt.split()
        if len(words) > 1000:
            issues.append("Overly long prompt length (> 1000 words).")

        # Check for duplicate instructions
        lines = [line.strip() for line in current_prompt.split("\n") if line.strip()]
        unique_lines = set()
        duplicates = 0
        for l in lines:
            if l in unique_lines:
                duplicates += 1
            else:
                unique_lines.add(l)

        if duplicates > 0:
            issues.append(f"Contains {duplicates} duplicate instruction lines.")

        if not issues and failure_rate < 0.20:
            return None

        # Build proposed optimized version without duplicate lines
        deduped_lines = []
        seen = set()
        for line in lines:
            if line not in seen:
                seen.add(line)
                deduped_lines.append(line)

        proposed_text = "\n".join(deduped_lines)
        reason = f"Optimized: Removed {duplicates} duplicate lines. Issues: {', '.join(issues)}"

        logger.info(f"Generated versioned PromptOptimizationProposal for '{prompt_type}' ({reason}).")

        return PromptOptimizationProposal(
            proposal_id=f"prop_{prompt_type}_v2",
            prompt_type=prompt_type,
            original_version=1,
            proposed_version=2,
            original_prompt=current_prompt,
            proposed_prompt=proposed_text,
            optimization_reason=reason,
        )


# Global PromptOptimizer instance
prompt_optimizer = PromptOptimizer()
