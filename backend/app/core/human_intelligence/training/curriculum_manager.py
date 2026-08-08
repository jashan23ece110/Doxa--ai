"""
Enterprise Curriculum Manager.

Manages learning modules, course versioning, role-based curricula,
certification pathways, prerequisite dependencies, and content lifecycles.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class CurriculumCourse(BaseModel):
    course_id: str
    title: str
    version: str = "1.0.0"
    target_role: str = "All"
    module_ids: List[str] = Field(default_factory=list)


class CurriculumManager:
    """Enterprise Curriculum Manager."""

    def __init__(self):
        self._courses: Dict[str, CurriculumCourse] = {
            "course_base_01": CurriculumCourse(
                course_id="course_base_01",
                title="Enterprise Cybersecurity Foundations & Awareness",
                version="1.2.0",
                target_role="All",
                module_ids=["mod_phish_01", "mod_cred_01"],
            )
        }

    def get_curriculum_for_role(self, role: str = "All") -> List[CurriculumCourse]:
        """Retrieves active curriculum courses matching a target role."""
        courses = [c for c in self._courses.values() if c.target_role in (role, "All")]
        security_logger.info(f"CurriculumManager: Retrieved {len(courses)} curriculum courses for role '{role}'.")
        return courses


# Global CurriculumManager instance
curriculum_manager = CurriculumManager()
