"""
Mission Manager Orchestrator for Autonomous Mission Control System.

Central lifecycle manager for mission creation, goal hierarchy resolution, workflow delegation,
progress monitoring, milestone evaluation, adaptive replanning, failure recovery, and completion.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.missions.adaptive_goal_engine import adaptive_goal_engine
from app.core.missions.goal_manager import goal_manager
from app.core.missions.milestone_engine import milestone_engine
from app.core.missions.mission_metrics import mission_metrics_tracker
from app.core.missions.mission_models import Mission, MissionState, Milestone
from app.core.missions.mission_recovery import mission_recovery
from app.core.missions.mission_repository import mission_repository
from app.core.missions.progress_tracker import progress_tracker
from app.core.workflows.workflow_engine import workflow_engine


class MissionManager:
    """Central lifecycle orchestrator for Long-Horizon Autonomous Missions."""

    async def create_and_execute_mission(
        self,
        primary_goal_prompt: str,
        user_id: str = "default_user",
    ) -> Mission:
        """
        Executes complete long-horizon mission lifecycle:
        Prompt -> Goal Hierarchy -> Milestone Setup -> Workflow Execution -> Progress Tracking -> Milestones -> Persistence.
        """
        start_t = time.time()

        # 1. Create Mission Instance
        mission = Mission(
            name=f"Mission: {primary_goal_prompt[:40]}",
            user_id=user_id,
            primary_goal=primary_goal_prompt,
            status=MissionState.RUNNING,
        )

        # 2. Build Goal Hierarchy Tree
        mission.goals = goal_manager.build_goal_hierarchy_from_prompt(primary_goal_prompt)

        # 3. Setup Default Milestones
        mission.milestones = milestone_engine.generate_default_milestones(mission)

        # Persist Initial State
        mission_repository.save_mission(mission)
        mission_metrics_tracker.active_missions_count += 1

        try:
            # 4. Execute Goals sequentially/hierarchically via WorkflowEngine
            for goal_item in list(mission.goals.values()):
                logger.info(f"Executing goal '{goal_item.goal_id}' ({goal_item.title}) for mission '{mission.mission_id}'.")

                # Delegate goal execution to Autonomous Workflow Execution Engine
                wf_res = await workflow_engine.execute_goal_workflow(
                    goal_item.description,
                    user_id=user_id,
                    policy="highest_quality",
                )

                goal_item.completed = True
                goal_item.output = wf_res.output
                goal_item.workflow_id = wf_res.workflow_id

                # Update progress percentage snapshot
                progress_tracker.update_mission_progress(mission)

                # Evaluate Milestones
                milestone_engine.evaluate_milestones(mission)

                # Scan and adapt goals dynamically if needed
                adaptive_goal_engine.adapt_mission_goals(mission)

            # Mark Mission Complete
            mission.status = MissionState.COMPLETED
            duration_s = round(time.time() - start_t, 2)
            mission_metrics_tracker.record_mission_completion(duration_s=duration_s)
            mission_metrics_tracker.active_missions_count = max(0, mission_metrics_tracker.active_missions_count - 1)

            mission_repository.save_mission(mission)
            logger.info(f"MissionManager successfully completed mission '{mission.mission_id}' in {duration_s}s.")
            return mission

        except Exception as e:
            logger.error(f"Mission '{mission.mission_id}' execution failed: {e}")
            mission_recovery.handle_mission_failure(mission, failed_component="WorkflowEngine", error_message=str(e))
            mission.status = MissionState.FAILED
            mission_metrics_tracker.failed_missions_count += 1
            mission_metrics_tracker.active_missions_count = max(0, mission_metrics_tracker.active_missions_count - 1)
            mission_repository.save_mission(mission)
            return mission

    def pause_mission(self, mission_id: str) -> Optional[Mission]:
        """Pauses a running mission."""
        mission = mission_repository.get_mission(mission_id)
        if mission and mission.status == MissionState.RUNNING:
            mission.status = MissionState.PAUSED
            mission_repository.save_mission(mission)
        return mission

    def resume_mission(self, mission_id: str) -> Optional[Mission]:
        """Resumes a paused mission."""
        mission = mission_repository.get_mission(mission_id)
        if mission and mission.status == MissionState.PAUSED:
            mission.status = MissionState.RUNNING
            mission_repository.save_mission(mission)
        return mission


# Global MissionManager instance
mission_manager = MissionManager()
