"""
HTTP layer for the URL shortener use case.

Thin by design: request validation is delegated to Pydantic schemas,
business logic is delegated to app.services.shortener. This router's only
job is translating between HTTP concerns (status codes, redirects) and the
domain service.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import BASE_URL
from app.database import get_db
from app.schemas import AnalyticsResponse, ShortenRequest, ShortenResponse
from app.services import shortener

router = APIRouter(tags=["urls"])


@router.post("/shorten", response_model=ShortenResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    try:
        record = shortener.create_short_url(
            db, original_url=payload.original_url, custom_alias=payload.custom_alias
        )
    except shortener.DuplicateAliasError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except shortener.ShortCodeGenerationError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    return ShortenResponse(
        id=record.id,
        original_url=record.original_url,
        short_code=record.short_code,
        short_url=f"{BASE_URL}/{record.short_code}",
        created_at=record.created_at,
    )


@router.get("/analytics/{short_code}", response_model=AnalyticsResponse)
def get_analytics(short_code: str, db: Session = Depends(get_db)):
    try:
        data = shortener.get_analytics(db, short_code)
    except shortener.ShortCodeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return AnalyticsResponse(**data)


@router.get("/{short_code}")
def redirect_short_url(short_code: str, db: Session = Depends(get_db)):
    try:
        record = shortener.resolve_and_record_click(db, short_code)
    except shortener.ShortCodeNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return RedirectResponse(url=record.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
