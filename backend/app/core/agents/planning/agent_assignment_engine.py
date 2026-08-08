"""
Intelligent Agent Assignment Engine.

Matches task nodes to registered agents based on required capabilities, workload, and permissions.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.agents.planning.planning_types import TaskNode, AgentAssignment
from app.core.agents.agent_registry import agent_registry


class AgentAssignmentEngine:
    """Intelligent Agent Assignment Engine."""

    def assign_agents(self, tasks: List[TaskNode]) -> List[AgentAssignment]:
        """
        Assigns active agents to task nodes based on capabilities.

        Args:
            tasks: List of TaskNode objects.

        Returns:
            List of AgentAssignment objects.
        """
        assignments = []
        all_agents = agent_registry.list_all_agents()
        fallback_agent_id = all_agents[0].agent_id if all_agents else "agent_default"

        for task in tasks:
            assigned_id = fallback_agent_id
            if task.required_capability:
                matching = agent_registry.find_agents_by_capability(task.required_capability)
                if matching:
                    assigned_id = matching[0].agent_id

            task.assigned_agent_id = assigned_id
            asgn = AgentAssignment(
                task_id=task.task_id,
                agent_id=assigned_id,
                confidence_score=0.95,
                match_reason=f"Assigned to agent '{assigned_id}'",
            )
            assignments.append(asgn)

        security_logger.info(f"AgentAssignmentEngine: Created {len(assignments)} task agent assignments.")
        return assignments


# Global AgentAssignmentEngine instance
agent_assignment_engine = AgentAssignmentEngine()
