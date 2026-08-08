#!/usr/bin/env python3
"""
Integration test for Enterprise Self-Optimization Platform (Stage 5, Part 5).

Validates all evolution components: capability analysis, self-evaluation,
optimization planning, adaptive tuning, performance learning, recommendations,
experimentation, evolution store, analytics, and the orchestrator.
"""

import sys
import os
import json
import shutil

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PASS = 0
FAIL = 0


def check(label, condition):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def test_evolution_models():
    print("\n🔬 Testing Evolution Models...")
    from app.core.evolution.evolution_models import (
        CapabilityDimension, CapabilityScore, CapabilityProfile,
        EvaluationMetric, SelfEvaluationScore,
        OptimizationRecommendation, OptimizationPlan,
        TuningParameter, TuningSnapshot,
        LearningInsight, PerformanceLearningRecord,
        RecommendationCategory, SystemRecommendation,
        ExperimentVariant, ABExperiment,
        EvolutionSnapshot, EvolutionAnalyticsSummary,
    )

    # CapabilityDimension enum
    check("CapabilityDimension has 10 members", len(CapabilityDimension) == 10)
    check("REASONING in dimensions", CapabilityDimension.REASONING.value == "reasoning")

    # CapabilityProfile
    profile = CapabilityProfile()
    check("CapabilityProfile has profile_id", profile.profile_id.startswith("cap_"))
    check("CapabilityProfile default maturity", profile.maturity_level == "DEVELOPING")

    # SelfEvaluationScore
    score = SelfEvaluationScore()
    check("SelfEvaluationScore has evaluation_id", score.evaluation_id.startswith("eval_"))

    # OptimizationPlan
    plan = OptimizationPlan()
    check("OptimizationPlan has plan_id", plan.plan_id.startswith("plan_"))
    check("OptimizationPlan default risk LOW", plan.risk_level == "LOW")

    # TuningSnapshot
    snap = TuningSnapshot()
    check("TuningSnapshot has snapshot_id", snap.snapshot_id.startswith("tune_"))

    # ABExperiment
    exp = ABExperiment(name="test", hypothesis="test hypothesis")
    check("ABExperiment has experiment_id", exp.experiment_id.startswith("exp_"))
    check("ABExperiment default DRAFT", exp.status == "DRAFT")

    # RecommendationCategory enum
    check("RecommendationCategory has 6 members", len(RecommendationCategory) == 6)

    # EvolutionSnapshot
    es = EvolutionSnapshot()
    check("EvolutionSnapshot has snapshot_id", es.snapshot_id.startswith("snap_"))

    # Serialization roundtrip
    data = profile.model_dump()
    restored = CapabilityProfile.model_validate(data)
    check("CapabilityProfile roundtrip serialization", restored.profile_id == profile.profile_id)


def test_capability_analyzer():
    print("\n🧠 Testing Capability Analyzer...")
    from app.core.evolution.capability_analyzer import capability_analyzer

    profile = capability_analyzer.analyze_capabilities()
    check("Profile has 10 dimension scores", len(profile.scores) == 10)
    check("Overall score > 0", profile.overall_score > 0)
    check("Overall score <= 1", profile.overall_score <= 1.0)
    check("IQ metric > 0", profile.intelligence_quotient > 0)
    check("Maturity is ADVANCED", profile.maturity_level == "ADVANCED")
    check("Assessment duration >= 0", profile.assessment_duration_ms >= 0)

    # Context-driven adjustment
    context_profile = capability_analyzer.analyze_capabilities(
        execution_context={"reasoning_adjustment": 0.05}
    )
    reasoning_score = next(s for s in context_profile.scores if s.dimension.value == "reasoning")
    check("Context adjustment applied", reasoning_score.score == 0.97)
    check("Context trend IMPROVING", reasoning_score.trend == "IMPROVING")


def test_self_evaluation():
    print("\n📊 Testing Self-Evaluation Engine...")
    from app.core.evolution.self_evaluation import self_evaluation_engine

    result = self_evaluation_engine.evaluate()
    check("Evaluation has 6 metrics", len(result.metrics) == 6)
    check("Composite score > 0", result.composite_score > 0)
    check("Accuracy score > 0.9", result.accuracy_score > 0.9)
    check("All defaults pass", all(m.passed for m in result.metrics))
    check("No recommendations for passing metrics", len(result.recommendations) == 0)

    # Test with failing metrics
    failing_result = self_evaluation_engine.evaluate(
        observed_metrics={"accuracy": 0.50, "goal_completion": 0.40}
    )
    check("Failing metrics produce recommendations", len(failing_result.recommendations) >= 2)


def test_optimization_engine():
    print("\n⚡ Testing Optimization Engine...")
    from app.core.evolution.optimization_engine import optimization_engine

    plan = optimization_engine.generate_optimization_plan()
    check("Plan has recommendations", len(plan.recommendations) > 0)
    check("Plan has plan_id", plan.plan_id.startswith("plan_"))
    check("Estimated improvement > 0", plan.estimated_total_improvement_pct > 0)
    check("Risk level is valid", plan.risk_level in ["LOW", "MEDIUM", "HIGH"])
    check("Recommendations sorted by improvement", 
          plan.recommendations[0].expected_improvement_pct >= plan.recommendations[-1].expected_improvement_pct)


