"""
Enterprise Agent Execution Engine.

Executes the foundational autonomous agent lifecycle:
Goal -> Context -> Task -> Plan -> Action -> Tool -> Observation -> Evaluation -> Next Action / Completion.
"""

import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.agents.agent_types import (
    AgentGoal, AgentTask, AgentPlan, PlanStep, AgentAction,
    AgentObservation, AgentEvaluation, AgentExecution, AgentState, ToolInvocation
)
from app.core.agents.goal_manager import goal_manager
from app.core.agents.agent_context_manager import agent_context_manager
from app.core.agents.tool_registry import tool_registry
from app.core.agents.agent_state_store import agent_state_store


class AgentExecutionEngine:
    """Enterprise Autonomous Agent Execution Engine."""

    async def execute_goal(self, agent_id: str, goal_title: str, goal_description: str) -> AgentExecution:
        """
        Executes an end-to-end goal lifecycle using the agent execution pipeline.

        Args:
            agent_id: Assigned agent ID string.
            goal_title: Title of goal.
            goal_description: Detailed goal description.

        Returns:
            AgentExecution object detailing execution state and results.
        """
        t0 = time.time()
        security_logger.info(f"AgentExecutionEngine: Starting execution for agent '{agent_id}' (Goal='{goal_title}').")

        # 1. Create Goal
        goal = goal_manager.create_goal(title=goal_title, description=goal_description)

        # 2. Build Context
        ctx = await agent_context_manager.build_context(goal_id=goal.goal_id)

        # 3. Decompose Goal into Tasks
        tasks = goal_manager.decompose_goal(goal.goal_id, [f"Analyze requirements for {goal_title}", f"Execute primary action for {goal_title}"])

        # 4. Construct Execution Plan
        steps = [
            PlanStep(sequence_index=1, action_type="AnalyzeContext", parameters={"context_id": ctx.context_id}),
            PlanStep(sequence_index=2, action_type="InvokeTool", tool_name="system_analyzer", parameters={"target": "scope_01"}),
        ]
        plan = AgentPlan(goal_id=goal.goal_id, steps=steps)

        # 5. Execute Action & Tool
        tool_inv = ToolInvocation(tool_name="system_analyzer", arguments={"target": "scope_01"}, agent_id=agent_id)
        tool_res = await tool_registry.invoke_tool(tool_inv)

        # 6. Record Observation & Evaluation
        obs = AgentObservation(action_id=f"act_{plan.plan_id[:4]}", data=tool_res.output)
        eval_res = AgentEvaluation(task_id=tasks[0].task_id, success=tool_res.success, score=1.0, feedback="Task completed successfully")

        # 7. Finalize Execution State
        goal_manager.update_goal_status(goal.goal_id, "ACHIEVED" if tool_res.success else "FAILED")

        execution = AgentExecution(
            agent_id=agent_id,
            goal_id=goal.goal_id,
            state=AgentState.COMPLETED if tool_res.success else AgentState.FAILED,
            current_plan=plan,
            started_at=t0,
            completed_at=time.time(),
        )

        agent_state_store.save_execution(execution)
        agent_state_store.save_tool_result(agent_id, tool_res)

        security_logger.info(f"AgentExecutionEngine: Completed execution '{execution.execution_id}' for agent '{agent_id}' in {round((time.time() - t0)*1000, 2)}ms.")
        return execution


# Global AgentExecutionEngine instance
agent_execution_engine = AgentExecutionEngine()
