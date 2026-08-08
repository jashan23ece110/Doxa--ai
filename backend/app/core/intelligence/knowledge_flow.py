"""
Knowledge Flow Engine for Doxa AI Operating System.

Automatically propagates knowledge across Retrieval -> Reasoning -> Memory -> Knowledge Graph -> Evaluation -> Future Retrieval
without redundant or duplicate processing.
"""

import hashlib
import time
from typing import Dict, Any, List, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import (
    KnowledgeFlowRecord,
    KnowledgeFlowStep,
)


class KnowledgeFlowEngine:
    """Enterprise Knowledge Flow Engine for seamless knowledge propagation."""

    def __init__(self):
        self._active_flows: Dict[str, KnowledgeFlowRecord] = {}

    def init_flow(self, request_id: str) -> KnowledgeFlowRecord:
        """Initializes a new knowledge flow tracking record."""
        flow = KnowledgeFlowRecord(request_id=request_id)
        self._active_flows[request_id] = flow
        return flow

    async def propagate(
        self,
        flow: KnowledgeFlowRecord,
        from_subsystem: str,
        to_subsystem: str,
        payload: Any,
    ) -> bool:
        """
        Propagates knowledge between two subsystems cleanly without duplicate processing.

        Args:
            flow: Active KnowledgeFlowRecord.
            from_subsystem: Source subsystem ('retrieval', 'reasoning', 'memory', 'knowledge_graph', 'eval', 'future_retrieval').
            to_subsystem: Destination subsystem.
            payload: Data object or summary being transferred.

        Returns:
            True if propagation succeeded, False if skipped due to duplication.
        """
        if not settings.KNOWLEDGE_FLOW_ENABLED:
            return True

        # Generate payload hash to prevent duplicate transfers
        payload_str = str(payload)
        data_hash = hashlib.md5(payload_str.encode("utf-8")).hexdigest()

        # Check for duplicate step in current flow
        for step in flow.steps:
            if step.from_subsystem == from_subsystem and step.to_subsystem == to_subsystem and step.data_hash == data_hash:
                flow.deduplicated_transfers += 1
                logger.debug(
                    f"KnowledgeFlowEngine: Skipped duplicate transfer {from_subsystem} -> {to_subsystem} "
                    f"(hash={data_hash[:8]})"
                )
                return False

        # Add step to flow
        summary = payload_str[:150] + ("..." if len(payload_str) > 150 else "")
        flow_step = KnowledgeFlowStep(
            from_subsystem=from_subsystem,
            to_subsystem=to_subsystem,
            payload_summary=summary,
            data_hash=data_hash,
            timestamp=time.time(),
        )

        flow.steps.append(flow_step)
        logger.info(
            f"KnowledgeFlowEngine: Propagated {from_subsystem} -> {to_subsystem} "
            f"[Flow={flow.flow_id}, Step={len(flow.steps)}]"
        )

        return True

    def finalize_flow(self, flow: KnowledgeFlowRecord):
        """Finalizes the knowledge flow lifecycle."""
        self._active_flows.pop(flow.request_id, None)
        logger.info(
            f"KnowledgeFlowEngine finalized '{flow.flow_id}': "
            f"Steps={len(flow.steps)}, Deduplicated={flow.deduplicated_transfers}"
        )


# Global KnowledgeFlowEngine instance
knowledge_flow_engine = KnowledgeFlowEngine()
