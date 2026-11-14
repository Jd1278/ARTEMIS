"""Structured logging with sensitive credential redaction."""
from __future__ import annotations

import logging
import re
from typing import Any

SECRET_PATTERNS = (
    re.compile(r"(postgresql(?:\+\w+)?://[^:\s]+:)([^@\s]+)(@)", re.IGNORECASE),
    re.compile(r"(SUPABASE_SERVICE_ROLE_KEY\s*=\s*)(\S+)", re.IGNORECASE),
    re.compile(r"(Bearer\s+)([A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE),
    re.compile(r"(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})"),
)


def redact_secrets(text: str) -> str:
    """Mask connection passwords, JWT tokens, and service keys from log messages."""
    sanitized = str(text)
    sanitized = SECRET_PATTERNS[0].sub(r"\1***REDACTED***\3", sanitized)
    sanitized = SECRET_PATTERNS[1].sub(r"\1***REDACTED***", sanitized)
    sanitized = SECRET_PATTERNS[2].sub(r"\1***REDACTED***", sanitized)
    sanitized = SECRET_PATTERNS[3].sub("***REDACTED_JWT***", sanitized)
    return sanitized


class SecretRedactingFilter(logging.Filter):
    """Logging filter that strips secrets from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = redact_secrets(record.msg)
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(
                    redact_secrets(arg) if isinstance(arg, str) else arg for arg in record.args
                )
            elif isinstance(record.args, dict):
                record.args = {
                    k: redact_secrets(v) if isinstance(v, str) else v for k, v in record.args.items()
                }
        return True


def get_logger(name: str = "artemis_health") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        )
        handler.setFormatter(formatter)
        handler.addFilter(SecretRedactingFilter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    logger.addFilter(SecretRedactingFilter())
    return logger
