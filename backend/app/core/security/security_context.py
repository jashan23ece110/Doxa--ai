"""
Unified Security Context for Enterprise Cybersecurity & Reverse Engineering Platform.

Merges uploaded binaries, memory, RAG, previous analyses, IOC history, threat intelligence,
user session, and forensic artifacts into one deduplicated, ranked, compressed, and budgeted context.
"""

import hashlib
import time
from typing import Dict, Any, List, Set, Optional
from app.core.logging import security_logger
from app.core.security.security_types import (
    BinaryMetadata,
    IOC,
    ThreatReport,
    ForensicArtifact,
    SecurityFinding,
)


class UnifiedSecurityContext:
    """Enterprise Unified Security Context for security research analysis."""

    async def build_context(
        self,
        binary_metadata: Optional[BinaryMetadata] = None,
        previous_reports: Optional[List[ThreatReport]] = None,
        iocs: Optional[List[IOC]] = None,
        forensic_artifacts: Optional[List[ForensicArtifact]] = None,
        findings: Optional[List[SecurityFinding]] = None,
        rag_snippets: Optional[List[Dict[str, Any]]] = None,
        max_token_budget: int = 4096,
    ) -> Dict[str, Any]:
        """
        Merges, deduplicates, ranks, and token-budgets security research context.

        Returns:
            Dict containing unified items, token count, and metadata summary.
        """
        raw_items: List[Dict[str, Any]] = []

        if binary_metadata:
            raw_items.append({
                "category": "binary_metadata",
                "priority": 1.0,
                "content": f"[BINARY METADATA]\nFile: {binary_metadata.file_name}, Arch: {binary_metadata.architecture.value}, Format: {binary_metadata.format.value}, Packed: {binary_metadata.is_packed}",
            })

        if iocs:
            for ioc in iocs:
                raw_items.append({
                    "category": "ioc",
                    "priority": 0.9,
                    "content": f"[IOC MATCH]\nType: {ioc.ioc_type}, Value: {ioc.value}, Severity: {ioc.severity.value}",
                })

        if findings:
            for find in findings:
                raw_items.append({
                    "category": "finding",
                    "priority": 0.85,
                    "content": f"[SECURITY FINDING]\nTitle: {find.title}, Category: {find.category}, Severity: {find.severity.value}",
                })

        if forensic_artifacts:
            for art in forensic_artifacts:
                raw_items.append({
                    "category": "forensic",
                    "priority": 0.8,
                    "content": f"[FORENSIC ARTIFACT]\nType: {art.artifact_type}, Source: {art.source}, Checksum: {art.checksum}",
                })

        if rag_snippets:
            for rag in rag_snippets:
                text = rag.get("text", str(rag))
                raw_items.append({
                    "category": "rag",
                    "priority": 0.75,
                    "content": f"[SECURITY INTEL KNOWLEDGE]\n{text}",
                })

        if previous_reports:
            for rep in previous_reports:
                raw_items.append({
                    "category": "history_report",
                    "priority": 0.7,
                    "content": f"[PREVIOUS REPORT]\nTitle: {rep.title}, Summary: {rep.summary[:200]}",
                })

        # Deduplicate
        deduped, deduped_count = self._deduplicate(raw_items)

        # Rank
        ranked = sorted(deduped, key=lambda x: x["priority"], reverse=True)

        # Token budget
        final_items = []
        accumulated_tokens = 0

        for item in ranked:
            item_tokens = len(item["content"]) // 4
            if accumulated_tokens + item_tokens <= max_token_budget:
                final_items.append(item)
                accumulated_tokens += item_tokens
            else:
                break

        security_logger.info(
            f"UnifiedSecurityContext: Merged {len(raw_items)} items -> {len(final_items)} budgeted items ({accumulated_tokens}/{max_token_budget} tokens)."
        )

        return {
            "items": final_items,
            "total_tokens": accumulated_tokens,
            "max_budget": max_token_budget,
            "deduplicated_count": deduped_count,
        }

    def _deduplicate(self, items: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], int]:
        seen = set()
        deduped = []
        count = 0
        for item in items:
            h = hashlib.md5(item["content"].lower().strip().encode("utf-8")).hexdigest()
            if h in seen:
                count += 1
            else:
                seen.add(h)
                deduped.append(item)
        return deduped, count


# Global UnifiedSecurityContext instance
unified_security_context = UnifiedSecurityContext()
