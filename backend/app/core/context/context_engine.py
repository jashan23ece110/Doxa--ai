"""
Enterprise Context Engineering Pipeline Orchestrator.

Combines Token Budget Optimization, Context Deduplication, Noise Compression,
Structured Section Assembly, and Confidence Scoring into a production-grade prompt engine with graceful fallback.
"""

from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.context.compressor import context_compressor
from app.core.context.ranker import context_ranker
from app.core.context.token_budget import token_budget_manager
from app.core.context.validator import context_validator
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger
from app.core.security import PromptSanitizer


class ContextEngine:
    """Orchestrates enterprise context engineering and prompt section assembly."""

    @staticmethod
    def build_optimal_prompt(
        user_prompt: str,
        contexts: List[Dict[str, Any]],
        memory_context: str = "",
        system_instruction: str = "",
        tool_outputs: str = "",
    ) -> str:
        """
        Constructs an optimal, structured, token-budgeted prompt for the LLM.
        Applies context ranking, deduplication, compression, section budgets, and confidence scoring.
        """
        if not settings.CONTEXT_ENGINE_ENABLED:
            # Fallback to simple concatenation if ContextEngine is disabled
            return f"{memory_context}\n\n{user_prompt}".strip()

        try:
            with DiagnosticSpan(span_name="context_engine_assembly", slow_threshold_ms=50.0, category="general"):
                sections = []

                # 1. System Instructions Section
                if system_instruction:
                    sys_trimmed = token_budget_manager.trim_text_to_token_budget(
                        system_instruction, settings.MAX_CONTEXT_TOKENS // 8
                    )
                    sections.append(f"=== SYSTEM INSTRUCTIONS ===\n{sys_trimmed}")

                # 2. User Memory Context Section
                if memory_context and settings.MEMORY_ENABLED:
                    mem_compressed = context_compressor.compress_text(memory_context)
                    mem_trimmed = token_budget_manager.trim_text_to_token_budget(
                        mem_compressed, settings.MAX_MEMORY_TOKENS
                    )
                    if mem_trimmed:
                        sections.append(mem_trimmed)

                # 3. Retrieved Knowledge Evidence Section (RAG)
                if contexts:
                    unique_contexts = context_ranker.deduplicate_and_group(contexts)
                    evidence_blocks = []

                    for ctx in unique_contexts:
                        clean_text = PromptSanitizer.sanitize_context_block(ctx["text"])
                        if settings.ENABLE_CONTEXT_COMPRESSION:
                            clean_text = context_compressor.compress_text(clean_text)

                        source_info = f"[Source: {ctx.get('filename', 'Doc')} | Chunk {ctx.get('chunk_index', 0)}]"
                        evidence_blocks.append(f"{source_info}\n{clean_text}")

                    joined_evidence = "\n\n---\n\n".join(evidence_blocks)
                    evidence_trimmed = token_budget_manager.trim_text_to_token_budget(
                        joined_evidence, settings.MAX_RETRIEVAL_TOKENS
                    )
                    if evidence_trimmed:
                        sections.append(
                            f"=== RETRIEVED KNOWLEDGE EVIDENCE ===\n\n{evidence_trimmed}\n\n=== END KNOWLEDGE EVIDENCE ==="
                        )

                # 4. Tool Outputs Section
                if tool_outputs:
                    tool_trimmed = token_budget_manager.trim_text_to_token_budget(
                        tool_outputs, settings.MAX_TOOL_TOKENS
                    )
                    if tool_trimmed:
                        sections.append(f"=== TOOL OUTPUT EVIDENCE ===\n{tool_trimmed}")

                # 5. User Question Section
                clean_user_prompt = PromptSanitizer.sanitize_user_input(user_prompt)
                sections.append(f"=== USER QUESTION ===\n{clean_user_prompt}")

                # Calculate overall confidence score for observability
                confidence_score = context_validator.calculate_confidence_score(contexts, memory_context)
                logger.debug(f"Assembled context engine prompt ({len(sections)} sections, Confidence Score: {confidence_score:.2f})")

                return "\n\n".join(sections)

        except Exception as e:
            logger.warning(f"ContextEngine prompt assembly failed ({e}). Falling back to standard prompt template.")
            # Graceful Fallback
            return f"{memory_context}\n\nUser's Question: {user_prompt}".strip()


# Global ContextEngine instance
context_engine = ContextEngine()
