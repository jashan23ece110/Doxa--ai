"""
Global Enterprise Security Platform.

Centralized entry point and master orchestrator unifying every Stage 6 subsystem:
Static Analysis, Reverse Engineering, Binary Intelligence, Dynamic Sandbox Analysis,
Threat Intelligence, Threat Hunting, Vulnerability Assessment, Digital Forensics,
Incident Response, Security Automation, Security Analytics, Security Knowledge Graph,
AI Security Engine, and Enterprise Security Dashboard.
Integrated with AI OS Kernel, Intelligence Core, RAG, and Memory.
"""

import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.security_types import ThreatReport, RiskAssessment
from app.core.security.security_intelligence import global_security_orchestrator


class SecurityPlatformStatus(BaseModel):
    platform_name: str = "Doxa Enterprise Cybersecurity Platform"
    version: str = "6.0.0"
    status: str = "OPERATIONAL"
    subsystems_active_count: int = 14
    health_score: float = 100.0
    initialized_at: float = Field(default_factory=time.time)


class EnterpriseSecurityPlatform:
    """Master Enterprise Security Platform Service."""

    def __init__(self):
        self._status = SecurityPlatformStatus()

    async def run_full_security_pipeline(
        self,
        binary_bytes: bytes,
        binary_name: str = "target.bin",
        user_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes unified master security analysis pipeline across all Stage 6 subsystems.

        Args:
            binary_bytes: Payload binary bytes.
            binary_name: Target binary filename.
            user_context: Execution context metadata.

        Returns:
            Dict containing unified platform analysis result.
        """
        start_time = time.time()
        security_logger.info(f"EnterpriseSecurityPlatform: Executing master pipeline for '{binary_name}' ({len(binary_bytes)} bytes).")

        # Invoke Global Security Intelligence Orchestrator
        assessment = await global_security_orchestrator.execute_unified_security_assessment(
            file_bytes=binary_bytes,
            file_name=binary_name,
            context=user_context,
        )

        elapsed_ms = (time.time() - start_time) * 1000.0
        assessment["platform_status"] = self._status.status
        assessment["total_platform_latency_ms"] = round(elapsed_ms, 2)

        security_logger.info(
            f"EnterpriseSecurityPlatform: Completed master security pipeline for '{binary_name}' in {elapsed_ms:.1f}ms."
        )

        return assessment

    def get_platform_status(self) -> SecurityPlatformStatus:
        """Retrieves global platform operational status."""
        return self._status


# Global EnterpriseSecurityPlatform instance
enterprise_security_platform = EnterpriseSecurityPlatform()
