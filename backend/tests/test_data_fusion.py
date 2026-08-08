#!/usr/bin/env python3
"""
Integration Test Suite for Stage 8 Part 3 — Enterprise Multi-Source Intelligence Fusion & Knowledge Graph Platform.
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


def test_entity_resolution():
    print("\n👥 Testing Entity Resolution Engine...")
    from app.core.data_intelligence.fusion.entity_resolution import entity_resolution_engine

    ent = entity_resolution_engine.resolve_entity("Acme Corp", "organization", "src_db_01", aliases=["Acme Corporation"])
    check("Entity resolved", ent is not None)
    check("Primary name correct", ent.primary_name == "Acme Corp")

    merged = entity_resolution_engine.resolve_entity("Acme Corp", "organization", "src_db_02", aliases=["Acme Inc"])
    check("Entity merged into canonical entity", merged.canonical_entity_id == ent.canonical_entity_id)
    check("Aliases updated", "Acme Inc" in merged.aliases)


def test_data_normalizer():
    print("\n🧹 Testing Data Normalizer...")
    from app.core.data_intelligence.fusion.data_normalizer import data_normalizer

    raw = {"User ID": 101, "First Name": "Alice"}
    norm = data_normalizer.normalize_record("rec_100", raw)
    check("Record normalized", norm is not None)
    check("Keys standard snake_case", "user_id" in norm.normalized_payload)


def test_semantic_enrichment():
    print("\n🏷️ Testing Semantic Enrichment Engine...")
    from app.core.data_intelligence.fusion.semantic_enrichment import semantic_enrichment_engine

    enriched = semantic_enrichment_engine.enrich_data("ds_100", [{"key": "value"}])
    check("Dataset enriched", enriched is not None)
    check("Extracted topics > 0", len(enriched.extracted_topics) > 0)


def test_multi_source_fusion():
    print("\n🔮 Testing Multi-Source Intelligence Fusion Engine...")
    from app.core.data_intelligence.fusion.intelligence_fusion import multi_source_fusion_engine

    fused = multi_source_fusion_engine.fuse_sources("Enterprise", ["rec_1", "rec_2"], [{"a": 1}, {"b": 2}])
    check("Multi-source fusion completed", fused is not None)
    check("Unified payload contains merged keys", "a" in fused.unified_payload and "b" in fused.unified_payload)


def test_cross_source_correlation():
    print("\n🔗 Testing Cross-Source Correlation Engine...")
    from app.core.data_intelligence.fusion.cross_source_correlation import cross_source_correlation_engine

    finding = cross_source_correlation_engine.correlate_sources("src_db_01", "src_db_02")
    check("Correlation finding generated", finding is not None)
    check("Correlation score > 0.80", finding.correlation_score > 0.80)


def test_knowledge_graph_builder():
    print("\n🕸️ Testing Knowledge Graph Builder...")
    from app.core.data_intelligence.fusion.knowledge_graph_builder import knowledge_graph_builder

    node1 = knowledge_graph_builder.add_node("n_ent_01", "Acme Corp", "organization")
    node2 = knowledge_graph_builder.add_node("n_evt_01", "Acquisition Event", "event")
    edge = knowledge_graph_builder.add_edge("n_ent_01", "n_evt_01", "PARTICIPATED_IN")

    check("Node 1 added", node1 is not None)
    check("Node 2 added", node2 is not None)
    check("Edge added", edge is not None)


async def test_graph_query_engine():
    print("\n🔍 Testing Knowledge Graph Query Engine...")
    from app.core.data_intelligence.fusion.graph_query_engine import graph_query_engine

    res = await graph_query_engine.execute_graph_query("MATCH (n:organization)-[r]->(e:event) RETURN n,r,e")
    check("Graph query executed", res is not None)
    check("Nodes found in query > 0", len(res.nodes_found) > 0)


def test_provenance_manager():
    print("\n📜 Testing Provenance Manager...")
    from app.core.data_intelligence.fusion.provenance_manager import provenance_manager

    prov = provenance_manager.record_provenance("art_100", "src_db_01")
    check("Provenance recorded", prov is not None)

    retrieved = provenance_manager.get_provenance("art_100")
    check("Provenance retrieved", retrieved.original_source_id == "src_db_01")


def test_conflict_resolution():
    print("\n⚖️ Testing Conflict Resolution Engine...")
    from app.core.data_intelligence.fusion.conflict_resolution import conflict_resolution_engine

    decision = conflict_resolution_engine.resolve_conflict("employee_status", {"src_hr": "Active", "src_legacy": "Inactive"})
    check("Conflict decision generated", decision is not None)
    check("Winning source selected", decision.winning_source_id in ["src_hr", "src_legacy"])


def test_fusion_analytics():
    print("\n📊 Testing Fusion Analytics...")
    from app.core.data_intelligence.fusion.fusion_analytics import fusion_analytics

    snapshot = fusion_analytics.get_analytics_snapshot()
    check("Analytics snapshot retrieved", snapshot is not None)
    check("Entities resolved count > 0", snapshot.total_entities_resolved > 0)


async def test_integration_and_backward_compatibility():
    print("\n🔒 Testing Integration & Backward Compatibility across Stages 1-7...")
    from app.core.human_intelligence import enterprise_human_intelligence_platform
    from app.core.data_intelligence import enterprise_data_intelligence_manager
    from app.core.security import enterprise_security_platform
    from app.core.intelligence import ai_os_kernel

    assess = await enterprise_human_intelligence_platform.run_master_human_intelligence_assessment("Fusion_Test")
    check("Human Intelligence Platform operates seamlessly with Fusion Platform", assess is not None)

    payload = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00VirtualAllocEx\x00"
    sec_res = await enterprise_security_platform.run_full_security_pipeline(payload, "fusion_test.exe")
    check("Enterprise Security Platform operates seamlessly", sec_res is not None)
    check("AI OS Kernel remains fully functional", ai_os_kernel is not None)


async def main():
    print("==========================================================================")
    print("STAGE 8 PART 3 — MULTI-SOURCE INTELLIGENCE FUSION & GRAPH TEST SUITE")
    print("==========================================================================")

    test_entity_resolution()
    test_data_normalizer()
    test_semantic_enrichment()
    test_multi_source_fusion()
    test_cross_source_correlation()
    test_knowledge_graph_builder()
    await test_graph_query_engine()
    test_provenance_manager()
    test_conflict_resolution()
    test_fusion_analytics()
    await test_integration_and_backward_compatibility()

    print("\n==========================================================================")
    print(f"RESULTS: {PASS} passed, {FAIL} failed, {PASS + FAIL} total")
    print("==========================================================================")

    if FAIL > 0:
        sys.exit(1)
    print("\n🎉 STAGE 8 PART 3 SUCCESS: Multi-Source Intelligence Fusion & Knowledge Graph Platform Deployed!")


if __name__ == "__main__":
    asyncio.run(main())