def test_adaptive_tuner():
    print("\n🎛️ Testing Adaptive Tuner...")
    from app.core.evolution.adaptive_tuner import AdaptiveTuner

    tuner = AdaptiveTuner()
    params_before = tuner.get_current_parameters()
    check("8 default parameters", len(params_before) == 8)

    snapshot = tuner.tune_parameters(performance_score=0.85)
    check("Snapshot has snapshot_id", snapshot.snapshot_id.startswith("tune_"))
    check("Performance improved", snapshot.performance_after >= snapshot.performance_before)
    check("8 tuned parameters", len(snapshot.parameters) == 8)

    history = tuner.get_tuning_history()
    check("History has 1 entry", len(history) == 1)


def test_performance_learning():
    print("\n📚 Testing Performance Learning Engine...")
    from app.core.evolution.performance_learning import PerformanceLearningEngine

    engine = PerformanceLearningEngine()
    record = engine.extract_learning(execution_logs_count=500, benchmarks_count=25)
    check("Record has insights", len(record.insights) > 0)
    check("Record has record_id", record.record_id.startswith("plr_"))
    check("Logs count recorded", record.execution_logs_analyzed == 500)

    all_insights = engine.get_all_insights()
    check("All insights retrievable", len(all_insights) == len(record.insights))

    throughput = engine.get_insights_by_category("throughput")
    check("Category filter works", len(throughput) > 0)
    check("All filtered are throughput", all(i.category == "throughput" for i in throughput))


def test_recommendation_engine():
    print("\n💡 Testing Recommendation Engine...")
    from app.core.evolution.recommendation_engine import ImprovementRecommendationEngine
    from app.core.evolution.evolution_models import RecommendationCategory

    engine = ImprovementRecommendationEngine()
    recs = engine.generate_recommendations()
    check("Recommendations generated", len(recs) > 0)
    check("Priority ranks assigned", recs[0].priority_rank == 1)
    check("Sorted by ROI", all(r.priority_rank <= r2.priority_rank for r, r2 in zip(recs, recs[1:])))

    # Focus filter
    perf_recs = engine.generate_recommendations(
        focus_categories=[RecommendationCategory.PERFORMANCE]
    )
    check("Category filter works", all(r.category == RecommendationCategory.PERFORMANCE for r in perf_recs))

    # Status update
    rid = recs[0].recommendation_id
    ok = engine.mark_recommendation_status(rid, "ACCEPTED")
    check("Status update succeeds", ok)


def test_experiment_manager():
    print("\n🧪 Testing Experiment Manager...")
    from app.core.evolution.experiment_manager import ExperimentManager

    mgr = ExperimentManager()

    # Create experiment
    exp = mgr.create_experiment(
        name="Cache TTL Test",
        hypothesis="Increasing cache TTL to 600s improves hit rate",
        treatment_config={"cache_ttl": 600},
    )
    check("Experiment created", exp.experiment_id.startswith("exp_"))
    check("Status is DRAFT", exp.status == "DRAFT")
    check("Has 2 variants", len(exp.variants) == 2)

    # Start experiment
    started = mgr.start_experiment(exp.experiment_id)
    check("Experiment started", started is not None)
    check("Status is RUNNING", started.status == "RUNNING")

    # Record results
    for _ in range(10):
        mgr.record_variant_result(exp.experiment_id, "control", True, 100.0)
        mgr.record_variant_result(exp.experiment_id, "treatment", True, 80.0)

    # Evaluate
    result = mgr.evaluate_experiment(exp.experiment_id)
    check("Experiment completed", result.status == "COMPLETED")
    check("Winner determined", result.winner_variant_id is not None)

    # Test rollback
    exp2 = mgr.create_experiment(
        name="Rollback Test",
        hypothesis="This should roll back",
        rollback_threshold=0.05,
    )
    mgr.start_experiment(exp2.experiment_id)
    for _ in range(10):
        mgr.record_variant_result(exp2.experiment_id, "control", True, 100.0)
        mgr.record_variant_result(exp2.experiment_id, "treatment", False, 200.0)
    rolled = mgr.evaluate_experiment(exp2.experiment_id)
    check("Auto-rollback triggered", rolled.status == "ROLLED_BACK")


