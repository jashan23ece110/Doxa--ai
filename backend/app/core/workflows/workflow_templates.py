"""
Workflow Templates for Enterprise Autonomous Workflow Engine.

Provides pre-configured reusable workflow templates for common tasks.
"""

from typing import Dict, Any, List, Optional
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowTask, WorkflowState


class WorkflowTemplates:
    """Pre-configured workflow templates generator."""

    @staticmethod
    def create_research_report_template(user_id: str, goal: str) -> WorkflowInstance:
        """Creates a Research Report workflow instance."""
        wf = WorkflowInstance(
            name=f"Research Report: {goal[:30]}",
            template_name="Research Report",
            user_id=user_id,
            state_variables={"goal": goal},
        )
        wf.tasks = {
            "t1": WorkflowTask(task_id="t1", name="Query Analysis", type="agent_task", assigned_agent="PlannerAgent"),
            "t2": WorkflowTask(task_id="t2", name="Hybrid RAG Search", type="agent_task", assigned_agent="RetrieverAgent", dependencies=["t1"]),
            "t3": WorkflowTask(task_id="t3", name="Web Search Gathering", type="agent_task", assigned_agent="ResearcherAgent", dependencies=["t1"]),
            "t4": WorkflowTask(task_id="t4", name="Cognitive Reasoning", type="agent_task", assigned_agent="ReasoningAgent", dependencies=["t2", "t3"]),
            "t5": WorkflowTask(task_id="t5", name="Evidence Verification", type="agent_task", assigned_agent="VerifierAgent", dependencies=["t4"]),
            "t6": WorkflowTask(task_id="t6", name="Report Synthesis", type="agent_task", assigned_agent="SynthesizerAgent", dependencies=["t5"]),
        }
        return wf

    @staticmethod
    def create_coding_project_template(user_id: str, goal: str) -> WorkflowInstance:
        """Creates a Coding Project workflow instance with approval checkpoint."""
        wf = WorkflowInstance(
            name=f"Coding Project: {goal[:30]}",
            template_name="Coding Project",
            user_id=user_id,
            state_variables={"goal": goal},
        )
        wf.tasks = {
            "t1": WorkflowTask(task_id="t1", name="Architecture Design", type="agent_task", assigned_agent="PlannerAgent"),
            "t2": WorkflowTask(task_id="t2", name="Code Generation & Reasoning", type="agent_task", assigned_agent="ReasoningAgent", dependencies=["t1"]),
            "t3": WorkflowTask(task_id="t3", name="Code Audit & Review", type="agent_task", assigned_agent="CriticAgent", dependencies=["t2"]),
            "t4": WorkflowTask(task_id="t4", name="Human Code Approval", type="approval_checkpoint", requires_approval=True, dependencies=["t3"]),
            "t5": WorkflowTask(task_id="t5", name="Final Code Synthesis", type="agent_task", assigned_agent="SynthesizerAgent", dependencies=["t4"]),
        }
        return wf

    @classmethod
    def get_template(cls, template_name: str, user_id: str, goal: str) -> Optional[WorkflowInstance]:
        """Factory method retrieving workflow template by name."""
        name_lower = template_name.lower().strip()
        if "coding" in name_lower:
            return cls.create_coding_project_template(user_id, goal)
        else:
            return cls.create_research_report_template(user_id, goal)


# Global WorkflowTemplates instance
workflow_templates = WorkflowTemplates()
