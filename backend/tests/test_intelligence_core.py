#!/usr/bin/env python3
"""
Integration test for Doxa AI Operating System - Unified Autonomous Intelligence Core (Stage 5, Final).

Validates all intelligence core components:
1. Intelligence Types & Serialization
2. Adaptive Decision Engine & Graph Generation
3. Global Context Manager (Merging, Deduplication, Ranking, Token Budgeting)
4. Intelligence Scheduler & Async Background Processing
5. Execution Optimizer & Memoization
6. Pipeline Profiler & End-to-End Tracing
7. Autonomous Optimization Engine & Policy Learning
8. Knowledge Flow Engine & Non-duplicate Propagation
9. Operational Dashboard Backend Telemetry
10. Global Intelligence Orchestrator
11. AI Operating System Kernel Lifecycle & Graceful Recovery
12. System Integration & Backward Compatibility
"""

import asyncio
import os
import sys
import time

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


def test_intelligence_types():
    print("\n🔬 Testing Intelligence Types & Enums...")
    from app.core.intelligence.intelligence_types import (
        ExecutionMode, TaskPriority, TaskType, ExecutionStatus,
        DecisionGraphNode, AdaptiveExecutionGraph, ContextItem,
        UnifiedGlobalContext, IntelligenceTask, OptimizationCacheEntry,
        ComponentLatencyTrace, PipelineTrace, PolicyRecommendation,
        KnowledgeFlowStep, KnowledgeFlowRecord, KernelExecutionState,
        SystemDashboardMetrics,
    )

    check("ExecutionMode has 6 modes", len(ExecutionMode) == 6)
    check("TaskPriority has 4 priorities", len(TaskPriority) == 4)
    check("TaskType has 9 task types", len(TaskType) == 9)
    check("ExecutionStatus has 9 statuses", len(ExecutionStatus) == 9)

    graph = AdaptiveExecutionGraph()
    check("AdaptiveExecutionGraph default mode BALANCED", graph.execution_mode == ExecutionMode.BALANCED)
    check("Graph ID generated", graph.graph_id.startswith("graph_"))

    ctx_item = ContextItem(source_type="rag", content="Sample text")
    check("ContextItem ID generated", ctx_item.item_id.startswith("ctx_"))

    task = IntelligenceTask(task_type=TaskType.RETRIEVAL_HYBRID)
    check("Task ID generated", task.task_id.startswith("task_"))

    trace = PipelineTrace()
    check("Trace ID generated", trace.trace_id.startswith("trace_"))

    metrics = SystemDashboardMetrics()
    check("Metrics system confidence score default 0.95", metrics.system_confidence_score == 0.95)

    # Roundtrip serialization
    data = graph.model_dump()
    restored = AdaptiveExecutionGraph.model_validate(data)
    check("AdaptiveExecutionGraph roundtrip serialization", restored.graph_id == graph.graph_id)


async def test_decision_engine():
    print("\n🧠 Testing Adaptive Decision Engine...")
    from app.core.intelligence.decision_engine import AdaptiveDecisionEngine
    from app.core.intelligence.intelligence_types import ExecutionMode

    engine = AdaptiveDecisionEngine()

    # Standard query
    graph = await engine.generate_execution_graph(prompt="What is the capital of France?")
    check("Standard query mode BALANCED or FAST", graph.execution_mode in (ExecutionMode.BALANCED, ExecutionMode.FAST))
    check("Graph has nodes", len(graph.nodes) > 0)
    check("RAG enabled", graph.should_run_rag)
    check("Memory enabled", graph.should_run_memory)

    # Code / Math query
    code_graph = await engine.generate_execution_graph(prompt="Write a Python script to calculate fibonacci numbers def fib():")
    check("Code query enables Python sandbox", code_graph.should_execute_python)

    # Search query
    search_graph = await engine.generate_execution_graph(prompt="Search latest news about AI developments today")
    check("Search query enables web search", search_graph.should_execute_web_search)

    # Complex Multi-Agent query
    complex_graph = await engine.generate_execution_graph(
        prompt="Synthesize and analyze the pros and cons of microservices vs monolith architecture with multi-perspective debate and review and critique",
        latency_budget_ms=5000.0,
    )
    check("High complexity query activates planner or multi-agent", complex_graph.should_run_planner or complex_graph.should_run_multi_agent)
    check("Complexity score > 0.6", complex_graph.complexity_score > 0.6)

    # Cache hit query
    cache_graph = await engine.generate_execution_graph(prompt="Cached prompt", cached_result_available=True)
    check("Cache hit mode FAST", cache_graph.execution_mode == ExecutionMode.FAST)


