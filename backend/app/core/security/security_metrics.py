"""
Security Metrics Tracker for Enterprise Zero-Trust Security Platform.

Tracks failed logins, denied requests, policy violations, tenant violations, audit volume,
secret rotations, and RBAC cache hit ratio.
"""

import threading
from typing import Dict, Any


class SecurityMetricsTracker:
    """Thread-safe metrics tracker for security events and RBAC operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self.failed_logins_count: int = 0
        self.denied_requests_count: int = 0
        self.policy_violations_count: int = 0
        self.tenant_violations_count: int = 0
        self.audit_records_count: int = 0
        self.secret_rotations_count: int = 0
        self.rbac_cache_hits: int = 0
        self.rbac_cache_misses: int = 0
        # Security Research Telemetry
        self.scans_executed: int = 0
        self.binaries_analyzed: int = 0
        self.total_analysis_time_ms: float = 0.0
        self.ioc_detections: int = 0
        self.malware_detections: int = 0
        self.total_report_latency_ms: float = 0.0
        self.reports_generated_count: int = 0
        self.active_sessions: int = 0

    def record_scan(self, duration_ms: float) -> None:
        """Records a completed security scan."""
        with self._lock:
            self.scans_executed += 1
            self.total_analysis_time_ms += duration_ms

    def record_binary_analysis(self, is_malicious: bool = False, ioc_count: int = 0) -> None:
        """Records binary analysis outcome."""
        with self._lock:
            self.binaries_analyzed += 1
            if is_malicious:
                self.malware_detections += 1
            self.ioc_detections += ioc_count

    def record_report_generated(self, latency_ms: float) -> None:
        """Records threat report generation latency."""
        with self._lock:
            self.reports_generated_count += 1
            self.total_report_latency_ms += latency_ms

    def set_active_sessions(self, count: int) -> None:
        """Updates active RE session count."""
        with self._lock:
            self.active_sessions = count

    def record_denied_request(self) -> None:
        """Records an access denied event."""
        with self._lock:
            self.denied_requests_count += 1

    def record_audit(self) -> None:
        """Records an audit log entry."""
        with self._lock:
            self.audit_records_count += 1

    def record_secret_rotation(self) -> None:
        """Records a secret rotation event."""
        with self._lock:
            self.secret_rotations_count += 1

    def record_rbac_cache(self, hit: bool) -> None:
        """Records RBAC cache hit/miss."""
        with self._lock:
            if hit:
                self.rbac_cache_hits += 1
            else:
                self.rbac_cache_misses += 1

    def get_summary(self) -> Dict[str, Any]:
        """Returns summary statistics across security operations."""
        with self._lock:
            tot_rbac = self.rbac_cache_hits + self.rbac_cache_misses
            ratio = round(self.rbac_cache_hits / tot_rbac, 2) if tot_rbac > 0 else 1.0
            avg_analysis_ms = round(self.total_analysis_time_ms / max(self.scans_executed, 1), 2)
            avg_report_lat = round(self.total_report_latency_ms / max(self.reports_generated_count, 1), 2)

            return {
                "failed_logins": self.failed_logins_count,
                "denied_requests": self.denied_requests_count,
                "policy_violations": self.policy_violations_count,
                "tenant_violations": self.tenant_violations_count,
                "audit_volume": self.audit_records_count,
                "secret_rotations": self.secret_rotations_count,
                "rbac_cache_hit_ratio": ratio,
                "scans_executed": self.scans_executed,
                "binaries_analyzed": self.binaries_analyzed,
                "average_analysis_time_ms": avg_analysis_ms,
                "ioc_detections": self.ioc_detections,
                "malware_detections": self.malware_detections,
                "report_generation_latency_ms": avg_report_lat,
                "active_sessions": self.active_sessions,
            }


# Global SecurityMetricsTracker instance
security_metrics_tracker = SecurityMetricsTracker()
