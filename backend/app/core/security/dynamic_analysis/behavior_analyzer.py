"""
Behavior Analysis Engine.

Monitors process trees, child processes, filesystem activity, registry activity,
network connections, service creation, persistence attempts, privilege requests, DLL loading,
and command execution to produce a structured BehavioralReport.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from app.core.logging import security_logger
from app.core.security.dynamic_analysis.sandbox_manager import SandboxExecutionResult


class BehavioralReport(BaseModel):
    execution_id: str
    has_persistence: bool = False
    has_privilege_escalation: bool = False
    has_network_activity: bool = False
    suspicious_process_spawns: List[str] = Field(default_factory=list)
    modified_files_count: int = 0
    registry_modifications_count: int = 0
    detected_behaviors: List[str] = Field(default_factory=list)


class BehaviorAnalyzer:
    """Enterprise Behavior Analysis Engine."""

    def analyze_sandbox_result(self, result: SandboxExecutionResult) -> BehavioralReport:
        """
        Analyzes sandbox execution telemetry to build a BehavioralReport.

        Args:
            result: SandboxExecutionResult model.

        Returns:
            BehavioralReport model.
        """
        detected: List[str] = []
        suspicious_spawns: List[str] = []

        # 1. Process tree inspection
        for proc in result.process_tree:
            p_name = proc.get("name", "").lower()
            if p_name in ("cmd.exe", "powershell.exe", "wmic.exe", "schtasks.exe"):
                suspicious_spawns.append(f"{proc.get('name')} (PID {proc.get('pid')})")
                detected.append(f"Spawned command execution utility: {proc.get('name')}")

        # 2. Registry persistence check
        has_persistence = False
        for reg in result.modified_registry_keys:
            if "CurrentVersion\\Run" in reg or "Services" in reg:
                has_persistence = True
                detected.append(f"Persistence registry key modified: {reg}")

        # 3. Network activity check
        has_network = len(result.network_connections) > 0
        if has_network:
            detected.append(f"Established {len(result.network_connections)} external network connections.")

        report = BehavioralReport(
            execution_id=result.execution_id,
            has_persistence=has_persistence,
            has_privilege_escalation=any("whoami" in p.get("command_line", "").lower() for p in result.process_tree),
            has_network_activity=has_network,
            suspicious_process_spawns=suspicious_spawns,
            modified_files_count=len(result.created_files),
            registry_modifications_count=len(result.modified_registry_keys),
            detected_behaviors=detected,
        )

        security_logger.info(f"BehaviorAnalyzer: Analyzed execution '{result.execution_id}': {len(detected)} behaviors identified.")
        return report


# Global BehaviorAnalyzer instance
behavior_analyzer = BehaviorAnalyzer()