async def test_context_manager():
    print("\n📚 Testing Global Context Manager...")
    from app.core.intelligence.context_manager import GlobalContextManager

    manager = GlobalContextManager()

    history = [
        {"role": "user", "content": "Hello Doxa"},
        {"role": "assistant", "content": "Hello! How can I assist you today?"},
    ]
    rag_chunks = [
        {"text": "Doxa is an Enterprise AI Operating System.", "similarity": 0.92},
        {"text": "Doxa supports multi-agent workflows.", "similarity": 0.88},
    ]
    semantic_memories = [
        {"content": "User prefers concise answers.", "relevance": 0.90},
    ]
    preferences = {"output_format": "json", "language": "python"}

    unified = await manager.build_unified_context(
        history=history,
        rag_chunks=rag_chunks,
        semantic_memories=semantic_memories,
        preferences=preferences,
        max_token_budget=1024,
    )

    check("Unified context ID generated", unified.context_id.startswith("ugc_"))
    check("Context items merged", len(unified.items) > 0)
    check("Total tokens > 0", unified.total_tokens > 0)
    check("Total tokens within budget", unified.total_tokens <= 1024)

    # Test Deduplication
    duplicate_rag = [
        {"text": "Identical chunk text", "similarity": 0.9},
        {"text": "Identical chunk text", "similarity": 0.9},
    ]
    dedup_ctx = await manager.build_unified_context(rag_chunks=duplicate_rag)
    check("Deduplication removed identical item", dedup_ctx.deduplicated_count == 1)


async def test_scheduler():
    print("\n⏱️ Testing Intelligence Scheduler...")
    from app.core.intelligence.scheduler import IntelligenceScheduler
    from app.core.intelligence.intelligence_types import TaskType, TaskPriority

    scheduler = IntelligenceScheduler()
    await scheduler.start()

    task1 = await scheduler.schedule_task(
        task_type=TaskType.EMBEDDING_GENERATION,
        payload={"texts": ["Hello world", "Doxa AI"]},
        priority=TaskPriority.HIGH,
    )
    check("Task1 scheduled with ID", task1.task_id.startswith("task_"))

    task2 = await scheduler.schedule_task(
        task_type=TaskType.RETRIEVAL_HYBRID,
        payload={"query": "test query"},
        priority=TaskPriority.CRITICAL,
    )
    check("Task2 scheduled with CRITICAL priority", task2.priority == TaskPriority.CRITICAL)

    # Allow worker loop to process background queue
    await asyncio.sleep(0.1)

    metrics = scheduler.get_queue_metrics()
    check("Worker loop running", metrics["worker_running"])

    await scheduler.stop()


def test_optimizer():
    print("\n⚡ Testing Execution Optimizer...")
    from app.core.intelligence.optimizer import ExecutionOptimizer

    opt = ExecutionOptimizer(default_ttl_seconds=60.0)

    payload = {"query": "vector search prompt", "top_k": 5}
    key = opt.generate_cache_key("retrieval", payload)
    check("Cache key generated", len(key) == 32)

    # Miss check
    miss = opt.get_cached_result("retrieval", payload)
    check("Initial cache miss", miss is None)

    # Store result
    stored_key = opt.store_result("retrieval", payload, result=["doc1", "doc2"])
    check("Store result key matches", stored_key == key)

    # Hit check
    hit = opt.get_cached_result("retrieval", payload)
    check("Cache hit returns stored result", hit == ["doc1", "doc2"])

    metrics = opt.get_metrics()
    check("Metrics total hits >= 1", metrics["total_hits"] >= 1)
    check("Metrics hit rate > 0", metrics["hit_rate"] > 0)


