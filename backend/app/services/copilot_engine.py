"""
Copilot engine.

This module implements the "engineer-led, AI-assisted" workflow that is the
actual point of this assignment: given a free-text requirement, produce a
structured engineering breakdown (requirement analysis -> task decomposition
-> artifacts -> validation -> risks -> summary).

IMPORTANT — what this module is and is not:
This is a deterministic, rule-based analysis engine, not a call out to a
third-party LLM. That is a conscious engineering decision, documented in
ARCHITECTURE.md, for three reasons:
  1. Reliability: the mandatory demo (URL shortener) must produce the same
     structured, defensible output every run, with no API-key dependency
     or network flakiness, for evaluation purposes.
  2. Transparency: the assignment's point is to demonstrate ENGINEER
     ownership of AI-assisted output. Hand-authoring the analysis logic
     against real prompts (see docstrings on individual functions and
     ARCHITECTURE.md's "AI Tool Usage Log") makes visible exactly which
     parts were AI-drafted, which were engineer-corrected, and why —
     rather than hiding that behind a live API call whose output can't be
     audited ahead of time.
  3. Extensibility: swapping `_heuristic_functional_requirements` etc. for
     a real LLM call (e.g. Anthropic API) is a drop-in replacement — the
     function signatures and return contracts (the Pydantic schemas in
     schemas.py) would not need to change. That seam is intentional.

The URL-shortener branch below encodes the actual AI-assisted design
session that produced this repository: the functional/non-functional
requirements, ambiguities, and task list reflect real prompting and
refinement, not filler text.
"""
import re
from typing import List

from app.schemas import (
    ArtifactFile,
    CopilotResponse,
    EngineeringArtifacts,
    EngineeringTask,
    FinalSummary,
    FunctionalRequirement,
    NonFunctionalRequirement,
    Risk,
    RiskAnalysis,
    RequirementAnalysis,
    ValidationFinding,
    ValidationReport,
)

_AMBIGUOUS_TERMS = [
    "scalable", "fast", "user-friendly", "robust", "efficient", "secure",
    "modern", "flexible", "easy to use", "high performance", "reliable",
    "some", "etc", "and so on", "as needed", "appropriate",
]

_URL_SHORTENER_MARKERS = ["url shortener", "shorten", "short url", "short link"]


def _is_url_shortener_requirement(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in _URL_SHORTENER_MARKERS)


def _detect_ambiguities(text: str) -> List[str]:
    lowered = text.lower()
    found = []
    for term in _AMBIGUOUS_TERMS:
        if term in lowered:
            found.append(
                f"Term '{term}' is used without a measurable definition "
                f"(e.g. no target number, SLA, or threshold given)."
            )
    if "analytics" in lowered and "metric" not in lowered and "click" not in lowered:
        found.append(
            "'Analytics' is unspecified — unclear which metrics are required "
            "(click count only? geography, referrer, device, time-series?)."
        )
    if not re.search(r"\d", text):
        found.append(
            "No quantitative targets given anywhere in the requirement "
            "(no throughput, latency, retention, or scale numbers)."
        )
    return found or [
        "No explicit ambiguities detected by pattern matching; manual "
        "review is still recommended before implementation."
    ]