def test_evolution_store():
    print("\n💾 Testing Evolution Store...")
    from app.core.evolution.evolution_store import EvolutionStore
    from app.core.evolution.evolution_models import EvolutionSnapshot

    test_dir = "./test_evolution_data"
    store = EvolutionStore(storage_dir=test_dir)

    snap = EvolutionSnapshot(optimization_plans_applied=5, learning_insights_count=3)
    store.save_snapshot(snap)

    # Retrieve
    retrieved = store.get_snapshot(snap.snapshot_id)
    check("Snapshot retrievable", retrieved is not None)
    check("Data matches", retrieved.optimization_plans_applied == 5)

    # List
    all_snaps = store.list_snapshots()
    check("List returns snapshots", len(all_snaps) >= 1)

    # Latest
    latest = store.get_latest_snapshot()
    check("Latest snapshot found", latest is not None)

    # Delete
    deleted = store.delete_snapshot(snap.snapshot_id)
    check("Snapshot deleted", deleted)
    check("Snapshot gone", store.get_snapshot(snap.snapshot_id) is None)

    # Verify disk persistence
    check("Store file exists", os.path.exists(os.path.join(test_dir, "store.json")))

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)


def test_evolution_analytics():
    print("\n📈 Testing Evolution Analytics Tracker...")
    from app.core.evolution.evolution_analytics import EvolutionAnalyticsTracker

    tracker = EvolutionAnalyticsTracker()

    tracker.record_optimization(success=True)
    tracker.record_optimization(success=True)
    tracker.record_optimization(success=False)
    tracker.record_experiment(successful=True)
    tracker.record_experiment(successful=False)
    tracker.record_recommendation(implemented=True)
    tracker.record_recommendation(implemented=False)
    tracker.record_tuning_cycle()
    tracker.record_insights(5)
    tracker.record_capability_score(0.85)
    tracker.record_capability_score(0.90)
    tracker.record_regression(avoided=True)

    summary = tracker.get_summary()
    check("Optimization success rate ~0.67", abs(summary.optimization_success_rate - 0.6667) < 0.01)
    check("Experiments completed = 2", summary.experiments_completed == 2)
    check("Experiments successful = 1", summary.experiments_successful == 1)
    check("Recommendations = 2", summary.total_recommendations == 2)
    check("Recommendations implemented = 1", summary.recommendations_implemented == 1)
    check("Tuning cycles = 1", summary.total_tuning_cycles == 1)
    check("Insights = 5", summary.insights_discovered == 5)
    check("Capability growth > 0", summary.capability_growth_rate > 0)
    check("Regression avoidance = 1.0", summary.regression_avoidance_rate == 1.0)


def test_evolution_orchestrator():
    print("\n🎯 Testing Evolution Orchestrator (Full Cycle)...")
    from app.core.evolution.evolution_orchestrator import EvolutionOrchestrator

    orchestrator = EvolutionOrchestrator()
    result = orchestrator.execute_evolution_cycle()

    check("Result has capability_profile", "capability_profile" in result)
    check("Result has self_evaluation", "self_evaluation" in result)
    check("Result has optimization_plan", "optimization_plan" in result)
    check("Result has tuning_snapshot", "tuning_snapshot" in result)
    check("Result has learning_record", "learning_record" in result)
    check("Result has recommendations", "recommendations" in result)
    check("Result has experiment", "experiment" in result)
    check("Result has evolution_snapshot", "evolution_snapshot" in result)
    check("Result has analytics_summary", "analytics_summary" in result)
    check("Result has cycle_duration_ms", "cycle_duration_ms" in result)
    check("Cycle completed in < 1000ms", result["cycle_duration_ms"] < 1000)

    # Verify orchestrator output consistency
    cap = result["capability_profile"]
    check("Capability profile has scores", len(cap.get("scores", [])) == 10)
    check("Capability overall > 0", cap.get("overall_score", 0) > 0)

    eval_ = result["self_evaluation"]
    check("Evaluation has composite", eval_.get("composite_score", 0) > 0)

    opt = result["optimization_plan"]
    check("Optimization has recommendations", len(opt.get("recommendations", [])) > 0)

    # Cleanup evolution_data from orchestrator
    shutil.rmtree("./evolution_data", ignore_errors=True)


def test_backward_compatibility():
    print("\n🔒 Testing Backward Compatibility...")
    # Verify existing modules are unaffected
    from app.core.config import settings
    check("Config still loads", settings is not None)
    check("EVOLUTION_ENGINE_ENABLED present", hasattr(settings, "EVOLUTION_ENGINE_ENABLED"))
    check("MULTI_AGENT_ENABLED preserved", settings.MULTI_AGENT_ENABLED is True)

    from app.core.decision import decision_orchestrator
    check("Decision orchestrator still available", decision_orchestrator is not None)

    from app.core.knowledge import knowledge_orchestrator
    check("Knowledge orchestrator still available", knowledge_orchestrator is not None)


if __name__ == "__main__":
    print("=" * 60)
    print("ENTERPRISE SELF-OPTIMIZATION PLATFORM - INTEGRATION TEST")
    print("=" * 60)

    test_evolution_models()
    test_capability_analyzer()
    test_self_evaluation()
    test_optimization_engine()
    test_adaptive_tuner()
    test_performance_learning()
    test_recommendation_engine()
    test_experiment_manager()
    test_evolution_store()
    test_evolution_analytics()
    test_evolution_orchestrator()
    test_backward_compatibility()

    print("\n" + "=" * 60)
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("=" * 60)

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 ALL TESTS PASSED — Enterprise Self-Optimization Platform is operational.")
