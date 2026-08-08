"""
Milestone Engine for Autonomous Mission Control System.

Validates automatic and manual milestones, tracking completion rewards and progress summaries.
"""

import time
from typing import List, Dict, Any
from app.core.logging import logger
from app.core.missions.mission_metrics import mission_metrics_tracker
from app.core.missions.mission_models import Mission, Milestone


class MilestoneEngine:
    """Evaluates and validates mission milestones."""

    @staticmethod
    def generate_default_milestones(mission: Mission) -> List[Milestone]:
        """Generates standard mission milestones based on goal hierarchy."""
        ms1 = Milestone(
            title="Phase 1: Domain & Architectural Specification",
            description="Complete initial research and architectural design.",
            reward_score=1.0,
        )
        ms2 = Milestone(
            title="Phase 2: Autonomous Implementation & Synthesis",
            description="Execute implementation workflows and verify output.",
            reward_score=2.0,
        )
        return [ms1, ms2]

    @staticmethod
    def evaluate_milestones(mission: Mission) -> int:
        """
        Checks goal completion statuses and marks completed milestones.
        Returns: number of newly completed milestones.
        """
        completed_count = 0
        total_goals = len(mission.goals)
        completed_goals = sum(1 for g in mission.goals.values() if g.completed)
        ratio = completed_goals / max(total_goals, 1)

        for idx, ms in enumerate(mission.milestones):
            if not ms.completed:
                # Mark first milestone at 50% completion, second at 100%
                threshold = (idx + 1) * 0.50
                if ratio >= threshold:
                    ms.completed = True
                    ms.completed_at = time.time()
                    completed_count += 1
                    mission_metrics_tracker.record_milestone_completion()
                    logger.info(f"Milestone '{ms.title}' achieved for mission '{mission.mission_id}'.")

        return completed_count


# Global MilestoneEngine instance
milestone_engine = MilestoneEngine()