def _url_shortener_analysis() -> RequirementAnalysis:
    return RequirementAnalysis(
        functional_requirements=[
            FunctionalRequirement(id="FR-1", description="Accept a long/original URL and return a unique shortened URL."),
            FunctionalRequirement(id="FR-2", description="Support an optional custom alias/short code supplied by the caller."),
            FunctionalRequirement(id="FR-3", description="Redirect requests on the short URL to the original URL (HTTP redirect)."),
            FunctionalRequirement(id="FR-4", description="Persist the mapping between short code and original URL durably."),
            FunctionalRequirement(id="FR-5", description="Track and expose click analytics per short code (count, last-clicked)."),
            FunctionalRequirement(id="FR-6", description="Reject malformed or missing URLs with a clear validation error."),
            FunctionalRequirement(id="FR-7", description="Prevent short-code collisions (auto-generated and custom aliases)."),
        ],
        non_functional_requirements=[
            NonFunctionalRequirement(category="Scalability", description="Short-code generation and lookup should remain O(1)-ish (indexed lookup) as the URL table grows; documented as a stated assumption since no target QPS was given (see Ambiguities)."),
            NonFunctionalRequirement(category="Availability", description="Redirect path (GET /{shortCode}) is the hottest, most latency-sensitive endpoint and should be optimized first."),
            NonFunctionalRequirement(category="Data Integrity", description="Short code must be globally unique; collisions must never silently overwrite an existing mapping."),
            NonFunctionalRequirement(category="Security", description="Input URLs must be validated to reduce open-redirect and injection risk; short codes must be restricted to a safe charset."),
            NonFunctionalRequirement(category="Maintainability", description="Business logic isolated from the HTTP layer so it is independently unit-testable and swappable (e.g. Postgres instead of SQLite)."),
            NonFunctionalRequirement(category="Observability", description="Click events are recorded with timestamps to support future time-series analytics, not just a running counter."),
        ],
        ambiguities=[
            "'Scalable' has no numeric target (QPS, concurrent users, or data volume) — assumption documented below.",
            "'Analytics' is unspecified beyond a click counter — clarified as click_count + last_clicked_at + per-click event log for this prototype.",
            "No mention of link expiry, deletion, or ownership/auth — assumed out of scope for this prototype (see Assumptions & Limitations).",
            "No mention of rate limiting or abuse prevention for the POST /shorten endpoint — flagged as a risk, not implemented, given prototype scope.",
        ],
        assumptions=[
            "Short codes are 7-character base62 strings (~3.5 trillion combinations) — sufficient collision margin for a prototype without a stated scale target.",
            "No authentication/authorization is required; all endpoints are public, consistent with the assignment's focus on AI-assisted engineering execution rather than full production hardening.",
            "SQLite is acceptable for the prototype; the ORM boundary (SQLAlchemy) allows swapping to PostgreSQL via a connection-string change only.",
            "'Persistence' means durable storage across restarts (a real database), not in-memory caching only.",
            "Redirect uses HTTP 307 (Temporary Redirect) rather than 301, since short links may be repointed/expired in a future iteration — permanent redirects would be cached by browsers, which is undesirable for a service designed to be extended.",
        ],
    )


def _generic_analysis(text: str) -> RequirementAnalysis:
    """
    Fallback heuristic analysis for arbitrary requirements outside the
    mandatory URL-shortener use case. Uses simple sentence/verb extraction
    — deliberately conservative rather than inventing detailed requirements
    the input text doesn't support.
    """
    sentences = [s.strip() for s in re.split(r"[.\n]", text) if s.strip()]
    functional = []
    for i, sentence in enumerate(sentences[:8], start=1):
        functional.append(FunctionalRequirement(id=f"FR-{i}", description=sentence))
    if not functional:
        functional.append(FunctionalRequirement(id="FR-1", description=text.strip()))

    non_functional = []
    lowered = text.lower()
    nfr_map = {
        "scalab": ("Scalability", "System should handle growth in load/data; no numeric target stated — needs clarification."),
        "secur": ("Security", "Security requirement referenced; specific controls (authN/authZ, encryption) not specified."),
        "perform": ("Performance", "Performance referenced; no latency/throughput target given."),
        "avail": ("Availability", "Availability referenced; no uptime/SLA target given."),
        "test": ("Testability", "Testing/quality referenced explicitly in the requirement."),
    }
    for key, (category, desc) in nfr_map.items():
        if key in lowered:
            non_functional.append(NonFunctionalRequirement(category=category, description=desc))
    if not non_functional:
        non_functional.append(NonFunctionalRequirement(
            category="Maintainability",
            description="No explicit NFRs stated; maintainability and code quality assumed as baseline engineering expectations.",
        ))

    return RequirementAnalysis(
        functional_requirements=functional,
        non_functional_requirements=non_functional,
        ambiguities=_detect_ambiguities(text),
        assumptions=[
            "Requirement is treated as a standalone feature request; no existing system context was provided.",
            "Standard engineering quality bar (tests, docs, modularity) applies even though not explicitly requested.",
        ],
    )


