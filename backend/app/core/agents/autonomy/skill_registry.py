"""
Enterprise Agent Skill Registry.

Registers and catalogues versioned reusable skills across research, coding, deployment, and testing.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.agents.autonomy.agent_memory_types import LearnedSkill


class SkillRegistry:
    """Thread-safe Enterprise Agent Skill Registry."""

    def __init__(self):
        self._lock = threading.Lock()
        self._skills: Dict[str, LearnedSkill] = {}
        self._seed_default_skills()

    def _seed_default_skills(self) -> None:
        defaults = [
            LearnedSkill(name="CodeGeneration", category="CODING", required_capability="code_generation", description="Automated patch creation"),
            LearnedSkill(name="EvidenceRetrieval", category="RESEARCH", required_capability="evidence_retrieval", description="Semantic research retrieval"),
            LearnedSkill(name="CanaryDeployment", category="DEVOPS", required_capability="deployment_planning", description="Staged canary deployment"),
        ]
        for sk in defaults:
            self._skills[sk.skill_id] = sk

    def register_skill(self, name: str, category: str, required_capability: str, description: str) -> LearnedSkill:
        """Registers a new reusable skill."""
        sk = LearnedSkill(name=name, category=category, required_capability=required_capability, description=description)
        with self._lock:
            self._skills[sk.skill_id] = sk
            security_logger.info(f"SkillRegistry: Registered skill '{name}' ({sk.skill_id}) under category '{category}'.")
        return sk

    def find_skills_by_category(self, category: str) -> List[LearnedSkill]:
        """Discovers registered skills matching target category."""
        with self._lock:
            return [s for s in self._skills.values() if s.category.upper() == category.upper()]


# Global SkillRegistry instance
skill_registry = SkillRegistry()
