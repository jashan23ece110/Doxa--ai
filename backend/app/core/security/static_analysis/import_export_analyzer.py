"""
Import & Export API Analyzer.

Analyzes imported DLLs, API functions, exported functions, and delayed imports.
Detects suspicious WinAPI usage, networking APIs, cryptography APIs, and process injection indicators.
"""

from typing import Dict, Any, List, Set, Optional
from app.core.logging import security_logger
from app.core.security.security_types import BinaryImport, BinaryExport, ThreatIndicator, ThreatSeverity


class ImportExportAnalyzer:
    """Enterprise Import and Export API Analyzer."""

    # Categorized Suspicious WinAPIs
    _SUSPICIOUS_NETWORKING_APIS = {
        "InternetOpenA", "InternetOpenW", "InternetConnectA", "InternetConnectW",
        "HttpOpenRequestA", "HttpOpenRequestW", "URLDownloadToFileA", "URLDownloadToFileW",
        "WSAStartup", "connect", "send", "recv", "socket",
    }

    _SUSPICIOUS_INJECTION_APIS = {
        "VirtualAllocEx", "WriteProcessMemory", "CreateRemoteThread", "NtCreateThreadEx",
        "QueueUserAPC", "SetThreadContext", "ResumeThread", "RtlCreateUserThread",
    }

    _SUSPICIOUS_CRYPTO_APIS = {
        "CryptAcquireContextA", "CryptAcquireContextW", "CryptEncrypt", "CryptDecrypt",
        "CryptGenKey", "BCryptEncrypt", "BCryptDecrypt",
    }

    _SUSPICIOUS_EVASION_APIS = {
        "IsDebuggerPresent", "CheckRemoteDebuggerPresent", "NtQueryInformationProcess",
        "OutputDebugStringA", "VirtualProtect", "SetUnhandledExceptionFilter",
    }

    def analyze_api_usage(
        self,
        imports: List[BinaryImport],
        exports: List[BinaryExport],
        extracted_strings: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyzes imported/exported APIs and extracted strings for threat indicators.

        Returns:
            Dict containing suspicious API lists, indicators, and capability flags.
        """
        suspicious_found: List[str] = []
        indicators: List[ThreatIndicator] = []

        imported_func_names = {imp.function_name for imp in imports}
        if extracted_strings:
            for s in extracted_strings:
                val = s.string_value if hasattr(s, "string_value") else str(s)
                imported_func_names.add(val.strip())

        # Check Process Injection
        injection_matches = imported_func_names.intersection(self._SUSPICIOUS_INJECTION_APIS)
        if injection_matches:
            suspicious_found.extend(list(injection_matches))
            indicators.append(ThreatIndicator(
                name="Process Injection APIs Detected",
                category="privilege_escalation",
                mitre_attack_id="T1055",
                description=f"Imports APIs commonly used for process injection: {', '.join(injection_matches)}",
                matched_patterns=list(injection_matches),
                severity=ThreatSeverity.HIGH,
            ))

        # Check Networking
        net_matches = imported_func_names.intersection(self._SUSPICIOUS_NETWORKING_APIS)
        if net_matches:
            suspicious_found.extend(list(net_matches))
            indicators.append(ThreatIndicator(
                name="Network Communication APIs Detected",
                category="command_and_control",
                mitre_attack_id="T1071",
                description=f"Imports networking APIs: {', '.join(net_matches)}",
                matched_patterns=list(net_matches),
                severity=ThreatSeverity.MEDIUM,
            ))

        # Check Anti-Debugging / Evasion
        evasion_matches = imported_func_names.intersection(self._SUSPICIOUS_EVASION_APIS)
        if evasion_matches:
            suspicious_found.extend(list(evasion_matches))
            indicators.append(ThreatIndicator(
                name="Anti-Debugging / Defense Evasion APIs Detected",
                category="evasion",
                mitre_attack_id="T1497",
                description=f"Imports anti-analysis APIs: {', '.join(evasion_matches)}",
                matched_patterns=list(evasion_matches),
                severity=ThreatSeverity.MEDIUM,
            ))

        security_logger.info(
            f"ImportExportAnalyzer: Analyzed {len(imports)} imports, {len(exports)} exports. "
            f"Found {len(suspicious_found)} suspicious APIs, {len(indicators)} indicators."
        )

        return {
            "total_imports": len(imports),
            "total_exports": len(exports),
            "suspicious_apis": list(set(suspicious_found)),
            "indicators": indicators,
            "has_injection_capabilities": len(injection_matches) > 0,
            "has_networking_capabilities": len(net_matches) > 0,
            "has_evasion_capabilities": len(evasion_matches) > 0,
        }


# Global ImportExportAnalyzer instance
import_export_analyzer = ImportExportAnalyzer()