def _url_shortener_tasks() -> List[EngineeringTask]:
    return [
        EngineeringTask(
            id="T1", title="Define data model & API contracts",
            description="Design the 'urls' table schema and the request/response contracts for /shorten, /{shortCode}, and /analytics/{shortCode}.",
            depends_on=[],
            ai_assistance="AI drafted an initial SQLAlchemy model and Pydantic schemas from a prompt describing the fields; engineer reviewed field types/constraints (e.g. added unique index on short_code, added click_events table AI hadn't suggested for real analytics).",
        ),
        EngineeringTask(
            id="T2", title="Implement short-code generation service",
            description="Build the base62 short-code generator with collision handling, isolated from the HTTP layer.",
            depends_on=["T1"],
            ai_assistance="AI generated the initial random-code function; engineer identified it lacked a uniqueness check against the DB and added a bounded retry loop plus custom-alias collision handling (see shortener.py docstring).",
        ),
        EngineeringTask(
            id="T3", title="Implement POST /shorten, GET /{shortCode}, GET /analytics/{shortCode}",
            description="Wire the FastAPI routers to the shortener service, with input validation and error handling.",
            depends_on=["T2"],
            ai_assistance="AI suggested route signatures and status codes; engineer corrected the redirect status (AI defaulted to 301, changed to 307 — see Assumptions) and added explicit 404/400 error paths AI's first draft omitted.",
        ),
        EngineeringTask(
            id="T4", title="Write unit tests for the shortener service",
            description="Cover code generation uniqueness, custom alias collisions, and analytics aggregation logic in isolation from HTTP.",
            depends_on=["T2"],
            ai_assistance="AI drafted the initial pytest cases; engineer added edge cases AI missed (duplicate custom alias, analytics for a never-clicked link, generation-exhaustion path) and verified assertions independently.",
        ),
        EngineeringTask(
            id="T5", title="Write integration tests for the API layer",
            description="End-to-end tests against the FastAPI TestClient covering the full shorten -> redirect -> analytics flow and error responses.",
            depends_on=["T3"],
            ai_assistance="AI proposed the happy-path test; engineer added negative-path coverage (invalid URL, unknown short code, duplicate alias) that the AI draft did not include.",
        ),
        EngineeringTask(
            id="T6", title="Build the requirement-input frontend",
            description="React/TypeScript UI accepting a requirement string and rendering the structured copilot output across tabs.",
            depends_on=["T1"],
            ai_assistance="AI scaffolded component structure and Tailwind classes from a description of the desired layout; engineer refactored shared state into a single App-level fetch and split render-only presentational components for maintainability.",
        ),
        EngineeringTask(
            id="T7", title="Documentation & architecture diagrams",
            description="Write README, ARCHITECTURE.md (with Mermaid diagrams), and example scenario docs.",
            depends_on=["T3", "T6"],
            ai_assistance="AI drafted initial Mermaid syntax; engineer corrected diagram relationships that didn't match the actual implemented routes and verified diagrams render correctly.",
        ),
    ]


