"""
IOC Detection & Scoring Engine.

Detects file hashes, domains, URLs, IP addresses, mutexes, registry keys,
filenames, scheduled tasks, services, and process names with confidence scoring.
"""

from typing import Dict, Any, List
from app.core.logging import security_logger
from app.core.security.security_types import IOC, ThreatSeverity
from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult


class IOCEngine:
    """Enterprise IOC Detection Engine."""

    def extract_iocs_from_sandbox(self, result: SandboxExecutionResult) -> List[IOC]:
        """
        Extracts structured IOCs from sandbox execution telemetry.

        Args:
            result: SandboxExecutionResult model.

        Returns:
            List of IOC objects.
        """
        extracted_iocs: List[IOC] = []

        # 1. Network IOCs
        for conn in result.network_connections:
            dst_ip = conn.get("dst_ip")
            if dst_ip:
                extracted_iocs.append(IOC(
                    value=dst_ip,
                    ioc_type="ip",
                    source="sandbox_network",
                ))

        # 2. File IOCs
        for f in result.created_files:
            extracted_iocs.append(IOC(
                value=f,
                ioc_type="file_path",
                source="sandbox_filesystem",
            ))

        # 3. Registry IOCs
        for reg in result.modified_registry_keys:
            extracted_iocs.append(IOC(
                value=reg,
                ioc_type="registry_key",
                source="sandbox_registry",
            ))

        security_logger.info(f"IOCEngine: Extracted {len(extracted_iocs)} IOCs from execution '{result.execution_id}'.")
        return extracted_iocs


# Global IOCEngine instance
ioc_engine = IOCEngine()
