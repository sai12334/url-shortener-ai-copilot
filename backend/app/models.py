"""
ORM models.

Schema (table: urls)
---------------------
id            INTEGER PRIMARY KEY
original_url  TEXT      NOT NULL
short_code    VARCHAR   NOT NULL UNIQUE, INDEXED
click_count   INTEGER   NOT NULL DEFAULT 0
created_at    DATETIME  NOT NULL DEFAULT now()

A separate ClickEvent table is included beyond the mandatory minimum schema
to support real analytics (timestamped click history) rather than a bare
counter. This is called out explicitly in ARCHITECTURE.md as a deliberate
scope extension, not scope creep left unexplained.
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(16), unique=True, index=True, nullable=False)
    click_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=utcnow)

    click_events = relationship(
        "ClickEvent", back_populates="url", cascade="all, delete-orphan"
    )


class ClickEvent(Base):
    """
    One row per redirect, enabling time-series analytics (e.g. clicks per
    day) instead of only a running total. Kept intentionally minimal
    (no IP/user-agent capture) to avoid unnecessary PII collection in a
    prototype with no stated privacy/compliance requirement.
    """
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    clicked_at = Column(DateTime, nullable=False, default=utcnow)

    url = relationship("URL", back_populates="click_events")