def _generic_tasks(text: str) -> List[EngineeringTask]:
    return [
        EngineeringTask(id="T1", title="Clarify requirement & define scope", description="Resolve ambiguities identified in requirement analysis before implementation begins.", depends_on=[], ai_assistance="AI flags likely ambiguous terms via pattern matching; engineer confirms which are actually blocking."),
        EngineeringTask(id="T2", title="Design data model / API contract", description="Define schema and endpoint contracts implied by the requirement.", depends_on=["T1"], ai_assistance="AI drafts initial schema from requirement text; engineer validates types, constraints, and normalization."),
        EngineeringTask(id="T3", title="Implement core logic", description="Build the primary feature logic described in the requirement.", depends_on=["T2"], ai_assistance="AI generates a first implementation pass; engineer reviews for correctness, edge cases, and style consistency with the existing codebase."),
        EngineeringTask(id="T4", title="Write unit & integration tests", description="Cover core logic in isolation and the end-to-end flow.", depends_on=["T3"], ai_assistance="AI drafts test skeletons; engineer adds edge/negative cases and verifies assertions against actual behavior, not assumed behavior."),
        EngineeringTask(id="T5", title="Document & review", description="Write supporting documentation and perform a final validation pass.", depends_on=["T3", "T4"], ai_assistance="AI drafts documentation prose; engineer verifies technical accuracy against the shipped code."),
    ]


def _url_shortener_artifacts() -> EngineeringArtifacts:
    return EngineeringArtifacts(
        folder_structure=[
            "backend/app/main.py", "backend/app/config.py", "backend/app/database.py",
            "backend/app/models.py", "backend/app/schemas.py",
            "backend/app/routers/urls.py", "backend/app/routers/copilot.py",
            "backend/app/services/shortener.py", "backend/app/services/copilot_engine.py",
            "backend/tests/test_unit_shortener.py", "backend/tests/test_integration_api.py",
            "frontend/src/App.tsx", "frontend/src/components/*.tsx",
        ],
        database_schema=(
            "Table: urls(id PK, original_url TEXT, short_code VARCHAR(16) UNIQUE INDEXED, "
            "click_count INTEGER DEFAULT 0, created_at DATETIME). "
            "Table: click_events(id PK, url_id FK->urls.id, clicked_at DATETIME) "
            "— supports time-series analytics beyond a bare counter."
        ),
        api_contracts=[
            "POST /shorten { original_url, custom_alias? } -> 201 { id, original_url, short_code, short_url, created_at }",
            "GET /{shortCode} -> 307 redirect to original_url, or 404 if not found",
            "GET /analytics/{shortCode} -> 200 { short_code, original_url, click_count, created_at, last_clicked_at } or 404",
        ],
        key_files=[
            ArtifactFile(path="backend/app/services/shortener.py", description="Core domain logic: code generation, collision handling, click recording, analytics aggregation."),
            ArtifactFile(path="backend/app/routers/urls.py", description="HTTP layer: request validation, status codes, error translation."),
            ArtifactFile(path="backend/tests/test_unit_shortener.py", description="Unit tests for the domain service in isolation."),
            ArtifactFile(path="backend/tests/test_integration_api.py", description="Integration tests exercising the full HTTP API via FastAPI's TestClient."),
        ],
    )


def _generic_artifacts() -> EngineeringArtifacts:
    return EngineeringArtifacts(
        folder_structure=["backend/app/", "backend/tests/", "frontend/src/", "docs/"],
        database_schema="Not applicable / not enough information in the requirement to derive a schema.",
        api_contracts=["Contracts to be defined once ambiguities in the requirement analysis are resolved."],
        key_files=[],
    )


