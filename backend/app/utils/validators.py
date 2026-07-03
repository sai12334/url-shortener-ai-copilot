"""
Small, pure validation helpers shared across schemas/services.

Kept separate from schemas.py so the same rules can be reused by future
non-Pydantic call sites (e.g. a CLI or batch import job) without importing
the web framework's validation layer.
"""
MAX_URL_LENGTH = 2048


def is_valid_url_scheme(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def is_within_max_length(url: str, max_length: int = MAX_URL_LENGTH) -> bool:
    return len(url) <= max_length


def is_safe_alias_charset(alias: str) -> bool:
    return alias.isalnum()
