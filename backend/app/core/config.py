"""
Centralized Configuration Module for Doxa Backend.

Loads environment variables, default model names, timeout limits,
security parameters, resource protection caps, environment profiles, paths, and RAG/Memory/Context/Reasoning/Eval/Multi-Agent settings.
"""

import os
import time
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings:
    """Application settings, resource limits, and environment profile configuration."""

    # Process Start Timestamp
    PROCESS_START_TIME: float = time.time()

    # Environment Profile
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()
    APP_NAME: str = "Doxa AI Platform Backend"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false" if ENVIRONMENT == "production" else "true").lower() in ("true", "1", "t")

    # TokenRouter / LLM Settings
    TOKENROUTER_API_KEY: str = os.getenv("TOKENROUTER_API_KEY", "")
    TOKENROUTER_BASE_URL: str = os.getenv("TOKENROUTER_BASE_URL", "https://api.tokenrouter.com/v1")
    DEFAULT_MODEL: str = os.getenv("TOKENROUTER_MODEL", "moonshotai/kimi-k3-free")
    DEFAULT_EVAL_MODEL_1: str = "moonshotai/kimi-k3-free"
    DEFAULT_EVAL_MODEL_2: str = "moonshotai/kimi-k3-free"
    
    LLM_MAX_RETRIES: int = 3
    LLM_RETRY_DELAY: float = 2.0
    LLM_TEMPERATURE: float = 0.1
    AGENT_MAX_ITERATIONS: int = 8
    LLM_TIMEOUT_SECONDS: float = 45.0

    # Resource Limits & Security Protection Caps
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB limit for file uploads
    MAX_REQUEST_BODY_SIZE: int = 2 * 1024 * 1024   # 2 MB limit for standard JSON body
    MAX_DOCUMENT_COUNT: int = 100                   # Max stored documents allowed
    MAX_TIMER_DURATION_SECONDS: int = 86400         # 24 hours max timer duration
    MAX_SEARCH_QUERY_LENGTH: int = 300              # Max length of search query
    MAX_PYTHON_CODE_LENGTH: int = 4000              # Max length of Python sandbox script
    MAX_CALCULATOR_EXPRESSION_LENGTH: int = 500     # Max length of math expression
    MAX_SSE_STREAM_LIFETIME_SECONDS: int = 300      # 5 minutes max streaming duration
    HTTP_TIMEOUT_SECONDS: float = 30.0

    # Allowed Document File Types
    ALLOWED_EXTENSIONS: List[str] = [".txt", ".pdf"]
    ALLOWED_MIME_TYPES: List[str] = ["text/plain", "application/pdf"]

    # Vector Storage & Hybrid RAG Settings
    CHROMA_PERSIST_DIR: str = os.getenv(
        "CHROMA_PERSIST_DIR",
        str(BASE_DIR / "chroma_data")
    )
    BM25_INDEX_PATH: str = os.getenv(
        "BM25_INDEX_PATH",
        str(BASE_DIR / "chroma_data" / "bm25_index.json")
    )
    MEMORY_STORE_PATH: str = os.getenv(
        "MEMORY_STORE_PATH",
        str(BASE_DIR / "chroma_data" / "memory_store.json")
    )
    EVAL_STORE_PATH: str = os.getenv(
        "EVAL_STORE_PATH",
        str(BASE_DIR / "chroma_data" / "eval_metrics.json")
    )
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    RAG_DEFAULT_CHUNK_SIZE: int = 500
    RAG_DEFAULT_OVERLAP: int = 50
    RAG_DEFAULT_TOP_K: int = 3
    RAG_DENSE_TOP_K: int = 5
    RAG_BM25_TOP_K: int = 5
    RAG_RRF_K: int = 60
    HYBRID_RETRIEVAL_ENABLED: bool = True

    # Cross-Encoder Reranker Settings
    RERANK_ENABLED: bool = True
    RERANK_MODEL: str = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    RERANK_TOP_K: int = 3
    RERANK_MAX_CANDIDATES: int = 20
    RERANK_BATCH_SIZE: int = 16
    RERANK_THRESHOLD: float = 0.0

    # Intelligent Query Processing Settings
    QUERY_PROCESSING_ENABLED: bool = True
    QUERY_REWRITE_ENABLED: bool = True
    HYDE_ENABLED: bool = True
    MULTI_QUERY_ENABLED: bool = True
    SELF_QUERY_ENABLED: bool = True
    QUERY_EXPANSION_ENABLED: bool = True
    MAX_GENERATED_QUERIES: int = 3
    MAX_HYDE_TOKENS: int = 150

    # Multi-Layer Enterprise Memory Architecture Settings
    MEMORY_ENABLED: bool = True
    SESSION_MEMORY_ENABLED: bool = True
    LONG_TERM_MEMORY_ENABLED: bool = True
    EPISODIC_MEMORY_ENABLED: bool = True
    MEMORY_ENGINE_ENABLED: bool = True
    MEMORY_CONSOLIDATION: bool = True
    MEMORY_GRAPH_ENABLED: bool = True
    MEMORY_COMPRESSION: bool = True
    MEMORY_ANALYTICS: bool = True
    MAX_SHORT_TERM_MEMORY: int = 200
    MAX_LONG_TERM_MEMORY: int = 50000
    MEMORY_IMPORTANCE_THRESHOLD: float = 0.35
    MAX_MEMORY_RESULTS: int = 5
    MEMORY_TTL_DAYS: int = 30


    # Enterprise Context Engineering Settings
    CONTEXT_ENGINE_ENABLED: bool = True
    TOKEN_BUDGET_ENABLED: bool = True
    MAX_CONTEXT_TOKENS: int = 8000
    MAX_RETRIEVAL_TOKENS: int = 2500
    MAX_MEMORY_TOKENS: int = 1000
    MAX_HISTORY_TOKENS: int = 1500
    MAX_TOOL_TOKENS: int = 1000
    ENABLE_CONTEXT_COMPRESSION: bool = True
    ENABLE_CONTEXT_VALIDATION: bool = True

    # Enterprise Reasoning Engine Settings
    REASONING_ENGINE_ENABLED: bool = True
    REFLECTION_ENABLED: bool = True
    CONFIDENCE_ESTIMATION_ENABLED: bool = True
    HALLUCINATION_CHECK_ENABLED: bool = True
    MAX_REFLECTION_PASSES: int = 1
    ENABLE_EVIDENCE_VALIDATION: bool = True
    ENABLE_CONTRADICTION_CHECK: bool = True

    # Enterprise Evaluation Platform Settings
    EVALUATION_ENABLED: bool = True
    BENCHMARK_ENABLED: bool = True
    LATENCY_TRACKING_ENABLED: bool = True
    QUALITY_SCORING_ENABLED: bool = True
    REGRESSION_DETECTION_ENABLED: bool = True
    MAX_METRIC_HISTORY: int = 1000

    # Enterprise Continuous Learning Layer Settings
    LEARNING_ENABLED: bool = True
    PROMPT_OPTIMIZATION: bool = True
    RETRIEVAL_OPTIMIZATION: bool = True
    TOOL_LEARNING: bool = True
    KNOWLEDGE_EVOLUTION: bool = True
    AUTO_ANALYTICS: bool = True
    LEARNING_HISTORY_LIMIT: int = 5000

    # Enterprise Planning & Reasoning Engine Settings
    ADVANCED_PLANNING_ENABLED: bool = True
    HIERARCHICAL_PLANNER: bool = True
    DEPENDENCY_GRAPH_ENABLED: bool = True
    DYNAMIC_REPLANNING: bool = True
    REASONING_ENGINE: bool = True
    DECISION_ENGINE: bool = True
    EXECUTION_MONITOR: bool = True
    MAX_PLAN_DEPTH: int = 8
    MAX_PARALLEL_BRANCHES: int = 12
    PLAN_TIMEOUT_SECONDS: int = 900

    # Autonomous Workflow Execution Engine Settings
    WORKFLOW_ENGINE_ENABLED: bool = True
    CHECKPOINTS_ENABLED: bool = True
    ROLLBACK_ENABLED: bool = True
    APPROVAL_ENGINE_ENABLED: bool = True
    WORKFLOW_ANALYTICS: bool = True
    MAX_PARALLEL_WORKERS: int = 16
    MAX_WORKFLOW_DEPTH: int = 25
    WORKFLOW_TIMEOUT_SECONDS: int = 7200
    DEFAULT_RETRY_LIMIT: int = 3

    # Enterprise Long-Horizon Autonomous Mission Control Settings
    MISSION_ENGINE_ENABLED: bool = True
    MISSION_ANALYTICS: bool = True
    AUTO_REPLAN_ENABLED: bool = True
    GOAL_PRIORITY_ENGINE: bool = True
    MISSION_PERSISTENCE: bool = True
    MAX_ACTIVE_MISSIONS: int = 500
    MISSION_HISTORY_LIMIT: int = 10000
    MISSION_CHECK_INTERVAL: int = 60
    AUTO_SUMMARY_ENABLED: bool = True

    # Universal Integration & Model Context Protocol (MCP) Platform Settings
    INTEGRATION_ENGINE_ENABLED: bool = True
    MCP_ENABLED: bool = True
    CONNECTOR_DISCOVERY: bool = True
    CONNECTOR_SANDBOX: bool = True
    CONNECTOR_ANALYTICS: bool = True
    AUTO_HEALTH_CHECK: bool = True
    AUTO_TOKEN_REFRESH: bool = True
    MAX_CONNECTORS: int = 500
    DEFAULT_CONNECTOR_TIMEOUT: int = 60

    # Enterprise Zero-Trust Security Platform Settings
    RBAC_ENABLED: bool = True
    AUDIT_ENABLED: bool = True
    ZERO_TRUST_ENABLED: bool = True
    POLICY_ENGINE_ENABLED: bool = True
    TENANT_ISOLATION_ENABLED: bool = True
    SECRET_MANAGER_ENABLED: bool = True
    SECURITY_ANALYTICS_ENABLED: bool = True
    COMPLIANCE_ENABLED: bool = True

    # Enterprise Distributed Observability & Diagnostics Platform Settings
    OBSERVABILITY_ENABLED: bool = True
    TRACING_ENABLED: bool = True
    METRICS_ENABLED: bool = True
    ALERTING_ENABLED: bool = True
    HEALTH_MONITOR_ENABLED: bool = True
    AUTO_RECOVERY_ENABLED: bool = True
    PROFILER_ENABLED: bool = True
    CAPACITY_PLANNING_ENABLED: bool = True

    # Enterprise AI Operating System Runtime & Hyperscale Infrastructure Settings
    CLUSTER_ENABLED: bool = True
    BACKUP_ENABLED: bool = True
    DISASTER_RECOVERY_ENABLED: bool = True
    SERVICE_DISCOVERY_ENABLED: bool = True
    RUNTIME_ENABLED: bool = True
    AUTO_SCALING_ENABLED: bool = True
    RELEASE_MANAGER_ENABLED: bool = True
    SYSTEM_REPORTING_ENABLED: bool = True

    # Enterprise Meta-Cognitive Intelligence Layer Settings
    METACOGNITION_ENABLED: bool = True
    CONFIDENCE_ENGINE_ENABLED: bool = True
    REFLECTION_ENABLED: bool = True
    SELF_CRITIQUE_ENABLED: bool = True
    UNCERTAINTY_ENGINE_ENABLED: bool = True
    STRATEGY_SELECTION_ENABLED: bool = True

    # Enterprise Deliberative Reasoning Engine Settings
    TREE_OF_THOUGHTS_ENABLED: bool = True
    GRAPH_OF_THOUGHTS_ENABLED: bool = True
    HYPOTHESIS_ENGINE_ENABLED: bool = True
    COUNTERFACTUAL_ENABLED: bool = True
    CONSENSUS_REASONING_ENABLED: bool = True
    RECURSIVE_REASONING_ENABLED: bool = True
    REASONING_CACHE_ENABLED: bool = True

    # Enterprise Knowledge Intelligence Platform Settings
    KNOWLEDGE_ENGINE_ENABLED: bool = True
    RESEARCH_ENGINE_ENABLED: bool = True
    FACT_VERIFICATION_ENABLED: bool = True
    KNOWLEDGE_GRAPH_ENABLED: bool = True
    SOURCE_RELIABILITY_ENABLED: bool = True
    EVIDENCE_FUSION_ENABLED: bool = True
    KNOWLEDGE_CACHE_ENABLED: bool = True

    # Enterprise Decision Intelligence Platform Settings
    DECISION_ENGINE_ENABLED: bool = True
    STRATEGIC_PLANNING_ENABLED: bool = True
    RISK_ENGINE_ENABLED: bool = True
    SCENARIO_SIMULATION_ENABLED: bool = True
    RESOURCE_OPTIMIZATION_ENABLED: bool = True
    DECISION_MEMORY_ENABLED: bool = True
    OPPORTUNITY_DISCOVERY_ENABLED: bool = True

    # Enterprise Self-Optimization Platform Settings
    EVOLUTION_ENGINE_ENABLED: bool = True
    SELF_EVALUATION_ENABLED: bool = True
    OPTIMIZATION_ENGINE_ENABLED: bool = True
    ADAPTIVE_TUNING_ENABLED: bool = True
    EXPERIMENT_MANAGER_ENABLED: bool = True
    CAPABILITY_ANALYZER_ENABLED: bool = True
    PERFORMANCE_LEARNING_ENABLED: bool = True

    # Enterprise AI Safety, Governance & Trust Layer Settings
    SAFETY_ENABLED: bool = True
    TRUST_SCORING_ENABLED: bool = True
    AUDIT_ENABLED: bool = True
    POLICY_ENGINE_ENABLED: bool = True
    COMPLIANCE_ENABLED: bool = True
    EXPLAINABILITY_ENABLED: bool = True
    GOVERNANCE_ENABLED: bool = True
    SAFETY_CHECKER_ENABLED: bool = True
    MAX_AUDIT_HISTORY: int = 10000
    RISK_THRESHOLD: float = 0.7
    TRUST_THRESHOLD: float = 0.4

    # Unified Autonomous Intelligence Core & AI OS Kernel Settings
    INTELLIGENCE_CORE_ENABLED: bool = True
    ADAPTIVE_DECISION_ENABLED: bool = True
    GLOBAL_CONTEXT_MANAGER_ENABLED: bool = True
    INTELLIGENCE_SCHEDULER_ENABLED: bool = True
    EXECUTION_OPTIMIZER_ENABLED: bool = True
    PIPELINE_PROFILER_ENABLED: bool = True
    AUTONOMOUS_OPTIMIZER_ENABLED: bool = True
    KNOWLEDGE_FLOW_ENABLED: bool = True
    AI_OS_KERNEL_ENABLED: bool = True
    OPERATIONAL_DASHBOARD_ENABLED: bool = True













    # Enterprise Multi-Agent Operating System Settings
    MULTI_AGENT_ENABLED: bool = True
    MAX_ACTIVE_AGENTS: int = 16
    AGENT_TIMEOUT_SECONDS: int = 300
    SHARED_WORKSPACE_ENABLED: bool = True
    AGENT_HEARTBEAT_INTERVAL: int = 5
    AGENT_AUTO_RECOVERY: bool = True
    CONFLICT_RESOLUTION_ENABLED: bool = True
    AGENT_PARALLELISM: int = 8
    MAX_AGENT_COUNT: int = 16
    AGENT_TIMEOUT: float = 300.0
    ENABLE_PARALLEL_AGENTS: bool = True
    ENABLE_CRITIC_AGENT: bool = True
    ENABLE_RESEARCH_AGENT: bool = True
    ENABLE_EXECUTOR_AGENT: bool = True


    # Tavily Web Search Settings
    TAVILY_API_KEY: Optional[str] = os.getenv("TAVILY_API_KEY")
    TAVILY_MAX_RESULTS: int = 3

    # Google OAuth / Calendar Settings
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth2callback")
    TOKEN_FILE_PATH: str = str(BASE_DIR / "token.json")

    # Python Sandbox Settings
    SANDBOX_TIMEOUT_SECONDS: float = 4.0

    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"] if ENVIRONMENT != "production" else os.getenv("ALLOWED_ORIGINS", "*").split(",")


settings = Settings()