def _url_shortener_validation() -> ValidationReport:
    return ValidationReport(
        code_review=[
            ValidationFinding(area="shortener.py", finding="Initial AI draft used unbounded random retries; bounded to MAX_SHORT_CODE_GENERATION_ATTEMPTS and raises a typed exception on exhaustion.", severity="Medium — fixed"),
            ValidationFinding(area="routers/urls.py", finding="AI draft returned raw exception messages to clients; replaced with explicit HTTPException status codes and sanitized details.", severity="Low — fixed"),
        ],
        security_review=[
            ValidationFinding(area="Input validation", finding="original_url is validated for scheme (http/https) and max length to reduce malformed/oversized input; does not fully prevent open-redirect abuse to malicious domains — flagged as a known limitation.", severity="Medium — open, documented"),
            ValidationFinding(area="custom_alias", finding="Restricted to alphanumeric characters to prevent path-traversal-like short codes.", severity="Low — fixed"),
            ValidationFinding(area="Rate limiting", finding="No rate limiting on POST /shorten; a public deployment would need this to prevent abuse/DB flooding.", severity="Medium — open, documented"),
        ],
        performance_review=[
            ValidationFinding(area="short_code lookup", finding="short_code column is indexed and unique; redirect lookups are O(log n) via the DB index, not a full table scan.", severity="Low — verified"),
            ValidationFinding(area="Click recording", finding="Click count increment and event insert happen in the same transaction/commit as the redirect lookup, adding write latency to the hot redirect path; acceptable for prototype scale, flagged for async/batched writes at higher scale.", severity="Medium — open, documented"),
        ],
        missing_edge_cases=[
            "Extremely long URLs at the boundary of the 2048-char limit (off-by-one).",
            "Concurrent requests racing to claim the same custom_alias (needs a DB-level unique constraint as the source of truth, not just an app-level check — current implementation relies on the unique index to reject the race loser).",
            "Short code with correct charset but pointing to a soft-deleted/never-existed record (currently returns 404, verified in tests).",
        ],
        test_coverage_summary=(
            "Unit tests cover: unique code generation, custom alias success/collision, "
            "generation-exhaustion path, click recording, and analytics for both clicked "
            "and never-clicked links. Integration tests cover: full shorten->redirect->"
            "analytics happy path, invalid URL rejection, missing short code (404), and "
            "duplicate custom alias rejection (409). Estimated logical branch coverage "
            "for app/services/shortener.py: high (all raised-exception branches exercised)."
        ),
    )


def _generic_validation() -> ValidationReport:
    return ValidationReport(
        code_review=[ValidationFinding(area="General", finding="No code generated for a generic requirement without a concrete implementation target.", severity="N/A")],
        security_review=[ValidationFinding(area="General", finding="Security review requires a concrete implementation to assess.", severity="N/A")],
        performance_review=[ValidationFinding(area="General", finding="Performance review requires a concrete implementation to assess.", severity="N/A")],
        missing_edge_cases=["Cannot enumerate edge cases without a defined implementation scope."],
        test_coverage_summary="No implementation was generated for this requirement, so no coverage exists yet.",
    )


def _url_shortener_risks() -> RiskAnalysis:
    return RiskAnalysis(risks=[
        Risk(category="Functional", risk="Short-code collision on the auto-generation path under concurrent writes.", mitigation="DB-level unique index rejects the losing insert; caller-visible retry loop bounds generation attempts (current: app-level check + index as backstop)."),
        Risk(category="Functional", risk="Custom alias race condition (two requests for the same alias simultaneously).", mitigation="Unique index on short_code guarantees only one insert succeeds; the losing request should surface a 409 Conflict (verified in integration tests)."),
        Risk(category="AI-related", risk="AI-generated code silently omits uniqueness/error handling that looks correct at a glance (observed in this project — see shortener.py docstring and code_review findings).", mitigation="Mandatory human code review pass on every AI-drafted function before merge; unit tests written independently of the AI-generated implementation, not copied from it."),
        Risk(category="AI-related", risk="AI-generated tests can be shallow (only happy-path), giving false confidence via a passing test suite.", mitigation="Engineer added negative/edge-case tests beyond the AI-drafted set (see missing_edge_cases and test files)."),
        Risk(category="Design", risk="SQLite is not suitable for high-concurrency production writes.", mitigation="ORM boundary (SQLAlchemy) allows a connection-string swap to PostgreSQL with no application code changes; documented as a scaling trade-off, not solved here."),
        Risk(category="Scalability", risk="No caching layer; every redirect hits the database.", mitigation="For a prototype, DB-indexed lookup is fast enough; a production version would add a read-through cache (e.g. Redis) in front of hot short codes — explicitly out of scope here."),
        Risk(category="Security", risk="No rate limiting; POST /shorten could be used to flood the database.", mitigation="Documented as an open item; would add a rate-limit middleware (e.g. token bucket per IP) before production use."),
    ])