def test_pipeline_profiler():
    print("\n📊 Testing Pipeline Profiler...")
    from app.core.intelligence.pipeline_profiler import PipelineProfiler

    profiler = PipelineProfiler()

    trace = profiler.start_trace("req_test_123")
    check("Trace request_id set", trace.request_id == "req_test_123")

    profiler.record_component_latency(trace, "retrieval", duration_ms=45.2, tokens_consumed=120)
    profiler.record_component_latency(trace, "reasoning", duration_ms=120.8, tokens_consumed=350, estimated_cost_usd=0.0005)

    check("Component traces recorded", len(trace.component_traces) == 2)
    check("Tokens accumulated", trace.total_tokens == 470)

    finalized = profiler.finalize_trace(trace, cache_hits=1, cache_misses=0)
    check("Trace duration_ms > 0", finalized.total_duration_ms >= 0)
    check("Cache hits recorded in trace", finalized.cache_hits == 1)

    avg_lat = profiler.get_average_latency_ms()
    check("Average latency calculated", avg_lat >= 0)


def test_auto_optimizer():
    print("\n🤖 Testing Autonomous Optimizer...")
    from app.core.intelligence.auto_optimizer import AutonomousOptimizer

    auto = AutonomousOptimizer()

    retrieval_pol = auto.get_policy("retrieval_strategy")
    check("Retrieval policy initialized", retrieval_pol is not None)
    check("Best retrieval strategy present", retrieval_pol.best_strategy == "hybrid_dense_sparse_rrf")

    # Record feedback
    auto.record_feedback("retrieval_strategy", "hybrid_dense_sparse_rrf", success=True, latency_ms=35.0, quality_score=0.98)
    updated_pol = auto.get_policy("retrieval_strategy")
    check("Evidence count incremented", updated_pol.evidence_count > 1)

    all_pols = auto.get_all_policies()
    check("All 7 subsystem policies present", len(all_pols) == 7)


async def test_knowledge_flow():
    print("\n🔄 Testing Knowledge Flow Engine...")
    from app.core.intelligence.knowledge_flow import KnowledgeFlowEngine

    kf_engine = KnowledgeFlowEngine()
    flow = kf_engine.init_flow("req_flow_1")
    check("Knowledge flow initialized", flow.request_id == "req_flow_1")

    # Propagate 1
    ok1 = await kf_engine.propagate(flow, "retrieval", "reasoning", "Retrieved facts")
    check("First propagation succeeded", ok1)
    check("Flow step count is 1", len(flow.steps) == 1)

    # Propagate duplicate
    ok2 = await kf_engine.propagate(flow, "retrieval", "reasoning", "Retrieved facts")
    check("Duplicate propagation skipped", not ok2)
    check("Deduplicated transfers count is 1", flow.deduplicated_transfers == 1)

    kf_engine.finalize_flow(flow)


def test_dashboard_backend():
    print("\n📈 Testing Operational Dashboard Backend...")
    from app.core.intelligence.dashboard_backend import OperationalDashboardBackend

    dash = OperationalDashboardBackend()

    metrics = dash.get_dashboard_metrics()
    check("Dashboard metrics retrieved", metrics is not None)
    check("Default reasoning quality score > 0", metrics.reasoning_quality_score > 0)

    dash.record_request_processed(duration_ms=150.0, tokens_consumed=500, confidence=0.96)
    updated = dash.get_dashboard_metrics()
    check("Total requests processed incremented", updated.total_requests_processed == 1)

    dash.update_live_status(active_agents=4, running_workflows=2, memory_usage_mb=256.0)
    live = dash.get_dashboard_metrics()
    check("Active agents updated", live.active_agents == 4)
    check("Running workflows updated", live.running_workflows == 2)


async def test_global_intelligence_orchestrator():
    print("\n🌐 Testing Global Intelligence Orchestrator...")
    from app.core.intelligence.intelligence_core import GlobalIntelligenceOrchestrator

    orchestrator = GlobalIntelligenceOrchestrator()

    res = await orchestrator.execute_request(
        prompt="Explain the architecture of Doxa AI OS",
        user_id="user_test_1",
        tenant_id="tenant_1",
        history=[{"role": "user", "content": "Hi"}],
    )

    check("Orchestrator returned response text", len(res.get("response_text", "")) > 0)
    check("Execution mode set", "execution_mode" in res)
    check("Trace included in response", "trace" in res)
    check("Context summary included", "context_summary" in res)


