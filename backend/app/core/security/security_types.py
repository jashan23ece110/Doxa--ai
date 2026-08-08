"""
Enterprise Security Research & Reverse Engineering Types.

Defines Pydantic data models for binary analysis, malware research, threat intelligence,
vulnerability findings, forensics, reverse engineering sessions, and security metrics.
"""

import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class Architecture(str, Enum):
    X86 = "x86"
    X64 = "x64"
    ARM = "arm"
    ARM64 = "arm64"
    MIPS = "mips"
    RISCV = "riscv"
    UNKNOWN = "unknown"


class FileFormat(str, Enum):
    ELF = "elf"
    PE = "pe"
    MACHO = "macho"
    DEX = "dex"
    JAVA_BYTECODE = "java_bytecode"
    RAW_BINARY = "raw_binary"
    UNKNOWN = "unknown"


class ThreatSeverity(str, Enum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class BinarySection(BaseModel):
    name: str
    virtual_address: int = 0
    virtual_size: int = 0
    raw_size: int = 0
    entropy: float = 0.0
    is_executable: bool = False
    is_readable: bool = True
    is_writable: bool = False
    md5: str = ""


class BinaryImport(BaseModel):
    library: str
    function_name: str
    ordinal: Optional[int] = None
    address: Optional[int] = None


class BinaryExport(BaseModel):
    function_name: str
    ordinal: Optional[int] = None
    address: int = 0


class BinarySymbol(BaseModel):
    name: str
    address: int = 0
    size: int = 0
    symbol_type: str = "function"


class BinaryInstruction(BaseModel):
    address: int
    mnemonic: str
    op_str: str = ""
    bytes_hex: str = ""
    size: int = 0


class BinaryFunction(BaseModel):
    function_id: str = Field(default_factory=lambda: f"func_{uuid.uuid4().hex[:8]}")
    name: str
    start_address: int
    end_address: int
    size_bytes: int = 0
    cyclomatic_complexity: int = 1
    instructions_count: int = 0
    calls: List[str] = Field(default_factory=list)
    called_by: List[str] = Field(default_factory=list)
    basic_blocks_count: int = 1
    decompiled_c: Optional[str] = None


class BinaryString(BaseModel):
    string_value: str
    offset: int = 0
    encoding: str = "ascii"
    category: str = "general"  # url, ip, file_path, registry_key, crypto, general


class FileFingerprint(BaseModel):
    md5: str
    sha1: str
    sha256: str
    ssdeep: Optional[str] = None
    tlsh: Optional[str] = None
    impash: Optional[str] = None
    rich_header_hash: Optional[str] = None
    file_size_bytes: int = 0
    file_type_magic: str = ""


class BinaryMetadata(BaseModel):
    binary_id: str = Field(default_factory=lambda: f"bin_{uuid.uuid4().hex[:8]}")
    file_name: str
    fingerprint: FileFingerprint
    format: FileFormat = FileFormat.UNKNOWN
    architecture: Architecture = Architecture.UNKNOWN
    entry_point: int = 0
    is_packed: bool = False
    packer_name: Optional[str] = None
    compiler: Optional[str] = None
    sections: List[BinarySection] = Field(default_factory=list)
    imports: List[BinaryImport] = Field(default_factory=list)
    exports: List[BinaryExport] = Field(default_factory=list)
    symbols: List[BinarySymbol] = Field(default_factory=list)
    subsystem: str = "unknown"
    created_at: float = Field(default_factory=time.time)


class MalwareSample(BaseModel):
    sample_id: str = Field(default_factory=lambda: f"mal_{uuid.uuid4().hex[:8]}")
    metadata: BinaryMetadata
    first_seen: float = Field(default_factory=time.time)
    threat_family: str = "unknown"
    is_malicious: bool = False
    confidence_score: float = 0.0
    tags: List[str] = Field(default_factory=list)


class IOC(BaseModel):
    ioc_id: str = Field(default_factory=lambda: f"ioc_{uuid.uuid4().hex[:8]}")
    ioc_type: str  # ip, domain, md5, sha256, url, registry_key, mutex, file_path
    value: str
    severity: ThreatSeverity = ThreatSeverity.MEDIUM
    description: str = ""
    first_detected: float = Field(default_factory=time.time)
    source: str = "internal_analysis"


class ThreatIndicator(BaseModel):
    indicator_id: str = Field(default_factory=lambda: f"ind_{uuid.uuid4().hex[:8]}")
    name: str
    category: str  # evasion, persistence, privilege_escalation, credential_access, exfiltration
    mitre_attack_id: Optional[str] = None
    description: str = ""
    matched_patterns: List[str] = Field(default_factory=list)
    severity: ThreatSeverity = ThreatSeverity.MEDIUM


class ThreatActorProfile(BaseModel):
    actor_id: str = Field(default_factory=lambda: f"actor_{uuid.uuid4().hex[:8]}")
    name: str
    aliases: List[str] = Field(default_factory=list)
    target_sectors: List[str] = Field(default_factory=list)
    associated_iocs: List[str] = Field(default_factory=list)
    known_tools: List[str] = Field(default_factory=list)
    motivation: str = "unknown"


class SecurityFinding(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"find_{uuid.uuid4().hex[:8]}")
    title: str
    category: str
    severity: ThreatSeverity = ThreatSeverity.MEDIUM
    description: str
    remediation: Optional[str] = None
    location: Optional[str] = None


class VulnerabilityFinding(BaseModel):
    vuln_id: str = Field(default_factory=lambda: f"vuln_{uuid.uuid4().hex[:8]}")
    cve_id: Optional[str] = None
    title: str
    cvss_score: float = 0.0
    severity: ThreatSeverity = ThreatSeverity.MEDIUM
    description: str
    affected_component: str = ""
    remediation_guidance: str = ""


class StaticAnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"sa_{uuid.uuid4().hex[:8]}")
    binary_id: str
    fingerprint: FileFingerprint
    sections_count: int = 0
    imports_count: int = 0
    exports_count: int = 0
    extracted_strings_count: int = 0
    functions_analyzed_count: int = 0
    suspicious_imports: List[str] = Field(default_factory=list)
    indicators: List[ThreatIndicator] = Field(default_factory=list)
    risk_score: float = 0.0
    completed_at: float = Field(default_factory=time.time)


