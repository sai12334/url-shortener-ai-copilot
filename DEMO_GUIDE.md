# URL Shortener AI Copilot - Complete Demo Guide

This guide walks through all features of the URL Shortener AI Copilot application.

## Overview

The application demonstrates AI-assisted software engineering with two main components:

1. **Copilot Console** - AI-powered requirement analysis and task decomposition
2. **Live Demo** - Functional URL shortener service with analytics

---

## Prerequisites & Setup

### Step 1: Install Backend Dependencies

```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Start Backend Server

```bash
# Make sure you're in the backend directory with venv activated
python -m uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
```

Backend API Docs: http://localhost:8000/docs

### Step 3: Start Frontend Server

```bash
cd frontend
npm install
npm run dev
```

**Expected Output:**
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Frontend App: http://localhost:5173

---

## Feature Demonstrations

### Feature 1: API Health Check

**Endpoint:** `GET /health`

**cURL Command:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0"
}
```

---

### Feature 2: Create a Short URL

**Endpoint:** `POST /shorten`

**Request:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://www.example.com/very/long/path/that/needs/shortening",
    "custom_alias": null
  }'
```

**Expected Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://www.example.com/very/long/path/that/needs/shortening",
  "short_url": "http://localhost:8000/abc123",
  "created_at": "2026-07-03T12:34:56.789Z"
}
```

**With Custom Alias:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://github.com/sai12334/url-shortener-ai-copilot",
    "custom_alias": "myrepo"
  }'
```

**Expected Response:**
```json
{
  "short_code": "myrepo",
  "original_url": "https://github.com/sai12334/url-shortener-ai-copilot",
  "short_url": "http://localhost:8000/myrepo",
  "created_at": "2026-07-03T12:34:56.789Z"
}
```

---

### Feature 3: Redirect to Original URL

**Endpoint:** `GET /{shortCode}`

**Request:**
```bash
curl -L http://localhost:8000/abc123
```

**Expected Response:**
- HTTP 307 (Temporary Redirect) to the original URL
- A click is recorded in the analytics database

**Browser Demo:**
1. Copy the `short_url` from Feature 2
2. Paste into your browser
3. You'll be redirected to the original URL
4. A click event is recorded in the database

---

### Feature 4: View Analytics

**Endpoint:** `GET /analytics/{shortCode}`

**Request:**
```bash
curl http://localhost:8000/analytics/abc123
```

**Expected Response:**
```json
{
  "short_code": "abc123",
  "original_url": "https://www.example.com/very/long/path/that/needs/shortening",
  "total_clicks": 3,
  "last_clicked": "2026-07-03T12:45:30.123Z",
  "created_at": "2026-07-03T12:34:56.789Z"
}
```

**Multiple Clicks Demo:**
1. Create a short URL (Feature 2)
2. Visit the short link multiple times (Feature 3)
3. Check analytics each time to see the click counter increase

---

### Feature 5: Copilot Console - Requirement Analysis

**In Browser:**

1. Go to http://localhost:5173
2. Click on the **"Copilot Console"** tab
3. The default requirement is pre-filled:
   ```
   Build a scalable URL shortener service with APIs, persistence, and analytics.
   ```
4. Click **"Generate"** button

**Expected Output Sections:**

#### A. Requirement Analysis
```
✓ Core Requirements Identified
  - URL shortening capability
  - Persistent storage
  - Analytics tracking
  
✓ Success Criteria
  - API endpoints working correctly
  - Database persists data
  - Click tracking functional

✓ Constraints
  - Database system selection
  - API rate limiting
```

#### B. Task Decomposition
```
Tasks Identified:
1. Design database schema
   - Create URL mappings table
   - Create analytics table
   - Add indexes for performance
   
2. Implement API endpoints
   - POST /shorten endpoint
   - GET /{shortCode} redirect
   - GET /analytics endpoint
   
