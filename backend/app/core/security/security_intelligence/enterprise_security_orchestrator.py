"""
Global Security Intelligence Orchestrator.

Highest-level security orchestration layer for Doxa.
Coordinates every Stage 6 security subsystem:
Static Analysis, Reverse Engineering, Dynamic Sandbox Analysis, Threat Intelligence,
Vulnerability Assessment, Incident Response, Security Automation, Threat Hunting,
Knowledge Graph, and AI Security Engine.
Integrated directly with the AI OS Kernel.
"""

import time
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_types import ThreatReport, RiskAssessment, IOC
from app.core.security.static_analysis import static_analysis_engine
from app.core.security.reverse_engineering import function_recovery_engine
from app.core.security.dynamic_analysis import sandbox_manager, behavior_analyzer, ioc_engine
from app.core.security.secops import incident_manager, secops_playbook_engine
from app.core.security.threat_management import vulnerability_engine, threat_model_engine
from app.core.security.security_intelligence.threat_hunting_engine import threat_hunting_engine
from app.core.security.security_intelligence.security_knowledge_graph import security_knowledge_graph
from app.core.security.security_intelligence.security_ai_engine import security_ai_engine
from app.core.security.security_intelligence.defense_orchestrator import defense_orchestrator
from app.core.security.security_intelligence.security_memory import security_memory_engine
from app.core.security.security_intelligence.security_health_monitor import security_health_monitor


class GlobalSecurityIntelligenceOrchestrator:
    """Global Security Intelligence & Autonomous Defense Orchestrator for Doxa."""

    async def execute_unified_security_assessment(
        self,
        file_bytes: bytes,
        file_name: str = "sample.bin",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes unified security intelligence orchestration across all Stage 6 subsystems.

        Args:
            file_bytes: Binary payload bytes.
            file_name: Name of file.
            context: Execution context.

        Returns:
            Dict containing unified security assessment summary.
        """
        start_time = time.time()
        security_logger.info(f"GlobalSecurityIntelligenceOrchestrator: Initiating unified security assessment for '{file_name}'.")

        # 1. Static Analysis
        static_res, report = await static_analysis_engine.analyze_bytes(file_bytes, file_name)

        # 2. Dynamic Sandbox Execution & Telemetry
        sandbox_res = await sandbox_manager.run_in_sandbox(static_res.binary_id, file_bytes)
        behavioral_rep = behavior_analyzer.analyze_sandbox_result(sandbox_res)
        extracted_iocs = ioc_engine.extract_iocs_from_sandbox(sandbox_res)

        # 3. Vulnerability Correlation & STRIDE Threat Model
        vulnerabilities = vulnerability_engine.correlate_cve(file_name)
        threat_model = threat_model_engine.generate_stride_model(file_name, [file_name], ["Sandbox"])

        # 4. Knowledge Graph Node Sync
        node_id = f"bin_{static_res.binary_id[:8]}"
        security_knowledge_graph.add_node(node_id, "malware_sample", file_name, {"sha256": static_res.fingerprint.sha256})

        # 5. AI Correlation & Defense Orchestration
        ai_res = security_ai_engine.analyze_findings([{"binary_id": static_res.binary_id, "risk": report.risk_assessment.overall_risk_score}])
        defense_res = await defense_orchestrator.orchestrate_defense_response(static_res.binary_id, report.risk_assessment, extracted_iocs)

        # 6. Security Memory Sync
        security_memory_engine.remember_investigation(static_res.binary_id, report.summary)

        elapsed_ms = (time.time() - start_time) * 1000.0
        security_logger.info(
            f"GlobalSecurityIntelligenceOrchestrator: Completed unified security assessment for '{file_name}' in {elapsed_ms:.1f}ms. "
            f"RiskScore={report.risk_assessment.overall_risk_score:.1f}/10.0"
        )

        return {
            "file_name": file_name,
            "binary_id": static_res.binary_id,
            "overall_risk_score": report.risk_assessment.overall_risk_score,
            "threat_level": report.risk_assessment.threat_level.value.upper(),
            "static_analysis": static_res.model_dump(),
            "behavioral_report": behavioral_rep.model_dump(),
            "iocs_count": len(extracted_iocs),
            "vulnerabilities_count": len(vulnerabilities),
            "ai_confidence": ai_res.confidence_score,
            "defense_status": defense_res["remediation_status"],
            "execution_time_ms": round(elapsed_ms, 2),
        }

    def get_system_security_health(self) -> Dict[str, Any]:
        """Retrieves global platform security health status."""
        health = security_health_monitor.check_health()
        return health.model_dump()


# Global GlobalSecurityIntelligenceOrchestrator instance
global_security_orchestrator = GlobalSecurityIntelligenceOrchestrator()