class SandboxResult(BaseModel):
    sandbox_id: str = Field(default_factory=lambda: f"sbx_{uuid.uuid4().hex[:8]}")
    execution_time_seconds: float = 0.0
    process_tree: List[Dict[str, Any]] = Field(default_factory=list)
    file_activity: List[str] = Field(default_factory=list)
    registry_activity: List[str] = Field(default_factory=list)
    network_connections: List[str] = Field(default_factory=list)
    dns_queries: List[str] = Field(default_factory=list)
    behavioral_score: float = 0.0


class DynamicAnalysisResult(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"da_{uuid.uuid4().hex[:8]}")
    binary_id: str
    sandbox_result: Optional[SandboxResult] = None
    api_calls_logged: int = 0
    network_activity_detected: bool = False
    persistence_mechanisms: List[str] = Field(default_factory=list)
    behavioral_indicators: List[ThreatIndicator] = Field(default_factory=list)
    completed_at: float = Field(default_factory=time.time)


class RiskAssessment(BaseModel):
    assessment_id: str = Field(default_factory=lambda: f"ra_{uuid.uuid4().hex[:8]}")
    overall_risk_score: float = 0.0  # 0.0 to 10.0
    threat_level: ThreatSeverity = ThreatSeverity.INFORMATIONAL
    is_malicious: bool = False
    confidence: float = 0.0
    mitre_techniques: List[str] = Field(default_factory=list)
    key_findings: List[str] = Field(default_factory=list)
    evaluated_at: float = Field(default_factory=time.time)


class ForensicArtifact(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:8]}")
    artifact_type: str  # memory_dump, pcap, registry_hive, disk_image, system_log
    source: str
    file_path: Optional[str] = None
    size_bytes: int = 0
    checksum: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    extracted_at: float = Field(default_factory=time.time)


class AttackSimulation(BaseModel):
    sim_id: str = Field(default_factory=lambda: f"sim_{uuid.uuid4().hex[:8]}")
    name: str
    technique_id: str
    target_scope: str = "sandbox"
    status: AnalysisStatus = AnalysisStatus.PENDING
    results_summary: str = ""
    executed_at: float = Field(default_factory=time.time)


class DetectionRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: f"rule_{uuid.uuid4().hex[:8]}")
    name: str
    rule_type: str  # yara, sigma, snort, custom
    content: str
    severity: ThreatSeverity = ThreatSeverity.MEDIUM
    author: str = "doxa_security"
    enabled: bool = True


class ThreatReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex[:8]}")
    title: str
    binary_id: Optional[str] = None
    risk_assessment: Optional[RiskAssessment] = None
    static_analysis: Optional[StaticAnalysisResult] = None
    dynamic_analysis: Optional[DynamicAnalysisResult] = None
    iocs: List[IOC] = Field(default_factory=list)
    vulnerabilities: List[VulnerabilityFinding] = Field(default_factory=list)
    summary: str = ""
    remediation_steps: List[str] = Field(default_factory=list)
    generated_at: float = Field(default_factory=time.time)


class ReverseEngineeringSession(BaseModel):
    session_id: str = Field(default_factory=lambda: f"re_sess_{uuid.uuid4().hex[:8]}")
    binary_id: str
    status: AnalysisStatus = AnalysisStatus.RUNNING
    functions: List[BinaryFunction] = Field(default_factory=list)
    strings: List[BinaryString] = Field(default_factory=list)
    findings: List[SecurityFinding] = Field(default_factory=list)
    active_disassembly_address: Optional[int] = None
    started_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class SecurityMetrics(BaseModel):
    scans_executed: int = 0
    binaries_analyzed: int = 0
    average_analysis_time_ms: float = 0.0
    ioc_detections: int = 0
    malware_detections: int = 0
    cache_hit_ratio: float = 0.0
    report_generation_latency_ms: float = 0.0
    active_sessions: int = 0
    updated_at: float = Field(default_factory=time.time)


class SecurityDashboardState(BaseModel):
    metrics: SecurityMetrics = Field(default_factory=SecurityMetrics)
    recent_reports: List[ThreatReport] = Field(default_factory=list)
    recent_iocs: List[IOC] = Field(default_factory=list)
    active_sessions_count: int = 0
    system_health: str = "healthy"
