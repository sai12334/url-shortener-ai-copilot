"""
Unit tests for app.services.shortener — exercised directly against the
domain service and an isolated in-memory DB session, with no HTTP layer
involved. These are independent of, not copied from, the AI-drafted
implementation: each test asserts a specific behavioral contract.
"""
import pytest

from app.services import shortener


def test_create_short_url_generates_unique_code(db_session):
    record = shortener.create_short_url(db_session, "https://example.com/very/long/path")
    assert record.id is not None
    assert len(record.short_code) == 7
    assert record.original_url == "https://example.com/very/long/path"
    assert record.click_count == 0


def test_create_short_url_with_custom_alias(db_session):
    record = shortener.create_short_url(
        db_session, "https://example.com", custom_alias="myAlias1"
    )
    assert record.short_code == "myAlias1"


def test_create_short_url_duplicate_alias_raises(db_session):
    shortener.create_short_url(db_session, "https://example.com", custom_alias="dup123")
    with pytest.raises(shortener.DuplicateAliasError):
        shortener.create_short_url(db_session, "https://other.com", custom_alias="dup123")


def test_generated_codes_are_unique_across_many_calls(db_session):
    codes = set()
    for _ in range(50):
        record = shortener.create_short_url(db_session, "https://example.com")
        codes.add(record.short_code)
    assert len(codes) == 50


def test_generation_exhaustion_raises(db_session, monkeypatch):
    # Force every candidate to collide by pre-seeding the code the
    # generator will always produce, verifying the bounded-retry error path.
    monkeypatch.setattr(shortener, "_generate_candidate_code", lambda length=7: "AAAAAAA")
    shortener.create_short_url(db_session, "https://example.com", custom_alias="AAAAAAA")
    with pytest.raises(shortener.ShortCodeGenerationError):
        shortener.create_short_url(db_session, "https://example.com")


def test_resolve_and_record_click_increments_counter(db_session):
    record = shortener.create_short_url(db_session, "https://example.com")
    assert record.click_count == 0

    updated = shortener.resolve_and_record_click(db_session, record.short_code)
    assert updated.click_count == 1

    updated_again = shortener.resolve_and_record_click(db_session, record.short_code)
    assert updated_again.click_count == 2


def test_resolve_unknown_code_raises_not_found(db_session):
    with pytest.raises(shortener.ShortCodeNotFoundError):
        shortener.resolve_and_record_click(db_session, "doesnotexist")


def test_analytics_for_never_clicked_link(db_session):
    record = shortener.create_short_url(db_session, "https://example.com")
    data = shortener.get_analytics(db_session, record.short_code)
    assert data["click_count"] == 0
    assert data["last_clicked_at"] is None


def test_analytics_reflects_click_count_and_last_clicked(db_session):
    record = shortener.create_short_url(db_session, "https://example.com")
    shortener.resolve_and_record_click(db_session, record.short_code)
    shortener.resolve_and_record_click(db_session, record.short_code)

    data = shortener.get_analytics(db_session, record.short_code)
    assert data["click_count"] == 2
    assert data["last_clicked_at"] is not None


def test_analytics_unknown_code_raises_not_found(db_session):
    with pytest.raises(shortener.ShortCodeNotFoundError):
        shortener.get_analytics(db_session, "nosuchcode")
