"""
Global Context Manager for Doxa AI Operating System.

Merges, deduplicates, ranks, clusters, compresses, and token-budgets information
from Conversation History, Hybrid RAG, Semantic Memory, Long-Term Memory, Episodic Memory,
User Preferences, Relationship Graphs, Workflow States, Planner Outputs, Reasoning Artifacts,
Evaluation Metadata, and Tool Outputs into one optimized Unified Global Context.
"""

import asyncio
import hashlib
import time
from typing import Dict, Any, List, Set, Optional
from app.core.logging import logger
from app.core.config import settings
from app.core.intelligence.intelligence_types import (
    ContextItem,
    UnifiedGlobalContext,
)


class GlobalContextManager:
    """Enterprise Global Context Manager."""

    # Default weights for context sources during prioritization
    _SOURCE_PRIORITIES: Dict[str, float] = {
        "preference": 1.0,
        "planner": 0.95,
        "reasoning": 0.90,
        "workflow": 0.88,
        "tool": 0.85,
        "rag": 0.82,
        "semantic_memory": 0.80,
        "episodic_memory": 0.75,
        "history": 0.70,
        "long_term_memory": 0.65,
        "knowledge_graph": 0.60,
        "eval": 0.50,
    }

    async def build_unified_context(
        self,
        history: Optional[List[Dict[str, Any]]] = None,
        rag_chunks: Optional[List[Dict[str, Any]]] = None,
        semantic_memories: Optional[List[Dict[str, Any]]] = None,
        long_term_memories: Optional[List[Dict[str, Any]]] = None,
        episodic_memories: Optional[List[Dict[str, Any]]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        knowledge_graph_triples: Optional[List[Any]] = None,
        workflow_state: Optional[Dict[str, Any]] = None,
        planner_output: Optional[Dict[str, Any]] = None,
        reasoning_artifacts: Optional[List[Dict[str, Any]]] = None,
        eval_metadata: Optional[Dict[str, Any]] = None,
        tool_outputs: Optional[List[Dict[str, Any]]] = None,
        max_token_budget: int = 4096,
    ) -> UnifiedGlobalContext:
        """
        Merges all contextual inputs into a deduplicated, ranked, and budgeted UnifiedGlobalContext.

        Args:
            history: Conversation history messages.
            rag_chunks: Retrieved RAG document snippets.
            semantic_memories: Key-value or concept memories.
            long_term_memories: Long-term facts or summary memories.
            episodic_memories: Event-based memories.
            preferences: User system preferences or customization settings.
            knowledge_graph_triples: Graph entity/relation triples.
            workflow_state: Current active workflow state.
            planner_output: Planner tasks or execution plan.
            reasoning_artifacts: CoT / ToT / GoT reasoning steps.
            eval_metadata: Safety, trust, or quality evaluation scores.
            tool_outputs: Output strings from executed tools.
            max_token_budget: Hard token limit for the unified context.

        Returns:
            UnifiedGlobalContext containing prioritized and budgeted ContextItems.
        """
        if not settings.GLOBAL_CONTEXT_MANAGER_ENABLED:
            return self._fallback_context(history, rag_chunks, max_token_budget)

        start_time = time.time()
        raw_items: List[ContextItem] = []

        # 1. Collect Context Items from All Sources
        # Preferences
        if preferences:
            pref_str = "\n".join([f"{k}: {v}" for k, v in preferences.items()])
            raw_items.append(ContextItem(
                source_type="preference",
                content=f"[USER PREFERENCES]\n{pref_str}",
                relevance_score=1.0,
            ))

        # Planner Output
        if planner_output:
            raw_items.append(ContextItem(
                source_type="planner",
                content=f"[EXECUTION PLAN]\n{str(planner_output)}",
                relevance_score=0.95,
            ))

        # Reasoning Artifacts
        if reasoning_artifacts:
            for artifact in reasoning_artifacts:
                raw_items.append(ContextItem(
                    source_type="reasoning",
                    content=f"[REASONING STEP]\n{str(artifact)}",
                    relevance_score=0.90,
                ))

        # Workflow State
        if workflow_state:
            raw_items.append(ContextItem(
                source_type="workflow",
                content=f"[WORKFLOW STATE]\n{str(workflow_state)}",
                relevance_score=0.88,
            ))

        # Tool Outputs
        if tool_outputs:
            for out in tool_outputs:
                raw_items.append(ContextItem(
                    source_type="tool",
                    content=f"[TOOL OUTPUT]\n{str(out)}",
                    relevance_score=0.85,
                ))

        # RAG Chunks
        if rag_chunks:
            for chunk in rag_chunks:
                text = chunk.get("text", "") or str(chunk)
                rel = float(chunk.get("similarity", 0.8))
                raw_items.append(ContextItem(
                    source_type="rag",
                    content=f"[KNOWLEDGE RETRIEVAL]\n{text}",
                    relevance_score=rel,
                    metadata=chunk.get("metadata", {}),
                ))

        # Semantic Memories
        if semantic_memories:
            for mem in semantic_memories:
                text = mem.get("content", "") or str(mem)
                raw_items.append(ContextItem(
                    source_type="semantic_memory",
                    content=f"[SEMANTIC MEMORY]\n{text}",
                    relevance_score=float(mem.get("relevance", 0.8)),
                ))

        # Episodic Memories
        if episodic_memories:
            for ep in episodic_memories:
                text = ep.get("summary", "") or str(ep)
                raw_items.append(ContextItem(
                    source_type="episodic_memory",
                    content=f"[EPISODIC MEMORY]\n{text}",
                    relevance_score=0.75,
                ))

        # Conversation History
        if history:
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                raw_items.append(ContextItem(
                    source_type="history",
                    content=f"[{role.upper()}]: {content}",
                    relevance_score=0.70,
                ))

        # Long-Term Memories
        if long_term_memories:
            for ltm in long_term_memories:
                text = ltm.get("fact", "") or str(ltm)
                raw_items.append(ContextItem(
                    source_type="long_term_memory",
                    content=f"[LONG-TERM FACT]\n{text}",
                    relevance_score=0.65,
                ))

        # Knowledge Graph Triples
        if knowledge_graph_triples:
            kg_str = "\n".join([str(t) for t in knowledge_graph_triples])
            raw_items.append(ContextItem(
                source_type="knowledge_graph",
                content=f"[KNOWLEDGE GRAPH TRIPLES]\n{kg_str}",
                relevance_score=0.60,
            ))

        # Evaluation Metadata
        if eval_metadata:
            raw_items.append(ContextItem(
                source_type="eval",
                content=f"[EVALUATION METADATA]\n{str(eval_metadata)}",
                relevance_score=0.50,
            ))

        # 2. Deduplication
        deduped_items, deduped_count = self._deduplicate_items(raw_items)

        # 3. Token Counting & Estimations
        for item in deduped_items:
            item.tokens_count = self._estimate_tokens(item.content)

        # 4. Semantic Clustering & Prioritized Ranking
        ranked_items = self._rank_and_cluster(deduped_items)

        # 5. Token Budgeting & Truncation
        final_items: List[ContextItem] = []
        accumulated_tokens = 0
        is_compressed = False

        for item in ranked_items:
            if accumulated_tokens + item.tokens_count <= max_token_budget:
                final_items.append(item)
                accumulated_tokens += item.tokens_count
            else:
                # Compress / truncate last fitting item if possible
                remaining_tokens = max_token_budget - accumulated_tokens
                if remaining_tokens > 50:
                    truncated_content = self._truncate_content(item.content, remaining_tokens)
                    item.content = truncated_content
                    item.tokens_count = remaining_tokens
                    final_items.append(item)
                    accumulated_tokens += remaining_tokens
                    is_compressed = True
                break

        compression_ratio = round(accumulated_tokens / max(sum(i.tokens_count for i in raw_items), 1), 2)

        unified_context = UnifiedGlobalContext(
            items=final_items,
            total_tokens=accumulated_tokens,
            max_token_budget=max_token_budget,
            deduplicated_count=deduped_count,
            clustered_group_count=len(final_items),
            compressed=is_compressed,
            compression_ratio=compression_ratio,
        )

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(
            f"GlobalContextManager generated context '{unified_context.context_id}': "
            f"Raw={len(raw_items)}, Final={len(final_items)}, Deduped={deduped_count}, "
            f"Tokens={accumulated_tokens}/{max_token_budget}, Elapsed={elapsed_ms:.2f}ms"
        )

        return unified_context

    def _deduplicate_items(self, items: List[ContextItem]) -> tuple[List[ContextItem], int]:
        """Removes duplicate or near-duplicate items based on content hashing."""
        seen_hashes: Set[str] = set()
        deduped: List[ContextItem] = []
        deduped_count = 0

        for item in items:
            normalized = "".join(item.content.lower().split())
            content_hash = hashlib.md5(normalized.encode("utf-8")).hexdigest()
            if content_hash in seen_hashes:
                deduped_count += 1
            else:
                seen_hashes.add(content_hash)
                deduped.append(item)

        return deduped, deduped_count

    def _rank_and_cluster(self, items: List[ContextItem]) -> List[ContextItem]:
        """Ranks items based on source priority, relevance score, and recency."""
        def calculate_rank(item: ContextItem) -> float:
            base_priority = self._SOURCE_PRIORITIES.get(item.source_type, 0.5)
            recency_weight = min(1.0, (item.recency_timestamp / time.time()))
            return (base_priority * 0.4) + (item.relevance_score * 0.4) + (recency_weight * 0.2)

        return sorted(items, key=calculate_rank, reverse=True)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimates token count (~4 characters per token)."""
        return max(1, len(text) // 4)

    @staticmethod
    def _truncate_content(text: str, max_tokens: int) -> str:
        """Truncates text to fit within maximum token allotment."""
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "... [truncated]"

    def _fallback_context(self, history: Optional[List[Dict[str, Any]]], rag_chunks: Optional[List[Dict[str, Any]]], max_budget: int) -> UnifiedGlobalContext:
        """Basic context builder fallback."""
        items: List[ContextItem] = []
        tokens = 0
        if history:
            for m in history:
                text = f"[{m.get('role', 'user')}]: {m.get('content', '')}"
                t_count = self._estimate_tokens(text)
                items.append(ContextItem(source_type="history", content=text, tokens_count=t_count))
                tokens += t_count
        return UnifiedGlobalContext(items=items, total_tokens=tokens, max_token_budget=max_budget)


# Global GlobalContextManager instance
global_context_manager = GlobalContextManager()