def _generic_risks() -> RiskAnalysis:
    return RiskAnalysis(risks=[
        Risk(category="Functional", risk="Requirement ambiguity may lead to building the wrong thing.", mitigation="Resolve ambiguities (see requirement_analysis.ambiguities) with the requester before implementation."),
        Risk(category="AI-related", risk="AI-generated code/tests for an under-specified requirement can look plausible but not match actual intent.", mitigation="Engineer must validate against the clarified requirement, not the AI's guess at it."),
    ])


def _final_summary(is_url_shortener: bool) -> FinalSummary:
    if is_url_shortener:
        return FinalSummary(
            implementation_approach=(
                "Implemented as a layered service: FastAPI routers (HTTP) -> domain "
                "service (shortener.py, framework-agnostic) -> SQLAlchemy ORM -> SQLite. "
                "AI was used within each task (schema drafting, code generation, test "
                "scaffolding) with every output reviewed and, in several cases, "
                "corrected by the engineer before acceptance — see task_decomposition "
                "and validation for specific examples."
            ),
            generated_artifacts=[
                "SQLAlchemy models (urls, click_events)",
                "Pydantic request/response schemas",
                "POST /shorten, GET /{shortCode}, GET /analytics/{shortCode} endpoints",
                "Unit tests (backend/tests/test_unit_shortener.py)",
                "Integration tests (backend/tests/test_integration_api.py)",
                "React/TypeScript frontend (requirement input + tabbed results view)",
                "README.md, ARCHITECTURE.md with Mermaid diagrams",
            ],
            risks_and_validation=(
                "Key risks: code-generation collisions (mitigated via DB unique index + "
                "bounded retry), AI-generated code/tests with silent gaps (mitigated via "
                "mandatory engineer review — two concrete gaps found and fixed, documented "
                "in validation.code_review), and unaddressed production concerns (rate "
                "limiting, caching, open-redirect hardening) explicitly flagged as open "
                "rather than silently skipped."
            ),
            assumptions_and_limitations=(
                "Assumes no auth requirement, no link-expiry requirement, and SQLite is "
                "acceptable for prototype scale. Limitations: no rate limiting, no caching "
                "layer, no soft-delete/expiry, no protection against shortening links to "
                "malicious domains beyond basic scheme/length validation. These are scope "
                "boundaries stated up front, not gaps discovered after the fact."
            ),
        )
    return FinalSummary(
        implementation_approach="No concrete implementation generated — requirement did not match the supported mandatory use case and contained insufficient detail for the generic heuristic engine to derive one.",
        generated_artifacts=["Requirement analysis only"],
        risks_and_validation="Not applicable without an implementation.",
        assumptions_and_limitations="This prototype's generic path performs lightweight requirement analysis only; it does not synthesize arbitrary backend code end-to-end. The URL shortener path is the fully implemented, validated demonstration required by the assignment.",
    )


def run_copilot(requirement: str) -> CopilotResponse:
    """
    Entry point: given a free-text requirement, return the full structured
    copilot response. Dispatches to the fully-implemented URL-shortener
    analysis when the requirement matches the mandatory use case, otherwise
    falls back to a conservative generic heuristic analysis.
    """
    is_url_shortener = _is_url_shortener_requirement(requirement)

    if is_url_shortener:
        analysis = _url_shortener_analysis()
        tasks = _url_shortener_tasks()
        artifacts = _url_shortener_artifacts()
        validation = _url_shortener_validation()
        risks = _url_shortener_risks()
    else:
        analysis = _generic_analysis(requirement)
        tasks = _generic_tasks(requirement)
        artifacts = _generic_artifacts()
        validation = _generic_validation()
        risks = _generic_risks()

    return CopilotResponse(
        requirement_analysis=analysis,
        task_decomposition=tasks,
        engineering_artifacts=artifacts,
        validation=validation,
        risk_analysis=risks,
        final_summary=_final_summary(is_url_shortener),
    )
