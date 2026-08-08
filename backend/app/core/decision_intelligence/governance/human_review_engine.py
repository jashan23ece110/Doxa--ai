"""
Enterprise Human Decision Review Engine.

Manages human approval requests, evidence presentation, reviewer assignments, and approval workflows.
"""

import threading
import time
from typing import Dict, Any, Optional
from app.core.logging import security_logger
from app.core.decision_intelligence.governance.explainability_types import ApprovalRequest, ApprovalDecision, HumanReview


class HumanReviewEngine:
    """Thread-safe Enterprise Human Decision Review Engine."""

    def __init__(self):
        self._lock = threading.Lock()
        self._reviews: Dict[str, HumanReview] = {}

    def create_approval_request(self, decision_id: str, action_title: str, estimated_cost: float = 15000.0) -> ApprovalRequest:
        """Creates a pending human approval request."""
        areq = ApprovalRequest(decision_id=decision_id, action_title=action_title, estimated_cost=estimated_cost, status="PENDING_APPROVAL")
        hrev = HumanReview(approval_request=areq)
        with self._lock:
            self._reviews[areq.approval_request_id] = hrev
            security_logger.info(f"HumanReviewEngine: Created approval request '{areq.approval_request_id}' for action '{action_title}'.")
        return areq

    def submit_approval_decision(self, approval_request_id: str, approver_id: str, decision: str = "APPROVED") -> ApprovalDecision:
        """Submits human approval or rejection decision."""
        adec = ApprovalDecision(approval_request_id=approval_request_id, approver_id=approver_id, decision=decision)
        with self._lock:
            if approval_request_id in self._reviews:
                hrev = self._reviews[approval_request_id]
                hrev.approval_request.status = decision
                hrev.decision = adec
                security_logger.info(f"HumanReviewEngine: Recorded human approval decision '{decision}' by approver '{approver_id}'.")
        return adec


# Global HumanReviewEngine instance
human_review_engine = HumanReviewEngine()
