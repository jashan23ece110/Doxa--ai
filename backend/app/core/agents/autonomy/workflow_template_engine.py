"""
Reusable Workflow Template Engine.

Creates, versions, and instantiates reusable workflow templates from validated task graphs.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.autonomy.agent_memory_types import WorkflowTemplate


class WorkflowTemplateEngine:
    """Thread-safe Reusable Workflow Template Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._templates: Dict[str, WorkflowTemplate] = {}

    def create_template(self, name: str, steps: List[str], roles: List[str]) -> WorkflowTemplate:
        """
        Registers a new reusable workflow template.

        Args:
            name: Template name string.
            steps: List of step names.
            roles: List of required agent roles.

        Returns:
            WorkflowTemplate object.
        """
        tmpl = WorkflowTemplate(name=name, steps=steps, agent_roles_required=roles)
        with self._lock:
            self._templates[tmpl.template_id] = tmpl
            security_logger.info(f"WorkflowTemplateEngine: Created template '{name}' ({tmpl.template_id}) with {len(steps)} steps.")
        return tmpl

    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Retrieves template by ID."""
        with self._lock:
            return self._templates.get(template_id)


# Global WorkflowTemplateEngine instance
workflow_template_engine = WorkflowTemplateEngine()
