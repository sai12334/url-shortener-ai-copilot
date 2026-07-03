"""
Pydantic schemas defining API contracts.

These are the source of truth for request/response shapes and are what
generates the OpenAPI schema at /docs.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.validators import (
    MAX_URL_LENGTH,
    is_safe_alias_charset,
    is_valid_url_scheme,
    is_within_max_length,
)


class ShortenRequest(BaseModel):
    original_url: str = Field(..., description="The URL to shorten")
    custom_alias: Optional[str] = Field(
        None,
        min_length=3,
        max_length=16,
        description="Optional custom short code. Must be alphanumeric.",
    )

    @field_validator("original_url")
    @classmethod
    def validate_url_format(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("original_url must not be empty")
        if not is_valid_url_scheme(v):
            raise ValueError("original_url must start with http:// or https://")
        if not is_within_max_length(v):
            raise ValueError(f"original_url exceeds maximum length of {MAX_URL_LENGTH} characters")
        return v

    @field_validator("custom_alias")
    @classmethod
    def validate_alias_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not is_safe_alias_charset(v):
            raise ValueError("custom_alias must be alphanumeric")
        return v


class ShortenResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: datetime
    last_clicked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    detail: str


# ---------------------------------------------------------------------------
# Copilot (AI-assisted engineering workflow) schemas
# ---------------------------------------------------------------------------

class CopilotRequest(BaseModel):
    requirement: str = Field(..., min_length=10, description="Free-text software requirement")


class FunctionalRequirement(BaseModel):
    id: str
    description: str


class NonFunctionalRequirement(BaseModel):
    category: str
    description: str


class RequirementAnalysis(BaseModel):
    functional_requirements: List[FunctionalRequirement]
    non_functional_requirements: List[NonFunctionalRequirement]
    ambiguities: List[str]
    assumptions: List[str]


class EngineeringTask(BaseModel):
    id: str
    title: str
    description: str
    depends_on: List[str]
    ai_assistance: str


class ArtifactFile(BaseModel):
    path: str
    description: str


class EngineeringArtifacts(BaseModel):
    folder_structure: List[str]
    database_schema: str
    api_contracts: List[str]
    key_files: List[ArtifactFile]


class ValidationFinding(BaseModel):
    area: str
    finding: str
    severity: str


class ValidationReport(BaseModel):
    code_review: List[ValidationFinding]
    security_review: List[ValidationFinding]
    performance_review: List[ValidationFinding]
    missing_edge_cases: List[str]
    test_coverage_summary: str


class Risk(BaseModel):
    category: str
    risk: str
    mitigation: str


class RiskAnalysis(BaseModel):
    risks: List[Risk]


class FinalSummary(BaseModel):
    implementation_approach: str
    generated_artifacts: List[str]
    risks_and_validation: str
    assumptions_and_limitations: str


class CopilotResponse(BaseModel):
    requirement_analysis: RequirementAnalysis
    task_decomposition: List[EngineeringTask]
    engineering_artifacts: EngineeringArtifacts
    validation: ValidationReport
    risk_analysis: RiskAnalysis
    final_summary: FinalSummary
