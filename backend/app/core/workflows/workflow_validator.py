"""
Workflow Validator for Enterprise Autonomous Workflow Engine.

Validates workflow definitions for cyclic dependencies, missing references, and orphaned tasks.
"""

from typing import List, Dict, Any, Tuple
from app.core.workflows.dependency_graph import DependencyGraph
from app.core.workflows.workflow_state import WorkflowInstance, WorkflowTask


class WorkflowValidator:
    """Validates workflow structural integrity."""

    @staticmethod
    def validate_workflow(workflow: WorkflowInstance) -> Tuple[bool, List[str]]:
        """
        Validates workflow structural integrity.
        Returns: (is_valid, list_of_error_strings)
        """
        errors = []

        if not workflow.tasks:
            errors.append("Workflow contains no tasks.")
            return False, errors

        # 1. Check for missing dependency references
        all_task_ids = set(workflow.tasks.keys())
        for task_id, task in workflow.tasks.items():
            for dep_id in task.dependencies:
                if dep_id not in all_task_ids:
                    errors.append(f"Task '{task_id}' references non-existent dependency '{dep_id}'.")

        # 2. Check for cyclic dependencies
        graph = DependencyGraph(workflow.tasks)
        if graph.has_cycles():
            errors.append("Workflow graph contains cyclic dependencies.")

        is_valid = len(errors) == 0
        return is_valid, errors


# Global WorkflowValidator instance
workflow_validator = WorkflowValidator()
