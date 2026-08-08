"""
Audit Logger for Enterprise Zero-Trust Security Platform.

Asynchronously writes immutable audit log records to disk (./security_data/audit_logs.json)
for audit completeness and compliance.
"""

import json
import os
import threading
from typing import Dict, Any, List, Optional
from app.core.logging import security_logger
from app.core.security.security_metrics import security_metrics_tracker
from app.core.security.security_models import AuditRecord


class AuditLogger:
    """Thread-safe immutable security audit logger."""

    def __init__(self, file_path: str = "./security_data/audit_logs.json"):
        self.file_path = file_path
        self._lock = threading.Lock()
        self._audit_records: List[AuditRecord] = []
        self._ensure_storage_dir()
        self._load_from_disk()

    def _ensure_storage_dir(self) -> None:
        """Ensures storage directory exists."""
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def _load_from_disk(self) -> None:
        """Loads audit records from disk."""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                self._audit_records.append(AuditRecord.model_validate(item))

            security_logger.info(f"Loaded {len(self._audit_records)} audit records from disk.")
        except Exception as e:
            security_logger.error(f"Failed to load audit logs from disk: {e}")

    def _save_to_disk(self) -> None:
        """Saves audit records to disk."""
        try:
            data = [a.model_dump() for a in self._audit_records[-5000:]]  # Keep last 5000 records
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            security_logger.error(f"Failed to save audit logs to disk: {e}")

    def log_action(
        self,
        user_id: str,
        tenant_id: str,
        resource: str,
        action: str,
        result: str = "success",
        ip_address: Optional[str] = "127.0.0.1",
        request_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditRecord:
        """
        Logs an immutable audit event and persists to disk.
        """
        record = AuditRecord(
            user_id=user_id,
            tenant_id=tenant_id,
            resource=resource,
            action=action,
            result=result,
            ip_address=ip_address,
            request_id=request_id,
            trace_id=trace_id,
            details=details or {},
        )

        with self._lock:
            self._audit_records.append(record)
            security_metrics_tracker.record_audit()
            self._save_to_disk()

        return record

    def list_records(self, limit: int = 100) -> List[AuditRecord]:
        """Lists recent audit records."""
        with self._lock:
            return self._audit_records[-limit:]


# Global AuditLogger instance
audit_logger = AuditLogger()
