"""
Legacy Security Sanitizers and Upload Defense.

Re-exports FilenameSanitizer, DocumentSanitizer, PromptSanitizer, and ToolValidator
for 100% backward compatibility.
"""

import os
import re
from typing import Tuple, Dict, Any
from app.core.config import settings
from app.core.exceptions import BadRequestError, PayloadTooLargeError, PromptInjectionError
from app.core.logging import security_logger


class FilenameSanitizer:
    """Normalizes filenames to prevent path traversal and shell code injection."""

    @staticmethod
    def sanitize(filename: str) -> str:
        if not filename:
            return "unnamed_document.txt"

        clean_name = os.path.basename(filename)
        clean_name = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', clean_name)
        clean_name = re.sub(r'[\/\\]', '', clean_name)
        clean_name = re.sub(r'\.\.+', '.', clean_name)

        clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', clean_name).strip("._")

        if not clean_name:
            clean_name = "document.txt"

        if len(clean_name) > 100:
            name_part, ext_part = os.path.splitext(clean_name)
            clean_name = name_part[:90] + ext_part

        return clean_name


class DocumentSanitizer:
    """Validates document file magic bytes, size limits, PDF integrity, and text injection."""

    PROMPT_INJECTION_PATTERNS = [
        re.compile(r'ignore\s+(all\s+)?(previous|prior)\s+instructions', re.IGNORECASE),
        re.compile(r'override\s+(developer|system)\s+prompt', re.IGNORECASE),
        re.compile(r'system\s+prompt\s*:\s*you\s+are', re.IGNORECASE),
        re.compile(r'<\|im_start\|>\s*system', re.IGNORECASE),
        re.compile(r'\[system\s*:\s*override\]', re.IGNORECASE),
        re.compile(r'reveal\s+your\s+system\s+prompt', re.IGNORECASE),
    ]

    @classmethod
    def validate_file_upload(cls, filename: str, content_bytes: bytes) -> Tuple[str, str]:
        if len(content_bytes) == 0:
            raise BadRequestError("Uploaded file is empty.")

        if len(content_bytes) > settings.MAX_UPLOAD_SIZE_BYTES:
            max_mb = settings.MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)
            security_logger.warning(f"File upload blocked: size {len(content_bytes)} bytes exceeds limit {max_mb}MB")
            raise PayloadTooLargeError(f"File size exceeds maximum allowed limit of {max_mb}MB.")

        sanitized_filename = FilenameSanitizer.sanitize(filename)
        ext = os.path.splitext(sanitized_filename)[1].lower()

        if ext not in settings.ALLOWED_EXTENSIONS:
            raise BadRequestError(f"Unsupported extension '{ext}'. Allowed extensions: {settings.ALLOWED_EXTENSIONS}")

        if ext == ".pdf":
            if not content_bytes.startswith(b"%PDF-"):
                security_logger.warning(f"File upload blocked: invalid PDF header magic bytes for '{sanitized_filename}'")
                raise BadRequestError("Invalid or corrupted PDF file header.")
        elif ext == ".txt":
            try:
                content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                security_logger.warning(f"File upload blocked: invalid UTF-8 encoding for '{sanitized_filename}'")
                raise BadRequestError("Invalid text file encoding. Only UTF-8 plain text is supported.")

        return sanitized_filename, ext

    @classmethod
    def inspect_extracted_text(cls, text: str) -> None:
        if not text or not text.strip():
            raise BadRequestError("Extracted document contains no readable text.")

        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                security_logger.warning(f"Document upload rejected due to prompt injection pattern match: '{pattern.pattern}'")
                raise PromptInjectionError("Security Violation: Document contains unauthorized instruction patterns.")

        if re.search(r'(.)\1{2000,}', text):
            security_logger.warning("Document upload rejected due to excessive repeated character DoS pattern.")
            raise BadRequestError("Invalid document structure: excessive repeated characters detected.")


class PromptSanitizer:
    """Sanitizes incoming prompts and retrieved context against injection attempts."""

    PROMPT_OVERRIDE_RE = re.compile(
        r'(ignore\s+(all\s+)?(previous|prior)\s+instructions|override\s+system\s+prompt|<\|im_start\|>)',
        re.IGNORECASE
    )

    @classmethod
    def sanitize_user_input(cls, user_input: str) -> str:
        if not user_input:
            return ""
        clean = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', user_input).strip()
        return clean

    @classmethod
    def sanitize_context_block(cls, context_text: str) -> str:
        if not context_text:
            return ""
        sanitized = cls.PROMPT_OVERRIDE_RE.sub('[filtered_instruction]', context_text)
        return sanitized


class ToolValidator:
    """Validates tool parameters before execution to prevent parameter abuse."""

    @staticmethod
    def validate_timer(title: str, seconds: int) -> None:
        if not title or not title.strip():
            raise BadRequestError("Timer title cannot be empty.")
        if seconds <= 0 or seconds > settings.MAX_TIMER_DURATION_SECONDS:
            raise BadRequestError(f"Timer duration must be between 1 and {settings.MAX_TIMER_DURATION_SECONDS} seconds.")

    @staticmethod
    def validate_search_query(query: str) -> str:
        if not query or not query.strip():
            raise BadRequestError("Search query cannot be empty.")
        cleaned = query.strip()
        if len(cleaned) > settings.MAX_SEARCH_QUERY_LENGTH:
            raise BadRequestError(f"Search query exceeds maximum length of {settings.MAX_SEARCH_QUERY_LENGTH} characters.")
        return cleaned

    @staticmethod
    def validate_calculator_expression(expression: str) -> str:
        if not expression or not expression.strip():
            raise BadRequestError("Calculator expression cannot be empty.")
        cleaned = expression.strip()
        if len(cleaned) > settings.MAX_CALCULATOR_EXPRESSION_LENGTH:
            raise BadRequestError(f"Calculator expression exceeds maximum length of {settings.MAX_CALCULATOR_EXPRESSION_LENGTH} characters.")
        return cleaned

    @staticmethod
    def validate_python_code(code: str) -> str:
        if not code or not code.strip():
            raise BadRequestError("Python code script cannot be empty.")
        cleaned = code.strip()
        if len(cleaned) > settings.MAX_PYTHON_CODE_LENGTH:
            raise BadRequestError(f"Python script exceeds maximum length of {settings.MAX_PYTHON_CODE_LENGTH} characters.")
        return cleaned