3. Add persistence layer
   - Setup SQLite/PostgreSQL
   - Create ORM models
   - Add database migrations
```

#### C. Engineering Artifacts
```
Generated Code Artifacts:
- Database schema (SQL)
- API route definitions (Python)
- Service layer code
- Data models/schemas
```

#### D. Validation Report
```
Validation Checks:
✓ API endpoints implemented
✓ Database schema matches requirements
✓ Analytics functionality working
✓ Error handling in place
✓ Tests pass: 26/26
```

#### E. Risk Analysis
```
Identified Risks:
- High: Database performance at scale
  Mitigation: Add indexing, caching layer
  
- Medium: URL collision risk
  Mitigation: Use random generation algorithm
  
- Low: API rate limiting
  Mitigation: Add rate limiting middleware
```

#### F. Final Summary
```
Engineering Summary:
✓ All requirements met
✓ System is production-ready
✓ Test coverage: 89%
✓ Code quality: Good
✓ Performance: Acceptable
```

---

### Feature 6: Live Demo Tab - Interactive Testing

**In Browser:**

1. Go to http://localhost:5173
2. Click on the **"Live Demo"** tab

**Demo Walkthrough:**

**Step 1: Create a Short URL**
- Input URL: `https://www.google.com`
- Optional Alias: leave blank (auto-generated)
- Click **"Shorten"** button

**Expected Output:**
```
✓ Short URL created successfully!

Original URL:   https://www.google.com
Short Code:     xyz789
Short Link:     http://localhost:8000/xyz789
Created At:     2026-07-03 12:34:56 PM
```

**Step 2: Share the Short Link**
- Copy the short link
- The link is now ready to share

**Step 3: Track Clicks**
- Click the short link to test the redirect
- You'll be taken to Google
- Click **"Refresh Analytics"** in the demo tab

**Expected Output:**
```
Analytics for xyz789:
├── Total Clicks:        1
├── Created:            2026-07-03 12:34:56 PM
└── Last Clicked:       2026-07-03 12:35:45 PM
```

**Step 4: Multiple Clicks Test**
- Click the short link 3-5 more times
- Refresh analytics
- See the click counter increase

**Expected Output:**
```
Analytics for xyz789:
├── Total Clicks:        5
├── Created:            2026-07-03 12:34:56 PM
└── Last Clicked:       2026-07-03 12:36:22 PM
```

**Step 5: Custom Alias**
- Input URL: `https://github.com/sai12334/url-shortener-ai-copilot`
- Custom Alias: `myproject`
- Click **"Shorten"**

**Expected Output:**
```
✓ Short URL created successfully!

Original URL:   https://github.com/sai12334/url-shortener-ai-copilot
Short Code:     myproject
Short Link:     http://localhost:8000/myproject
Created At:     2026-07-03 12:37:01 PM
```

---

## Running Automated Tests

### Run All Tests

```bash
cd backend
pytest
```

**Expected Output:**
```
========================= test session starts ==========================
collected 26 items

tests/test_unit_shortener.py::test_generate_short_code PASSED        [ 3%]
tests/test_unit_shortener.py::test_shorten_url PASSED                [ 7%]
tests/test_unit_shortener.py::test_custom_alias PASSED               [11%]
tests/test_integration_api.py::test_shorten_endpoint PASSED          [15%]
tests/test_integration_api.py::test_redirect_endpoint PASSED         [19%]
tests/test_integration_api.py::test_analytics_endpoint PASSED        [23%]
... (26 tests total)

======================== 26 passed in 2.34s ===========================
```

### Run with Coverage

```bash
pytest --cov=app
```

**Expected Output:**
```
Name                    Stmts   Miss  Cover
-------------------------------------------
app/__init__.py             1      0   100%
app/config.py              15      0   100%
app/database.py            28      2    93%
app/main.py                35      3    91%
app/models.py              22      0   100%
app/schemas.py             18      0   100%
app/routers/urls.py        45      2    96%
app/routers/copilot.py     52      5    90%
app/services/shortener.py  35      0   100%
app/services/copilot_engine.py  68      8    88%
-------------------------------------------
TOTAL                     319     20    94%
```

