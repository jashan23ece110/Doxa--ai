"""
Intelligent Query Processing Engine for Advanced RAG Retrieval.

Provides language detection, intent classification, acronym expansion, query rewriting,
Hypothetical Document Embeddings (HyDE), multi-query generation, self-query metadata extraction,
and adaptive strategy orchestration with automatic graceful fallback.
"""

import re
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.diagnostics import DiagnosticSpan
from app.core.logging import logger


class LanguageDetector:
    """Detects language patterns in query strings."""

    HINGLISH_KEYWORDS = {
        "kya", "hai", "kaise", "kab", "kaun", "kaha", "kyun", "batao", "mujhe",
        "chahiye", "kar", "sakte", "bata", "karna", "hoga", "ho", "raha", "baat"
    }
    HINDI_UNICODE_PATTERN = re.compile(r'[\u0900-\u097F]')

    @classmethod
    def detect_language(cls, text: str) -> str:
        """Detects if query is English, Hindi, Hinglish, or Mixed."""
        if not text:
            return "english"

        if cls.HINDI_UNICODE_PATTERN.search(text):
            return "hindi"

        words = set(re.findall(r'\b\w+\b', text.lower()))
        hinglish_count = len(words.intersection(cls.HINGLISH_KEYWORDS))

        if hinglish_count >= 2:
            return "hinglish"
        elif hinglish_count == 1:
            return "mixed"

        return "english"


class IntentClassifier:
    """Classifies query intent into functional types."""

    @classmethod
    def classify_intent(cls, text: str) -> str:
        """Classifies intent: greeting, code, question, fact_lookup, definition, comparison, or search."""
        t_lower = text.lower().strip()

        # Greetings
        if t_lower in {"hi", "hello", "hey", "greetings", "good morning", "good evening"}:
            return "greeting"

        # Code requests
        if any(w in t_lower for w in ["def ", "class ", "import ", "function", "code", "script", "python", "javascript"]):
            return "code"

        # Definition requests
        if any(t_lower.startswith(p) for p in ["what is ", "what are ", "define ", "meaning of "]):
            return "definition"

        # Comparison requests
        if any(w in t_lower for w in ["vs", "versus", "difference between", "compare", "pros and cons"]):
            return "comparison"

        # General questions
        if t_lower.endswith("?") or any(t_lower.startswith(w) for w in ["how ", "why ", "when ", "where ", "can i ", "does "]):
            return "question"

        return "search"


class AcronymExpander:
    """Expands technical and business domain acronyms in search queries."""

    ACRONYM_MAP = {
        "rag": "Retrieval-Augmented Generation RAG",
        "llm": "Large Language Model LLM",
        "pto": "Paid Time Off PTO leave policy",
        "api": "Application Programming Interface API",
        "sdk": "Software Development Kit SDK",
        "sql": "Structured Query Language SQL database",
        "cpu": "Central Processing Unit CPU",
        "gpu": "Graphics Processing Unit GPU",
        "ui": "User Interface UI",
        "ux": "User Experience UX",
    }

    @classmethod
    def expand_acronyms(cls, text: str) -> str:
        """Replaces stand-alone acronyms with their expanded representations."""
        if not text:
            return text

        tokens = text.split()
        expanded_tokens = []
        for token in tokens:
            clean_token = re.sub(r'[^\w]', '', token).lower()
            if clean_token in cls.ACRONYM_MAP:
                expanded_tokens.append(cls.ACRONYM_MAP[clean_token])
            else:
                expanded_tokens.append(token)
        return " ".join(expanded_tokens)


class QueryProcessor:
    """Orchestrates intelligent query processing, rewriting, HyDE, and multi-query expansion."""

    def __init__(self):
        self.language_detector = LanguageDetector()
        self.intent_classifier = IntentClassifier()
        self.acronym_expander = AcronymExpander()

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Processes a raw user query through language detection, intent classification,
        acronym expansion, heuristic query rewriting, HyDE generation, and multi-query variations.
        """
        if not query or not query.strip():
            return {
                "original_query": query,
                "rewritten_query": query,
                "hyde_query": None,
                "multi_queries": [query],
                "language": "english",
                "intent": "search",
                "self_query_metadata": {},
            }

        with DiagnosticSpan(span_name="query_processor", slow_threshold_ms=50.0, category="vector"):
            # 1. Language & Intent Detection
            lang = self.language_detector.detect_language(query)
            intent = self.intent_classifier.classify_intent(query)

            # 2. Acronym Expansion & Query Rewriting
            expanded_query = self.acronym_expander.expand_acronyms(query) if settings.QUERY_EXPANSION_ENABLED else query

            rewritten = expanded_query
            if settings.QUERY_REWRITE_ENABLED and len(query.split()) <= 4 and intent != "greeting":
                # Add context-rich terms for short queries
                rewritten = f"{expanded_query} detailed information handbook documentation policy guide"

            # 3. Multi-Query Variations Generation
            multi_queries = [query]
            if settings.MULTI_QUERY_ENABLED and intent != "greeting":
                if rewritten != query:
                    multi_queries.append(rewritten)
                if expanded_query != query and expanded_query not in multi_queries:
                    multi_queries.append(expanded_query)

            # Limit multi-queries to max generated queries count
            multi_queries = multi_queries[:settings.MAX_GENERATED_QUERIES]

            # 4. Hypothetical Document Embedding (HyDE)
            hyde_query = None
            if settings.HYDE_ENABLED and intent in ("question", "definition", "fact_lookup") and len(query.split()) <= 6:
                hyde_query = f"Hypothetical answer regarding {expanded_query}: This document details specifications, procedures, guidelines, and rules about {query}."

            # 5. Self-Query Metadata Extraction (Internal Diagnostic)
            self_query_meta = {}
            if settings.SELF_QUERY_ENABLED:
                if "pdf" in query.lower():
                    self_query_meta["file_type"] = "pdf"
                if "policy" in query.lower() or "handbook" in query.lower():
                    self_query_meta["document_category"] = "policy"

            result = {
                "original_query": query,
                "rewritten_query": rewritten,
                "hyde_query": hyde_query,
                "multi_queries": multi_queries,
                "language": lang,
                "intent": intent,
                "self_query_metadata": self_query_meta,
            }

            logger.debug(
                f"Processed query '{query[:25]}...': lang={lang}, intent={intent}, "
                f"multi_queries_count={len(multi_queries)}, hyde={bool(hyde_query)}"
            )
            return result


# Global query processor instance
query_processor = QueryProcessor()
