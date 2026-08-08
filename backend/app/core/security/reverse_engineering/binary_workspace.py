"""
Reverse Engineering Workspace.

Manages projects, binary versions, analyst notes, bookmarks, recovered symbols,
renamed functions, comments, and analysis history.
"""

import threading
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger


class AnalystNote(BaseModel):
    note_id: str
    author: str = "analyst"
    address: Optional[int] = None
    content: str
    created_at: float = Field(default_factory=time.time)


class REProject(BaseModel):
    project_id: str
    name: str
    binary_id: str
    renamed_functions: Dict[str, str] = Field(default_factory=dict)  # old_name -> new_name
    bookmarks: List[int] = Field(default_factory=list)
    notes: List[AnalystNote] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


class BinaryWorkspace:
    """Thread-safe Reverse Engineering Workspace Manager."""

    def __init__(self):
        self._lock = threading.Lock()
        self._projects: Dict[str, REProject] = {}

    def create_project(self, project_id: str, name: str, binary_id: str) -> REProject:
        """Creates a new reverse engineering project."""
        proj = REProject(project_id=project_id, name=name, binary_id=binary_id)
        with self._lock:
            self._projects[project_id] = proj
            security_logger.info(f"BinaryWorkspace: Created project '{name}' ({project_id}).")
        return proj

    def rename_function(self, project_id: str, old_name: str, new_name: str) -> bool:
        """Renames a function in the project workspace."""
        with self._lock:
            proj = self._projects.get(project_id)
            if proj:
                proj.renamed_functions[old_name] = new_name
                security_logger.info(f"BinaryWorkspace: Renamed function '{old_name}' -> '{new_name}' in project '{project_id}'.")
                return True
        return False

    def add_note(self, project_id: str, content: str, address: Optional[int] = None, author: str = "analyst") -> Optional[AnalystNote]:
        """Adds an analyst note or comment."""
        with self._lock:
            proj = self._projects.get(project_id)
            if proj:
                note_id = f"note_{len(proj.notes) + 1}"
                note = AnalystNote(note_id=note_id, author=author, address=address, content=content)
                proj.notes.append(note)
                return note
        return None

    def get_project(self, project_id: str) -> Optional[REProject]:
        """Retrieves project details."""
        with self._lock:
            return self._projects.get(project_id)


# Global BinaryWorkspace instance
binary_workspace = BinaryWorkspace()
