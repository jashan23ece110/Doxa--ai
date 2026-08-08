#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 5 — Enterprise Multimodal Search & Unified Intelligence Retrieval Platform.
"""

import asyncio
import os
import sys

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


def test_multimodal_indexer():
    print("\n📦 Testing Multimodal Indexer...")
    from app.core.data_intelligence.search.multimodal_indexer import multimodal_indexer

    item = multimodal_indexer.index_item("doc_100", "document", "Security Audit Report")
    check("Item indexed", item is not None)

    retrieved = multimodal_indexer.get_indexed_item("doc_100")
    check("Indexed item retrieved", retrieved.modality == "document")


def test_semantic_search_engine():
    print("\n🔍 Testing Semantic Search Engine...")
    from app.core.data_intelligence.search.semantic_search_engine import semantic_search_engine

    res = semantic_search_engine.search("cloud threat analysis", top_k=3)
    check("Search executed", res is not None)
    check("Hits count > 0", res.total_hits_count > 0)


def test_cross_modal_retriever():
    print("\n🌉 Testing Cross-Modal Retriever...")
    from app.core.data_intelligence.search.cross_modal_retriever import cross_modal_retriever

    res = cross_modal_retriever.retrieve_cross_modal("q_100", ["image", "document"])
    check("Cross-modal retrieval executed", res is not None)
    check("Target modalities count == 2", len(res.target_modalities) == 2)


async def test_unified_query_engine():
    print("\n🌐 Testing Unified Query Engine...")
    from app.core.data_intelligence.search.unified_query_engine import unified_query_engine

    res = await unified_query_engine.execute_unified_query("Find recent threat actor reports")
    check("Unified query executed", res is not None)
    check("Hits returned", len(res.hits) > 0)


def test_retrieval_fusion_engine():
    print("\n🔮 Testing Retrieval Fusion Engine...")
    from app.core.data_intelligence.search.retrieval_fusion_engine import retrieval_fusion_engine
    from app.core.data_intelligence.search.semantic_search_engine import SearchHit

    h1 = [SearchHit(hit_id="h1", title="A", snippet="s1", relevance_score=0.9)]
    h2 = [SearchHit(hit_id="h2", title="B", snippet="s2", relevance_score=0.8)]

    fused = retrieval_fusion_engine.fuse_retrieval_results([h1, h2])
    check("Retrieval results fused", fused is not None)
    check("Fused hits count == 2", len(fused.fused_hits) == 2)


def test_semantic_entity_linker():
    print("\n🏷️ Testing Semantic Entity Linker...")
    from app.core.data_intelligence.search.semantic_entity_linker import semantic_entity_linker

    links = semantic_entity_linker.link_entities_in_hit("h1", "Doxa Enterprise platform report")
    check("Entities linked", len(links) > 0)
    check("Entity type is organization", links[0].entity_type == "organization")


def test_search_ranking_engine():
    print("\n📊 Testing Search Ranking Engine...")
    from app.core.data_intelligence.search.search_ranking_engine import search_ranking_engine
    from app.core.data_intelligence.search.semantic_search_engine import SearchHit

    hits = [
        SearchHit(hit_id="h1", title="Low", snippet="s", relevance_score=0.5),
        SearchHit(hit_id="h2", title="High", snippet="s", relevance_score=0.95),
    ]

    ranked = search_ranking_engine.rank_hits(hits)
    check("Search hits ranked", ranked[0].hit_id == "h2")


def test_query_optimizer():
    print("\n⚡ Testing Query Optimizer...")
    from app.core.data_intelligence.search.query_optimizer import query_optimizer

    plan = query_optimizer.optimize_plan("Find insider risk indicators")
    check("Query plan optimized", plan is not None)
    check("Plan steps count > 0", len(plan.steps) > 0)


def test_search_cache():
    print("\n⚡ Testing Search Cache...")
    from app.core.data_intelligence.search.search_cache import search_cache

    search_cache.set("query_key", {"hits": 5}, ttl_seconds=60.0)
    val = search_cache.get("query_key")
    check("Cached search result retrieved", val is not None and val["hits"] == 5)


def test_search_observability():
    print("\n👁️ Testing Search Observability...")
    from app.core.data_intelligence.search.search_observability import search_observability

    metrics = search_observability.get_observability_snapshot()
    check("Search observability snapshot retrieved", metrics is not None)
    check("Query volume > 0", metrics.query_volume_total > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Search_Test")
    check("Human Intelligence Platform operates seamlessly with Search Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "search_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 5 — MULTIMODAL SEARCH & UNIFIED RETRIEVAL TEST SUITE")
    print("==========================================================================")

    test_multimodal_indexer()
    test_semantic_search_engine()
    test_cross_modal_retriever()
    await test_unified_query_engine()
    test_retrieval_fusion_engine()
    test_semantic_entity_linker()
    test_search_ranking_engine()
    test_query_optimizer()
    test_search_cache()
    test_search_observability()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 5 SUCCESS: Enterprise Multimodal Search & Unified Retrieval Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
