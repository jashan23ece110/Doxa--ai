"""
Repository & Storage Layer for Enterprise Long-Term Memory Engine.

Supports thread-safe JSON file storage (memory_store.json) with pluggable repository architecture.
"""

import json
import os
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.memory.memory_types import MemoryItem, MemoryType


class IMemoryStore(ABC):
    """Abstract interface for memory persistence storage."""

    @abstractmethod
    def add_memory(self, memory: MemoryItem) -> MemoryItem:
        pass

    @abstractmethod
    def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> Optional[MemoryItem]:
        pass

    @abstractmethod
    def delete_memory(self, memory_id: str) -> bool:
        pass

    @abstractmethod
    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        pass

    @abstractmethod
    def list_memories(
        self,
        user_id: str = "default_user",
        memory_type: Optional[MemoryType] = None,
        tag: Optional[str] = None,
    ) -> List[MemoryItem]:
        pass


class JSONMemoryStore(IMemoryStore):
    """Thread-safe JSON file implementation of IMemoryStore."""

    def __init__(self, store_path: Optional[str] = None):
        self.store_path = store_path or settings.MEMORY_STORE_PATH
        self._lock = threading.Lock()
        self.memories: Dict[str, MemoryItem] = {}
        self._load_from_disk()

    def _save_to_disk(self) -> None:
        """Persists memory records to JSON file."""
        if not self.store_path:
            return
        try:
            parent_dir = Path(self.store_path).parent
            parent_dir.mkdir(parents=True, exist_ok=True)
            serializable_dict = {
                m_id: m.model_dump() for m_id, m in self.memories.items()
            }
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(serializable_dict, f, ensure_ascii=False, indent=2)
            logger.debug(f"Persisted {len(self.memories)} long-term memories to disk.")
        except Exception as e:
            logger.error(f"Failed to persist long-term memories to disk: {e}")

    def _load_from_disk(self) -> None:
        """Loads memory records from JSON file with legacy schema adapter."""
        if not self.store_path or not os.path.exists(self.store_path):
            return
        try:
            with open(self.store_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for m_id, m_dict in data.items():
                    # Legacy schema adaptation
                    if "title" not in m_dict:
                        m_dict["title"] = m_dict.get("key", "Memory Item")
                    if "content" not in m_dict:
                        m_dict["content"] = str(m_dict.get("value", m_dict.get("key", "")))
                    if "type" not in m_dict or m_dict["type"] not in MemoryType.__members__.values():
                        m_dict["type"] = MemoryType.FACT.value
                    if "id" not in m_dict:
                        m_dict["id"] = m_id
                    
                    self.memories[m_id] = MemoryItem(**m_dict)
            logger.info(f"Loaded {len(self.memories)} long-term memories from disk.")
        except Exception as e:
            logger.warning(f"Failed to load long-term memories from disk: {e}")

    def add_memory(self, memory: MemoryItem) -> MemoryItem:
        with self._lock:
            self.memories[memory.id] = memory
            self._save_to_disk()
            return memory

    def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> Optional[MemoryItem]:
        with self._lock:
            if memory_id not in self.memories:
                return None
            item = self.memories[memory_id]
            updated_dict = item.model_dump()
            updated_dict.update(updates)
            updated_dict["updated_at"] = time.time()
            new_item = MemoryItem(**updated_dict)
            self.memories[memory_id] = new_item
            self._save_to_disk()
            return new_item

    def delete_memory(self, memory_id: str) -> bool:
        with self._lock:
            if memory_id in self.memories:
                del self.memories[memory_id]
                self._save_to_disk()
                return True
            return False

    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        with self._lock:
            return self.memories.get(memory_id)

    def list_memories(
        self,
        user_id: str = "default_user",
        memory_type: Optional[MemoryType] = None,
        tag: Optional[str] = None,
    ) -> List[MemoryItem]:
        with self._lock:
            res = []
            for item in self.memories.values():
                if item.user_id != user_id:
                    continue
                if memory_type and item.type != memory_type:
                    continue
                if tag and tag not in item.tags:
                    continue
                res.append(item)
            return res


# Global JSONMemoryStore instance
memory_store = JSONMemoryStore()
