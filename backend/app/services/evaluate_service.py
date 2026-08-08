"""
Evaluate Service for Dual-Model Benchmark Comparisons with Reasoning Engine Post-Processing.

Handles concurrent LLM completion invocations across model variants and applies internal reasoning verification.
"""

import asyncio
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger
from app.core.reasoning.reasoning_engine import reasoning_engine
from app.services.llm_service import llm_service


class EvaluateService:
    """Service handling multi-model prompt evaluation and response verification."""

    @staticmethod
    async def call_single_model(
        model_name: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        contexts: Optional[List[Dict[str, Any]]] = None,
        memory_context: str = "",
    ) -> Dict[str, Any]:
        """Calls an LLM model and applies internal ReasoningEngine verification."""
        try:
            raw_response = await llm_service.call_tokenrouter(
                prompt=prompt,
                model=model_name,
                system_prompt=system_prompt,
            )

            # Internal Reasoning Verification & Reflection Pass
            verified_response = reasoning_engine.process_and_verify_response(
                draft_response=raw_response,
                query=prompt,
                contexts=contexts or [],
                memory_context=memory_context,
            )

            return {
                "model": model_name,
                "response": verified_response,
                "error": None,
            }
        except Exception as e:
            logger.error(f"Evaluation call failed for model {model_name}: {e}")
            return {
                "model": model_name,
                "response": f"Evaluation error: {str(e)}",
                "error": str(e),
            }

    async def evaluate_models(
        self,
        prompt: str,
        model1: str = settings.DEFAULT_EVAL_MODEL_1,
        model2: str = settings.DEFAULT_EVAL_MODEL_2,
        system_prompt: Optional[str] = None,
        contexts: Optional[List[Dict[str, Any]]] = None,
        memory_context: str = "",
    ) -> Dict[str, Any]:
        """Executes concurrent dual-model evaluations."""
        logger.info(f"Evaluating models '{model1}' vs '{model2}' for prompt '{prompt[:30]}...'")

        task1 = self.call_single_model(model1, prompt, system_prompt, contexts, memory_context)
        task2 = self.call_single_model(model2, prompt, system_prompt, contexts, memory_context)

        res1, res2 = await asyncio.gather(task1, task2)

        return {
            "prompt": prompt,
            "results": {
                model1: res1["response"],
                model2: res2["response"],
            },
            "errors": {
                model1: res1["error"],
                model2: res2["error"],
            },
        }


evaluate_service = EvaluateService()
