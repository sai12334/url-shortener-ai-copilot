# AI-Assisted Software Engineering Copilot

A working prototype demonstrating how AI-assisted development (copilot
model) transforms a software requirement into a production-quality
engineering outcome — with a fully implemented, runnable **URL shortener
service** as the mandatory demo use case.

> "AI assists the engineer within tasks; the engineer owns execution and quality."

See `ARCHITECTURE.md` for system design, diagrams, and the AI-tool-usage log.
See `docs/examples/` for greenfield, brownfield, and ambiguous requirement
walkthroughs.

## What's in this repo

1. **Copilot Console** (`frontend/` + `POST /copilot/analyze`) — paste a
   requirement, get back structured requirement analysis, task
   decomposition, engineering artifacts, validation, risk analysis, and a
   final engineering summary.
2. **URL Shortener API** (`backend/`, mandatory use case) — a real,
   persisted, tested service:
   - `POST /shorten` — create a short link (optional custom alias)
   - `GET /{shortCode}` — 307 redirect to the original URL, records a click
   - `GET /analytics/{shortCode}` — click count + last-clicked timestamp

Both are wired into one console UI: the "Live Demo" tab drives the real
API end to end.

## Setup instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is now live at `http://localhost:8000`. Interactive OpenAPI docs
are auto-generated at `http://localhost:8000/docs`. A `url_shortener.db`
SQLite file is created automatically on first run.

To point at PostgreSQL instead, set an env var before starting:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/urlshortener"
```

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api/*` to the
backend on port 8000 (see `frontend/vite.config.ts`), so both must be
running together.

### 3. Try it

- **Copilot Console**: paste the mandatory requirement (pre-filled by
  default) — *"Build a scalable URL shortener service with APIs,
  persistence, and analytics."* — and click **Generate**. Walk through the
  pipeline tabs (Requirement Analysis → Task Decomposition → Engineering
  Artifacts → Validation → Risk Analysis → Final Summary).
- **Live Demo tab**: paste any `http(s)://` URL, optionally set a custom
  alias, click **Shorten**. Click the generated short link to trigger a
  real redirect, then click **refresh** to see the click count update.

### 4. Run the tests

```bash
cd backend
pytest                    # 26 tests: unit + integration
pytest --cov=app          # with coverage
```

All 26 tests pass against a clean checkout (verified during development —
see Testing Approach below).

## Testing approach

**Unit tests** (`tests/test_unit_shortener.py`, `tests/test_unit_copilot.py`)
exercise the domain services directly — no HTTP layer, no FastAPI
`TestClient` — using an isolated in-memory SQLite database per test
(`tests/conftest.py`). They cover:

- Unique short-code generation across repeated calls
- Custom alias success and duplicate-alias rejection
- The bounded-retry exhaustion path (forced via `monkeypatch`)
- Click recording and count accumulation
- Analytics for both clicked and never-clicked links
- Copilot engine's URL-shortener-specific vs. generic-fallback branches
- Task dependency graph integrity (every `depends_on` id actually exists)

**Integration tests** (`tests/test_integration_api.py`) exercise the full
FastAPI app via `TestClient`, covering the mandatory end-to-end flow
(shorten → redirect → analytics) plus negative paths:

- Invalid URL scheme → `422`
- Empty URL → `422`
- Duplicate custom alias → `409`
- Unknown short code on redirect and analytics → `404`
- Multiple clicks accumulate correctly
- Copilot endpoint validation (`422` on too-short requirement text)

**Manual end-to-end verification** performed during development: backend
started with `uvicorn`, exercised via `curl` for `/health`, `/shorten`,
redirect-without-follow, `/analytics/{code}`, and `/copilot/analyze` — all
verified against real HTTP responses, not just the test suite. Frontend
type-checked with `tsc -b` and production-built with `vite build` with zero
errors.

### Known limitations

- No authentication/authorization — all endpoints are public (documented
  scope boundary, not an oversight).
- No rate limiting on `POST /shorten` — a public deployment would need this.
- No caching layer in front of the database — every redirect is a DB read.
- Basic URL validation (scheme + length) does not fully prevent
  shortening links to malicious domains (open-redirect risk); flagged in
  `validation.security_review`, not solved here.
- The Copilot Console's analysis engine is deterministic/rule-based, not a
  live LLM call — see `ARCHITECTURE.md §1` and
  `backend/app/services/copilot_engine.py` for the reasoning and the
  intentional seam for swapping in a real model call.
- Concurrent custom-alias claims rely on the database's unique index as the
  ultimate arbiter; the losing request surfaces as `409` (verified in
  tests) but under very high concurrency this means occasional client-side
  retries, not a queued/serialized allocation.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0 |
| Database | SQLite (default) / PostgreSQL (via `DATABASE_URL`) |
| Testing | Pytest, FastAPI `TestClient`, `pytest-cov` |
| Docs | Markdown, Mermaid |



live link
https://url-shortener-ai-copilot.vercel.app/

