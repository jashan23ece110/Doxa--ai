"""Evaluation package initialization."""
from app.core.eval.ir_metrics import ir_metrics_calculator, IRMetricsCalculator
from app.core.eval.quality_engine import quality_engine, QualityEngine
from app.core.eval.eval_storage import eval_storage, EvaluationStorage
from app.core.eval.eval_platform import eval_platform, EvalPlatform

__all__ = [
    "ir_metrics_calculator",
    "IRMetricsCalculator",
    "quality_engine",
    "QualityEngine",
    "eval_storage",
    "EvaluationStorage",
    "eval_platform",
    "EvalPlatform",
]
