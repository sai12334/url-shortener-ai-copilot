"""
Shortener domain service.

All business logic for creating short codes and resolving/recording clicks
lives here, kept separate from the HTTP layer (routers) so it can be unit
tested without spinning up FastAPI, and so the router stays a thin
translation layer between HTTP and domain logic (single responsibility).

--- AI-assisted development note ---
The base62 encoding and collision-retry approach below was first drafted
with AI assistance (prompt: "generate a random short code for a URL
shortener, base62, configurable length"). The initial AI suggestion used
`random.choices` without a uniqueness check against existing DB rows —
that is a real correctness gap (silent collisions), so during review it was
extended with a DB-uniqueness check and a bounded retry loop before
acceptance. This is called out explicitly in ARCHITECTURE.md's
"AI-assisted execution" section and in VALIDATION as an example of an
AI-output gap that engineering review caught and fixed.
"""
import secrets
import string
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.config import MAX_SHORT_CODE_GENERATION_ATTEMPTS, SHORT_CODE_LENGTH
from app.models import URL, ClickEvent

_ALPHABET = string.ascii_letters + string.digits  # base62


class DuplicateAliasError(Exception):
    """Raised when a requested custom alias is already taken."""


class ShortCodeGenerationError(Exception):
    """Raised when a unique short code could not be generated after retries."""


class ShortCodeNotFoundError(Exception):
    """Raised when a short code has no matching URL record."""


def _generate_candidate_code(length: int = SHORT_CODE_LENGTH) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def _code_exists(db: Session, code: str) -> bool:
    return db.query(URL).filter(URL.short_code == code).first() is not None


def create_short_url(db: Session, original_url: str, custom_alias: Optional[str] = None) -> URL:
    """
    Create and persist a shortened URL record.

    Raises:
        DuplicateAliasError: if custom_alias is already in use.
        ShortCodeGenerationError: if a unique auto-generated code cannot be
            found within MAX_SHORT_CODE_GENERATION_ATTEMPTS tries.
    """
    if custom_alias:
        if _code_exists(db, custom_alias):
            raise DuplicateAliasError(f"Alias '{custom_alias}' is already in use")
        code = custom_alias
    else:
        code = None
        for _ in range(MAX_SHORT_CODE_GENERATION_ATTEMPTS):
            candidate = _generate_candidate_code()
            if not _code_exists(db, candidate):
                code = candidate
                break
        if code is None:
            raise ShortCodeGenerationError(
                "Could not generate a unique short code after "
                f"{MAX_SHORT_CODE_GENERATION_ATTEMPTS} attempts"
            )

    record = URL(original_url=original_url, short_code=code, click_count=0)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def resolve_and_record_click(db: Session, short_code: str) -> URL:
    """
    Look up the URL for a short code, increment its click counter, and
    record a ClickEvent row for time-series analytics. Returns the updated
    URL record so the caller (router) can issue a redirect.

    Raises:
        ShortCodeNotFoundError: if no URL matches short_code.
    """
    record = db.query(URL).filter(URL.short_code == short_code).first()
    if record is None:
        raise ShortCodeNotFoundError(f"No URL found for short code '{short_code}'")

    record.click_count += 1
    db.add(ClickEvent(url_id=record.id))
    db.commit()
    db.refresh(record)
    return record


def get_analytics(db: Session, short_code: str) -> dict:
    """
    Returns aggregate analytics for a short code, including the most recent
    click timestamp (None if the link has never been clicked).

    Raises:
        ShortCodeNotFoundError: if no URL matches short_code.
    """
    record = db.query(URL).filter(URL.short_code == short_code).first()
    if record is None:
        raise ShortCodeNotFoundError(f"No URL found for short code '{short_code}'")

    last_click: Optional[datetime] = None
    if record.click_events:
        last_click = max(e.clicked_at for e in record.click_events)
        if last_click.tzinfo is None:
            last_click = last_click.replace(tzinfo=timezone.utc)

    return {
        "short_code": record.short_code,
        "original_url": record.original_url,
        "click_count": record.click_count,
        "created_at": record.created_at,
        "last_clicked_at": last_click,
    }