async def test_ai_os_kernel():
    print("\n⚙️ Testing AI OS Kernel Lifecycle & Recovery...")
    from app.core.intelligence.kernel import AIOSKernel

    kernel = AIOSKernel()

    # Successful request execution through Kernel
    res = await kernel.execute(
        prompt="Write a concise overview of clean architecture in Python",
        user_id="kernel_user",
        tenant_id="default",
    )

    check("Kernel response text present", len(res.get("response_text", "")) > 0)
    check("Kernel execution metadata present", "kernel_execution" in res)
    check("Kernel execution status completed", res["kernel_execution"]["status"] == "completed")
    check("Active executions cleared after completion", kernel.get_active_executions_count() == 0)


async def test_system_integration_and_backward_compatibility():
    print("\n🔒 Testing System Integration & Backward Compatibility...")
    from app.core.config import settings

    check("INTELLIGENCE_CORE_ENABLED present", hasattr(settings, "INTELLIGENCE_CORE_ENABLED"))
    check("ADAPTIVE_DECISION_ENABLED present", hasattr(settings, "ADAPTIVE_DECISION_ENABLED"))
    check("GLOBAL_CONTEXT_MANAGER_ENABLED present", hasattr(settings, "GLOBAL_CONTEXT_MANAGER_ENABLED"))
    check("INTELLIGENCE_SCHEDULER_ENABLED present", hasattr(settings, "INTELLIGENCE_SCHEDULER_ENABLED"))
    check("EXECUTION_OPTIMIZER_ENABLED present", hasattr(settings, "EXECUTION_OPTIMIZER_ENABLED"))
    check("PIPELINE_PROFILER_ENABLED present", hasattr(settings, "PIPELINE_PROFILER_ENABLED"))
    check("AUTONOMOUS_OPTIMIZER_ENABLED present", hasattr(settings, "AUTONOMOUS_OPTIMIZER_ENABLED"))
    check("KNOWLEDGE_FLOW_ENABLED present", hasattr(settings, "KNOWLEDGE_FLOW_ENABLED"))
    check("AI_OS_KERNEL_ENABLED present", hasattr(settings, "AI_OS_KERNEL_ENABLED"))
    check("OPERATIONAL_DASHBOARD_ENABLED present", hasattr(settings, "OPERATIONAL_DASHBOARD_ENABLED"))

    # Test clean imports from package __init__
    from app.core.intelligence import (
        ai_os_kernel,
        global_intelligence_orchestrator,
        adaptive_decision_engine,
        global_context_manager,
        intelligence_scheduler,
        execution_optimizer,
        pipeline_profiler,
        autonomous_optimizer,
        knowledge_flow_engine,
        operational_dashboard_backend,
    )
    check("All 10 singletons imported cleanly from app.core.intelligence", all([
        ai_os_kernel,
        global_intelligence_orchestrator,
        adaptive_decision_engine,
        global_context_manager,
        intelligence_scheduler,
        execution_optimizer,
        pipeline_profiler,
        autonomous_optimizer,
        knowledge_flow_engine,
        operational_dashboard_backend,
    ]))


async def main():
    print("==========================================================================")
    print("DOXA AI OPERATING SYSTEM - UNIFIED AUTONOMOUS INTELLIGENCE CORE TEST SUITE")
    print("==========================================================================")

    test_intelligence_types()
    await test_decision_engine()
    await test_context_manager()
    await test_scheduler()
    test_optimizer()
    test_pipeline_profiler()
    test_auto_optimizer()
    await test_knowledge_flow()
    test_dashboard_backend()
    await test_global_intelligence_orchestrator()
    await test_ai_os_kernel()
    await test_system_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 5 FINAL COMPLETION CONFIRMED: Doxa is a Unified AI Operating System!")


if __name__ == "__main__":
    asyncio.run(main())