---

## Demo Scenarios

### Scenario 1: Quick Start (5 minutes)

1. Start backend and frontend
2. Go to Live Demo tab
3. Shorten a URL
4. Click the short link
5. View analytics showing 1 click

### Scenario 2: Copilot Console Deep Dive (10 minutes)

1. Go to Copilot Console tab
2. Paste the requirement
3. Click Generate
4. Walk through each tab:
   - Requirement Analysis
   - Task Decomposition
   - Engineering Artifacts
   - Validation Report
   - Risk Analysis
   - Final Summary

### Scenario 3: Full Feature Test (15 minutes)

1. **Create URLs:**
   - Auto-generated alias
   - Custom alias
   - Different domains

2. **Test Redirects:**
   - Click each short link
   - Verify redirect works

3. **Analytics:**
   - View click counts
   - Verify last-clicked timestamps
   - Multiple visits increase counter

4. **Run Tests:**
   - Run pytest suite
   - View coverage report

### Scenario 4: Custom Requirement (15 minutes)

1. Go to Copilot Console
2. Modify the requirement to something custom, e.g.:
   ```
   Build an API that tracks user login events with timestamps,
   daily active user counts, and geographic information.
   ```
3. Click Generate
4. Watch the Copilot analyze your custom requirement
5. Review the generated artifacts

---

## API Reference Summary

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/health` | GET | Check API health | None |
| `/shorten` | POST | Create short URL | None |
| `/{shortCode}` | GET | Redirect to original | None |
| `/analytics/{shortCode}` | GET | Get click analytics | None |
| `/copilot/analyze` | POST | AI requirement analysis | None |

---

## Database

### Schema Overview

**URLs Table:**
```sql
CREATE TABLE urls (
  id INTEGER PRIMARY KEY,
  short_code TEXT UNIQUE NOT NULL,
  original_url TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Analytics Table:**
```sql
CREATE TABLE analytics (
  id INTEGER PRIMARY KEY,
  short_code TEXT NOT NULL,
  clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (short_code) REFERENCES urls(short_code)
);
```

**Database File:** `backend/url_shortener.db` (SQLite)

---

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # macOS/Linux

# Kill process or use different port:
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend won't connect to backend

- Ensure backend is running on port 8000
- Check `frontend/vite.config.ts` proxy configuration
- Verify CORS headers are correct

### Database errors

```bash
# Delete old database and start fresh:
cd backend
rm url_shortener.db
python -m uvicorn app.main:app --reload --port 8000
```

### Tests fail

```bash
cd backend
pytest -v  # verbose output
pytest --tb=short  # shorter traceback
```

---

## Next Steps

After trying the demo:

1. **Explore the code:**
   - `backend/app/services/shortener.py` - Core shortening logic
   - `backend/app/services/copilot_engine.py` - AI analysis logic
   - `frontend/src/components/` - React components

2. **Modify and experiment:**
   - Change the default requirement
   - Add new endpoints
   - Customize the UI

3. **Deploy:**
   - Push changes to GitHub
   - Deploy backend to hosting service
   - Deploy frontend to CDN

---

## Video Walkthrough (if creating a video)

**Timestamps:**
- 0:00 - Introduction
- 0:30 - Backend setup
- 1:00 - Frontend setup  
- 1:30 - Live Demo tab walkthrough
- 3:00 - Creating short URLs
- 4:30 - Testing redirects & analytics
- 6:00 - Copilot Console tab
- 8:00 - Running tests
- 9:00 - Conclusion

---

**Repository:** https://github.com/sai12334/url-shortener-ai-copilot

**Questions or issues?** Check the README.md or open an issue on GitHub!
