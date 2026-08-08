"""
REST API Router for Enterprise Long-Term Memory & Personalization Engine.

Provides CRUD endpoints for memory management and user profile retrieval.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Status
from pydantic import BaseModel, Field
from app.core.memory.memory_store import memory_store
from app.core.memory.memory_types import MemoryItem, MemoryType
from app.core.memory.profile_builder import profile_builder

router = APIRouter(prefix="", tags=["Memory"])


class MemoryCreateRequest(BaseModel):
    """Payload for creating a new memory item."""

    type: MemoryType = MemoryType.FACT
    title: str
    content: str
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    pinned: bool = False


class MemoryUpdateRequest(BaseModel):
    """Payload for updating an existing memory item."""

    title: Optional[str] = None
    content: Optional[str] = None
    importance_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    tags: Optional[List[str]] = None
    pinned: Optional[bool] = None


@router.get("/memory", response_model=Dict[str, Any])
async def list_memories(
    user_id: str = Query("default_user", description="User ID filter"),
    type: Optional[MemoryType] = Query(None, description="Memory type filter"),
    tag: Optional[str] = Query(None, description="Tag filter"),
):
    """Lists stored long-term memories for a user."""
    items = memory_store.list_memories(user_id=user_id, memory_type=type, tag=tag)
    return {
        "count": len(items),
        "memories": [item.model_dump() for item in items],
    }


@router.post("/memory", response_model=Dict[str, Any], status_code=Status.HTTP_201_CREATED)
async def create_memory(req: MemoryCreateRequest, user_id: str = "default_user"):
    """Creates a new long-term memory item explicitly."""
    item = MemoryItem(
        user_id=user_id,
        type=req.type,
        title=req.title,
        content=req.content,
        importance_score=req.importance_score,
        tags=req.tags,
        pinned=req.pinned,
    )
    saved = memory_store.add_memory(item)
    return {"status": "created", "memory": saved.model_dump()}


@router.patch("/memory/{memory_id}", response_model=Dict[str, Any])
async def update_memory(memory_id: str, req: MemoryUpdateRequest):
    """Updates an existing memory item by ID."""
    updates = {k: v for k, v in req.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided for update.")

    updated = memory_store.update_memory(memory_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Memory '{memory_id}' not found.")

    return {"status": "updated", "memory": updated.model_dump()}


@router.delete("/memory/{memory_id}", response_model=Dict[str, Any])
async def delete_memory(memory_id: str):
    """Deletes a long-term memory item by ID."""
    deleted = memory_store.delete_memory(memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Memory '{memory_id}' not found.")

    return {"status": "deleted", "id": memory_id}


@router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(user_id: str = Query("default_user", description="User ID")):
    """Retrieves synthesized dynamic user profile."""
    profile = profile_builder.build_user_profile(user_id=user_id)
    return {"profile": profile}
