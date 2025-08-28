# app/compliance.py
import re
from typing import Tuple

# Patterns to detect typical secrets / tokens / emails (extend as needed)
EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
LONG_HEX_RE = re.compile(r"\b[0-9a-fA-F]{32,}\b")  # long hex tokens
AWS_KEY_RE = re.compile(r"AKIA[0-9A-Z]{16}")  # AWS Access Key ID pattern (common example)
API_KEY_LIKE = re.compile(r"(?i)(api[_-]?key|secret|token)[\s:=]+['\"]?([A-Za-z0-9\-_\.]{16,})['\"]?")

FORBIDDEN_KEYWORDS = {"password", "passwd", "secret", "api_key", "private_key", "confidential"}


def _contains_forbidden_keyword(code: str) -> bool:
    lower = code.lower()
    return any(word in lower for word in FORBIDDEN_KEYWORDS)


def sanitize_code(code: str) -> Tuple[str, bool]:
    """
    Sanitize code by redacting emails, long tokens, common API keys, and any discovered sensitive strings.
    Returns (sanitized_code, did_sanitize_bool)
    """
    original = code
    sanitized = code

    # redact emails
    sanitized = EMAIL_RE.sub("[REDACTED_EMAIL]", sanitized)
    # redact long hex-like tokens
    sanitized = LONG_HEX_RE.sub("[REDACTED_TOKEN]", sanitized)
    # redact AWS-like keys
    sanitized = AWS_KEY_RE.sub("[REDACTED_AWS_KEY]", sanitized)

    # redact obvious api_key=... or token: ...
    def _api_key_repl(m):
        keyname = m.group(1)
        return f"{keyname}= [REDACTED_SECRET]"

    sanitized = API_KEY_LIKE.sub(_api_key_repl, sanitized)

    # naive line-based secret removal: remove lines containing forbidden keywords (redact value)
    def _redact_line(line: str) -> str:
        low = line.lower()
        for kw in FORBIDDEN_KEYWORDS:
            if kw in low:
                # keep the key name, redact the rest of the line
                # simple heuristic: split at the keyword and redact after
                parts = re.split(f"(?i)({kw})", line, maxsplit=1)
                if len(parts) >= 3:
                    return parts[0] + parts[1] + " [REDACTED]"
                return "[REDACTED_LINE]"
        return line

    sanitized_lines = []
    for l in sanitized.splitlines():
        sanitized_lines.append(_redact_line(l))
    sanitized = "\n".join(sanitized_lines)

    did_sanitize = sanitized != original
    return sanitized, did_sanitize


def validate_request(code: str) -> Tuple[bool, str]:
    """
    Validate the request according to simple policy rules.
    Returns (is_valid, reason)
    """
    # If forbidden keywords present, reject
    if _contains_forbidden_keyword(code):
        return False, "Request contains forbidden keywords that may indicate secrets."

    # If code is extremely large, reject (prevent DoS)
    if len(code) > 1_000_000:  # 1MB cap for basic MVP
        return False, "Payload too large."

    # Additional checks can be plugged here (PII detectors, allowlists, etc.)
    return True, "OK"
