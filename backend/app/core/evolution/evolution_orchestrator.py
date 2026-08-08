"""
Evolution Orchestrator for Enterprise Self-Optimization Platform.

Coordinates end-to-end self-evaluation, capability profiling, optimization planning,
adaptive tuning, performance learning, experimentation, and continuous evolution cycles.
"""

import time
from typing import Dict, Any
from app.core.logging import logger
from app.core.evolution.capability_analyzer import capability_analyzer
from app.core.evolution.self_evaluation import self_evaluation_engine
from app.core.evolution.optimization_engine import optimization_engine
from app.core.evolution.adaptive_tuner import adaptive_tuner
from app.core.evolution.performance_learning import performance_learning_engine
from app.core.evolution.recommendation_engine import improvement_recommendation_engine
from app.core.evolution.experiment_manager import experiment_manager
from app.core.evolution.evolution_store import evolution_store
from app.core.evolution.evolution_analytics import evolution_analytics_tracker
from app.core.evolution.evolution_models import EvolutionSnapshot


class EvolutionOrchestrator:
    """Central Orchestrator for Enterprise Self-Optimization Platform."""

    @staticmethod
    def execute_evolution_cycle(
        execution_context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Executes a complete evolution cycle:
        1. Capability analysis
        2. Self-evaluation
        3. Optimization planning
        4. Adaptive tuning
        5. Performance learning
        6. Recommendation generation
        7. Experiment creation
        8. Snapshot persistence
        9. Analytics update

        Args:
            execution_context: Optional runtime context for capability analysis.

        Returns:
            Dict containing all evolution cycle outputs.
        """
        start = time.time()
        logger.info("EvolutionOrchestrator starting evolution cycle...")

        # 1. Capability Analysis
        capability_profile = capability_analyzer.analyze_capabilities(
            execution_context=execution_context,
        )

        # 2. Self-Evaluation
        evaluation = self_evaluation_engine.evaluate()

        # 3. Optimization Planning
        opt_plan = optimization_engine.generate_optimization_plan(
            evaluation_composite_score=evaluation.composite_score,
        )

        # 4. Adaptive Tuning
        tuning_snapshot = adaptive_tuner.tune_parameters(
            performance_score=evaluation.composite_score,
        )

        # 5. Performance Learning
        learning_record = performance_learning_engine.extract_learning()

        # 6. Recommendation Generation
        recommendations = improvement_recommendation_engine.generate_recommendations()

        # 7. Experiment Creation (auto-create from top optimization)
        experiment = None
        if opt_plan.recommendations:
            top_rec = opt_plan.recommendations[0]
            experiment = experiment_manager.create_experiment(
                name=f"Auto: {top_rec.optimization_type}",
                hypothesis=f"Applying {top_rec.optimization_type} optimization to {top_rec.target_component} "
                           f"will improve performance by {top_rec.expected_improvement_pct}%",
                treatment_config={"optimization": top_rec.optimization_type, "value": str(top_rec.recommended_value)},
            )

        # 8. Snapshot Persistence
        snapshot = EvolutionSnapshot(
            capability_profile=capability_profile,
            evaluation_score=evaluation,
            active_experiments=(
                [experiment.experiment_id] if experiment else []
            ),
            optimization_plans_applied=len(opt_plan.recommendations),
            tuning_snapshots_count=len(adaptive_tuner.get_tuning_history()),
            learning_insights_count=len(learning_record.insights),
            recommendations_count=len(recommendations),
        )
        evolution_store.save_snapshot(snapshot)

        # 9. Analytics Update
        evolution_analytics_tracker.record_optimization(success=True)
        evolution_analytics_tracker.record_tuning_cycle()
        evolution_analytics_tracker.record_insights(len(learning_record.insights))
        evolution_analytics_tracker.record_capability_score(
            capability_profile.overall_score
        )
        for _ in recommendations:
            evolution_analytics_tracker.record_recommendation(implemented=False)

        analytics_summary = evolution_analytics_tracker.get_summary()

        elapsed = (time.time() - start) * 1000
        logger.info(
            f"EvolutionOrchestrator completed evolution cycle in {elapsed:.1f}ms: "
            f"Capability={capability_profile.overall_score}, "
            f"Evaluation={evaluation.composite_score}, "
            f"Optimizations={len(opt_plan.recommendations)}, "
            f"Insights={len(learning_record.insights)}, "
            f"Recommendations={len(recommendations)}"
        )

        return {
            "capability_profile": capability_profile.model_dump(),
            "self_evaluation": evaluation.model_dump(),
            "optimization_plan": opt_plan.model_dump(),
            "tuning_snapshot": tuning_snapshot.model_dump(),
            "learning_record": learning_record.model_dump(),
            "recommendations": [r.model_dump() for r in recommendations],
            "experiment": experiment.model_dump() if experiment else None,
            "evolution_snapshot": snapshot.model_dump(),
            "analytics_summary": analytics_summary.model_dump(),
            "cycle_duration_ms": round(elapsed, 2),
        }


# Global EvolutionOrchestrator instance
evolution_orchestrator = EvolutionOrchestrator()
