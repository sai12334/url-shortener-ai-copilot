# Quick Start Guide - URL Shortener AI Copilot Demo

## 5-Minute Quick Start

### 1. Start the Backend

```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Success:** You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Start the Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

**Success:** You should see:
```
VITE v5.0.0  ready in 234 ms
Local:   http://localhost:5173/
```

### 3. Open the Application

Visit: **http://localhost:5173**

---

## Demo Path 1: Web UI (Most Visual)

### Step 1: Live Demo Tab
1. Click **"Live Demo"** tab
2. Enter URL: `https://www.python.org`
3. Click **"Shorten"**
4. Copy the short link
5. Click it to test redirect
6. Click **"Refresh Analytics"** to see clicks increase

### Step 2: Copilot Console Tab
1. Click **"Copilot Console"** tab
2. Default requirement is pre-filled
3. Click **"Generate"**
4. Scroll through tabs:
   - Requirement Analysis
   - Task Decomposition
   - Engineering Artifacts
   - Validation Report
   - Risk Analysis
   - Final Summary

---

## Demo Path 2: API Testing (Using Python Script)

### Run the Demo Script

```bash
# Make sure backend is running on port 8000
python demo.py
```

**What you'll see:**
- Health check ✓
- Creating short URLs ✓
- Simulating clicks ✓
- Viewing analytics ✓
- Copilot analysis ✓

---

## Demo Path 3: Manual API Calls

### Test in Terminal/PowerShell

**Create a short URL:**
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com", "custom_alias": null}'
```

**Expected output:**
```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://www.example.com",
  "created_at": "2026-07-03T12:34:56.789Z"
}
```

**Get analytics:**
```bash
curl http://localhost:8000/analytics/abc123
```

---

## Demo Path 4: Run Tests

```bash
cd backend
pytest
```

**See all 26 tests pass!**

---

## What Each Demo Shows

| Demo | Best For | Time |
|------|----------|------|
| Web UI - Live Demo | Visual users, interactive | 5 min |
| Web UI - Copilot | Understanding AI analysis | 5 min |
| Python Script | Developers, automation | 3 min |
| Manual API Calls | Understanding endpoints | 5 min |
| Running Tests | Code quality, coverage | 2 min |

---

## Features Demonstrated

✅ **Short URL Creation**
- Auto-generated codes
- Custom aliases

✅ **URL Redirects**
- 307 temporary redirects
- Automatic click tracking

✅ **Analytics**
- Click counting
- Last-clicked timestamps
- URL metadata

✅ **Copilot Console**
- Requirement analysis
- Task decomposition
- Engineering artifacts
- Risk analysis
- Validation reports

✅ **Database**
- SQLite persistence
- Data relationships
- Query performance

✅ **Testing**
- Unit tests
- Integration tests
- Code coverage

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Try installing uvicorn separately
pip install uvicorn fastapi
```

### Port 8000 already in use
```bash
# Use different port
python -m uvicorn app.main:app --reload --port 8001

# Update frontend vite.config.ts proxy target
```

### Frontend can't reach backend
```bash
# Make sure backend is running
curl http://localhost:8000/health

# Check vite proxy config in frontend/vite.config.ts
```

### npm install fails
```bash
# Clear cache
npm cache clean --force
npm install
```

---

## Repository Links

- **GitHub**: https://github.com/sai12334/url-shortener-ai-copilot
- **API Docs**: http://localhost:8000/docs (when running)
- **Full Documentation**: See `DEMO_GUIDE.md`

---

## Next Steps After Demo

1. **Explore the code** - Check backend and frontend architecture
2. **Modify the demo requirement** - Try custom requirements in Copilot
3. **Add new features** - Extend the URL shortener functionality
4. **Deploy** - Push to production using Docker, Vercel, or Heroku

---

**Enjoy exploring the URL Shortener AI Copilot!** 🚀
