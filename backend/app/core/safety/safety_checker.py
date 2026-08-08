"""
Enterprise AI Safety Checker.

Detects unsafe tool chains, dangerous execution sequences, prompt injection,
RAG poisoning, malicious memory injection, tool abuse, recursive loops,
privilege escalation, and agent misuse.
"""

import asyncio
import re
import time
from typing import Dict, Any, List
from app.core.logging import logger
from app.core.config import settings
from app.core.safety.safety_types import (
    ExecutionRisk,
    RiskAssessment,
    RiskLevel,
)


class SafetyChecker:
    """Detects unsafe patterns and attack vectors in AI executions."""

    # ── Prompt Injection Patterns ──
    _INJECTION_PATTERNS: List[re.Pattern] = [
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
        re.compile(r"ignore\s+(all\s+)?above\s+instructions", re.IGNORECASE),
        re.compile(r"disregard\s+(all\s+)?prior\s+(instructions|context)", re.IGNORECASE),
        re.compile(r"you\s+are\s+now\s+(a|an|the)\s+", re.IGNORECASE),
        re.compile(r"forget\s+(everything|all|your\s+instructions)", re.IGNORECASE),
        re.compile(r"system\s*:\s*you\s+are", re.IGNORECASE),
        re.compile(r"<\s*/?system\s*>", re.IGNORECASE),
        re.compile(r"\[\s*INST\s*\]", re.IGNORECASE),
        re.compile(r"act\s+as\s+(if\s+)?(you\s+are|a)", re.IGNORECASE),
        re.compile(r"override\s+(your\s+)?(safety|system|rules)", re.IGNORECASE),
        re.compile(r"jailbreak", re.IGNORECASE),
        re.compile(r"DAN\s*mode", re.IGNORECASE),
    ]

    # ── Dangerous Tool Chain Patterns ──
    _DANGEROUS_TOOL_SEQUENCES: List[List[str]] = [
        ["file_read", "shell_execute"],
        ["memory_read", "external_api"],
        ["credential_read", "http_request"],
        ["database_query", "file_write"],
        ["shell_execute", "shell_execute", "shell_execute"],
        ["file_write", "shell_execute"],
    ]

    # ── Dangerous Tool Names ──
    _DANGEROUS_TOOLS: List[str] = [
        "shell_execute", "system_command", "os_exec", "raw_sql",
        "eval", "exec", "subprocess_run", "credential_dump",
    ]

    # ── RAG Poisoning Patterns ──
    _RAG_POISONING_PATTERNS: List[re.Pattern] = [
        re.compile(r"<script[^>]*>", re.IGNORECASE),
        re.compile(r"javascript\s*:", re.IGNORECASE),
        re.compile(r"data\s*:\s*text/html", re.IGNORECASE),
        re.compile(r"on(error|load|click)\s*=", re.IGNORECASE),
        re.compile(r"\\x[0-9a-fA-F]{2}", re.IGNORECASE),
        re.compile(r"base64\s*,\s*[A-Za-z0-9+/=]{50,}", re.IGNORECASE),
    ]

    async def assess_risk(
        self,
        context: Dict[str, Any] = None,
    ) -> RiskAssessment:
        """
        Performs comprehensive risk assessment on an execution context.

        Args:
            context: Dict containing:
                - prompt (str): User prompt text.
                - tool_chain (List[str]): Sequence of tool names to be executed.
                - memory_updates (List[dict]): Proposed memory writes.
                - retrieval_texts (List[str]): Retrieved document chunks.
                - agent_count (int): Current number of active agents.
                - recursion_depth (int): Current recursive call depth.
                - user_role (str): Role of the requesting user.
                - requested_tools (List[str]): Tools requested in this execution.

        Returns:
            RiskAssessment with individual risks and overall score.
        """
        if not settings.SAFETY_CHECKER_ENABLED:
            return RiskAssessment(is_acceptable=True)

        start = time.time()
        ctx = context or {}
        risks: List[ExecutionRisk] = []

        # 1. Prompt Injection Detection
        prompt = ctx.get("prompt", "")
        injection_risk = self._check_prompt_injection(prompt)
        if injection_risk:
            risks.append(injection_risk)

        # 2. Dangerous Tool Chain Detection
        tool_chain = ctx.get("tool_chain", [])
        chain_risk = self._check_tool_chain(tool_chain)
        if chain_risk:
            risks.append(chain_risk)

        # 3. Dangerous Individual Tools
        requested_tools = ctx.get("requested_tools", [])
        for tool_risk in self._check_dangerous_tools(requested_tools, ctx.get("user_role", "")):
            risks.append(tool_risk)

        # 4. RAG Poisoning Detection
        retrieval_texts = ctx.get("retrieval_texts", [])
        for poisoning_risk in self._check_rag_poisoning(retrieval_texts):
            risks.append(poisoning_risk)

        # 5. Memory Injection Detection
        memory_updates = ctx.get("memory_updates", [])
        mem_risk = self._check_memory_injection(memory_updates)
        if mem_risk:
            risks.append(mem_risk)

        # 6. Recursive Loop Detection
        recursion_depth = ctx.get("recursion_depth", 0)
        if recursion_depth > 10:
            risks.append(ExecutionRisk(
                category="recursive_loop",
                risk_score=min(1.0, recursion_depth / 20),
                risk_level=RiskLevel.HIGH if recursion_depth > 15 else RiskLevel.MEDIUM,
                description=f"Excessive recursion depth detected: {recursion_depth}",
                affected_components=["execution_engine", "agent_runtime"],
                mitigation="Terminate recursive execution and return partial result.",
            ))

        # 7. Privilege Escalation Detection
        priv_risk = self._check_privilege_escalation(ctx)
        if priv_risk:
            risks.append(priv_risk)

        # 8. Agent Misuse Detection
        agent_count = ctx.get("agent_count", 0)
        if agent_count > settings.MAX_ACTIVE_AGENTS:
            risks.append(ExecutionRisk(
                category="agent_misuse",
                risk_score=min(1.0, agent_count / (settings.MAX_ACTIVE_AGENTS * 2)),
                risk_level=RiskLevel.HIGH,
                description=f"Agent count ({agent_count}) exceeds maximum ({settings.MAX_ACTIVE_AGENTS}).",
                affected_components=["agent_runtime", "multi_agent"],
                mitigation="Deny new agent creation until existing agents complete.",
            ))

        # 9. Tool Abuse (excessive invocations)
        tool_count = ctx.get("tool_invocations_in_session", 0)
        if tool_count > 50:
            risks.append(ExecutionRisk(
                category="tool_abuse",
                risk_score=min(1.0, tool_count / 100),
                risk_level=RiskLevel.MEDIUM if tool_count <= 75 else RiskLevel.HIGH,
                description=f"Excessive tool invocations in session: {tool_count}.",
                affected_components=["tool_registry"],
                mitigation="Rate-limit tool invocations for this session.",
            ))

        # ── Compute Overall Risk ──
        if risks:
            max_score = max(r.risk_score for r in risks)
            avg_score = sum(r.risk_score for r in risks) / len(risks)
            overall = round((max_score * 0.6) + (avg_score * 0.4), 4)
        else:
            overall = 0.0

        overall_level = self._score_to_level(overall)
        is_acceptable = overall <= settings.RISK_THRESHOLD
        requires_review = any(r.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL) for r in risks)

        elapsed = (time.time() - start) * 1000

        assessment = RiskAssessment(
            overall_risk_score=overall,
            overall_risk_level=overall_level,
            individual_risks=risks,
            is_acceptable=is_acceptable,
            requires_human_review=requires_review,
            assessment_duration_ms=round(elapsed, 2),
        )

        logger.info(
            f"SafetyChecker assessed '{assessment.assessment_id}': "
            f"Risks={len(risks)}, Overall={overall:.4f}, Level={overall_level.value}, "
            f"Acceptable={is_acceptable}, Duration={elapsed:.2f}ms"
        )
        return assessment

    # ── Detection Methods ──

    def _check_prompt_injection(self, prompt: str) -> ExecutionRisk | None:
        """Checks for prompt injection patterns."""
        if not prompt:
            return None
        matches = []
        for pattern in self._INJECTION_PATTERNS:
            if pattern.search(prompt):
                matches.append(pattern.pattern)
        if matches:
            return ExecutionRisk(
                category="prompt_injection",
                risk_score=min(1.0, 0.5 + (len(matches) * 0.15)),
                risk_level=RiskLevel.CRITICAL if len(matches) >= 3 else RiskLevel.HIGH,
                description=f"Detected {len(matches)} prompt injection pattern(s).",
                affected_components=["llm_gateway", "prompt_engine"],
                mitigation="Sanitize prompt, alert security team, log attempt.",
            )
        return None

    def _check_tool_chain(self, tool_chain: List[str]) -> ExecutionRisk | None:
        """Checks for dangerous tool chain sequences."""
        if len(tool_chain) < 2:
            return None
        for dangerous_seq in self._DANGEROUS_TOOL_SEQUENCES:
            seq_len = len(dangerous_seq)
            for i in range(len(tool_chain) - seq_len + 1):
                window = tool_chain[i:i + seq_len]
                if window == dangerous_seq:
                    return ExecutionRisk(
                        category="tool_chain",
                        risk_score=0.85,
                        risk_level=RiskLevel.HIGH,
                        description=f"Dangerous tool chain detected: {' → '.join(dangerous_seq)}.",
                        affected_components=["tool_registry", "execution_engine"],
                        mitigation="Block tool chain execution, require explicit approval.",
                    )
        return None

    def _check_dangerous_tools(self, tools: List[str], user_role: str) -> List[ExecutionRisk]:
        """Checks for individually dangerous tool invocations."""
        risks: List[ExecutionRisk] = []
        for tool in tools:
            if tool.lower() in self._DANGEROUS_TOOLS:
                if user_role.lower() != "admin":
                    risks.append(ExecutionRisk(
                        category="dangerous_tool",
                        risk_score=0.9,
                        risk_level=RiskLevel.CRITICAL,
                        description=f"Dangerous tool '{tool}' requested by non-admin user.",
                        affected_components=["tool_registry"],
                        mitigation=f"Deny '{tool}' execution for role '{user_role}'.",
                    ))
        return risks

    def _check_rag_poisoning(self, texts: List[str]) -> List[ExecutionRisk]:
        """Checks retrieved texts for RAG poisoning patterns."""
        risks: List[ExecutionRisk] = []
        for i, text in enumerate(texts):
            for pattern in self._RAG_POISONING_PATTERNS:
                if pattern.search(text):
                    risks.append(ExecutionRisk(
                        category="rag_poisoning",
                        risk_score=0.8,
                        risk_level=RiskLevel.HIGH,
                        description=f"RAG poisoning pattern detected in chunk {i}.",
                        affected_components=["rag_engine", "retrieval"],
                        mitigation="Quarantine poisoned chunk, re-index document.",
                    ))
                    break  # one risk per chunk is sufficient
        return risks

    def _check_memory_injection(self, memory_updates: List[Dict[str, Any]]) -> ExecutionRisk | None:
        """Checks for malicious memory injection attempts."""
        if not memory_updates:
            return None
        suspicious_count = 0
        for update in memory_updates:
            content = str(update.get("content", ""))
            # Check for injection in memory content
            for pattern in self._INJECTION_PATTERNS[:6]:
                if pattern.search(content):
                    suspicious_count += 1
                    break
        if suspicious_count > 0:
            return ExecutionRisk(
                category="memory_injection",
                risk_score=min(1.0, 0.6 + (suspicious_count * 0.1)),
                risk_level=RiskLevel.HIGH,
                description=f"Detected {suspicious_count} suspicious memory write(s).",
                affected_components=["memory_engine", "working_memory"],
                mitigation="Block memory writes, log injection attempt.",
            )
        return None

    def _check_privilege_escalation(self, ctx: Dict[str, Any]) -> ExecutionRisk | None:
        """Checks for privilege escalation patterns."""
        user_role = ctx.get("user_role", "viewer").lower()
        requested_action = ctx.get("requested_action", "").lower()
        elevated_actions = [
            "admin_override", "role_change", "tenant_switch",
            "security_disable", "policy_bypass", "config_write",
        ]
        if user_role != "admin" and requested_action in elevated_actions:
            return ExecutionRisk(
                category="privilege_escalation",
                risk_score=0.95,
                risk_level=RiskLevel.CRITICAL,
                description=f"Privilege escalation attempt: '{requested_action}' by role '{user_role}'.",
                affected_components=["rbac", "security"],
                mitigation="Deny action, alert security team, log attempt.",
            )
        return None

    @staticmethod
    def _score_to_level(score: float) -> RiskLevel:
        """Converts numeric risk score to risk level."""
        if score >= 0.8:
            return RiskLevel.CRITICAL
        elif score >= 0.6:
            return RiskLevel.HIGH
        elif score >= 0.4:
            return RiskLevel.MEDIUM
        elif score >= 0.1:
            return RiskLevel.LOW
        return RiskLevel.NONE


# Global SafetyChecker instance
safety_checker = SafetyChecker()
