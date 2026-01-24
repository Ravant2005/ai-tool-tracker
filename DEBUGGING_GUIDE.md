# AI Tool Tracker - Debugging & Fix Guide

## Problem Summary
The `/api/scan/manual` endpoint always returned "success" but only 3 tools were ever in the database. New tools were not being discovered despite multiple manual scans.

## Root Causes Identified

### 1. **Silent Exception Swallowing** (Critical)
**Issue**: All scrapers caught exceptions but returned empty lists without detailed error messages.

**Impact**: 
- No visibility into why scraping failed
- API always returned "success" even when scrapers found 0 tools
- Impossible to debug without reading logs

**Fixed by**: Enhanced logging with exception types and stack traces

---

### 2. **Product Hunt Scraper Broken** (Major)
**Issue**: Product Hunt heavily relies on JavaScript rendering. HTML scraping returns 0 results.

**Impact**:
- 0 products ever added to database
- Silent failure - logs showed "Found 0 products" with no explanation

**Fixed by**: 
- Added warning messages about JS rendering
- Improved error handling
- Suggested GraphQL API as alternative

**Recommendation**: Implement Product Hunt GraphQL API
```python
# Future improvement - use their official API
# https://api.producthunt.com/graphql
```

---

### 3. **Missing Debug Logging** (Major)
**Issue**: No logs showing:
- Number of tools found at each scraping stage
- Which tools passed/failed AI analysis
- Duplicate detection results
- Database insert success/failure

**Impact**: Impossible to determine where tools were lost in the pipeline

**Fixed by**: Added comprehensive phase-by-phase logging:
```
[Scraping Phase] → [Analysis Phase] → [Database Phase]
   ✅ GitHub: N repos
   ✅ HF Models: M models
   ...→ [Analyzed N/M tools] →  [Saved X, Updated Y, Skipped Z]
```

---

### 4. **No URL Validation** (Minor)
**Issue**: Tools with invalid or missing URLs got placeholder URLs like `https://example.com`

**Fixed by**: Added URL validation in database insert logic

---

## Changes Made

### 1. Enhanced Scraper Error Handling
**File**: `backend/scraper/github_scraper.py`, `huggingface_scraper.py`, `producthunt_scraper.py`

Added:
- Exception type logging (`type(e).__name__`)
- Stack trace inclusion (`exc_info=True`)
- HTTP response code logging
- Parse error counts
- Detailed info about each tool found

**Example**:
```python
except requests.exceptions.RequestException as e:
    logger.error(f"❌ HTTP Error: {type(e).__name__}: {str(e)}")
    return []
except Exception as e:
    logger.error(f"❌ Error: {type(e).__name__}: {str(e)}", exc_info=True)
    return []
```

---

### 2. Comprehensive Daily Job Logging
**File**: `backend/scheduler/daily_job.py`

Added detailed phase reporting:

```
PHASE 1: WEB SCRAPING
  [1/4] GitHub: 12 repos found
  [2/4] Product Hunt: 0 products found
  [3/4] HF Models: 15 models found
  [4/4] HF Spaces: 8 spaces found
  Total: 35 tools

PHASE 2: AI ANALYSIS & ENRICHMENT
  [1/35] Analyzing: Tool A
    ✅ Hype Score: 75/100
    📂 Category: NLP
    💰 Pricing: freemium
  [2/35] Analyzing: Tool B
    ✅ Hype Score: 82/100
  ...
  Successfully analyzed: 35/35

PHASE 3: DATABASE STORAGE
  ✅ New tools saved: 15
  🔄 Existing tools updated: 20
  ⏭️  Duplicates skipped: 0
  ❌ Insert/Update failed: 0
```

---

### 3. Improved Database Logging
**File**: `backend/database/connection.py`

Added:
- Tool ID on successful insert
- Empty response detection
- Better error messages on failure
- Duplicate search logging (debug level)

---

### 4. Manual Scan Endpoint Improvements
**File**: `backend/main.py`

Enhanced response with:
- Clear success/failure indication
- Timestamp
- Tip to check logs for details
- Reference to `/api/scan/test` endpoint

---

## How to Debug Issues

### Step 1: Check Real-Time Logs
```bash
# If running locally with reload
python backend/main.py

# Watch for PHASE 1 scraping results
# Each scraper should log found items
```

### Step 2: Look for These Signals

**✅ Everything Working**:
```
Phase 1: Total tools collected: 35
Phase 2: Successfully analyzed: 35/35
Phase 3: New tools saved: 15
```

**⚠️ Scraping Failing**:
```
Phase 1: Total tools collected: 0
❌ HTTP Error scraping GitHub: ConnectionError
⚠️ Note: Product Hunt uses heavy JavaScript rendering. Results may be limited.
```

**⚠️ Analysis Failing**:
```
Phase 2: Successfully analyzed: 5/35
        Failed: 30
```

**⚠️ Database Failing**:
```
Phase 3: Insert/Update failed: 10
❌ Error saving tool 'X': ConnectionRefusedError: Supabase offline
```

### Step 3: Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `0 tools collected` | All scrapers failing | Check API keys, network connectivity, website structure changes |
| `0 PH products` | GitHub still works, PH fails | Product Hunt is JS-rendered; use GraphQL API instead |
| `Analysis failed` | Hugging Face API issue | Check HUGGINGFACE_API_KEY in `.env` |
| `Insert failed` | Database issue | Verify SUPABASE_URL and SUPABASE_KEY |
| `Duplicates skipped: 50` | All tools already exist | Expected after many scans; check hype_score updates |

---

## Testing the Fix

### Quick Test (3-5 tools)
```bash
curl -X POST http://localhost:8000/api/scan/test
```

Check logs for:
- ✅ GitHub repos parsed
- ✅ HF models fetched
- ✅ Analysis successful
- ✅ Database insert worked

### Full Scan (30+ tools)
```bash
curl -X POST http://localhost:8000/api/scan/manual
```

Check Render logs or local output for complete phase breakdown.

### Verify in Frontend
```
GET /api/tools        # Should show all tools
GET /api/tools/trending  # Should show today's new tools
```

---

## Future Improvements

### 1. Product Hunt: Switch to GraphQL API
```python
# Current: HTML scraping (unreliable)
# Future: Use official GraphQL API
https://api.producthunt.com/graphql
```

### 2. Better Fallback Sources
- Hacker News / Show HN
- Twitter API for AI tool announcements
- Reddit /r/MachineLearning daily discussions
- GitHub trending with better filtering

### 3. Retry Logic
```python
# Add exponential backoff for failed scrapers
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def scrape_trending_ai_repos(self):
    ...
```

### 4. Rate Limiting Awareness
```python
# Some sites block frequent requests
# Add configurable delays per source
self.delay = {
    'github': 0.5,
    'producthunt': 2.0,  # More aggressive blocking
    'huggingface': 0.2
}
```

### 5. Prometheus Metrics
```python
# Track success/failure rates over time
from prometheus_client import Counter, Histogram

scrape_duration = Histogram('scraper_duration_seconds', 'Scraper duration')
tools_found = Counter('tools_found_total', 'Tools found', ['source'])
scrape_failures = Counter('scrape_failures_total', 'Scrape failures', ['source', 'error_type'])
```

---

## Log File Locations

- **Local**: Console output from `python backend/main.py`
- **Render**: https://dashboard.render.com → Logs tab
- **Docker**: `docker logs <container-id>`

---

## Questions to Ask When Debugging

1. **How many tools were collected in Phase 1?**
   - 0? → Scrapers failing
   - <20? → Some scrapers working, others broken
   - >30? → Scraping healthy

2. **How many tools were analyzed in Phase 2?**
   - Same as Phase 1? → Analysis OK
   - Much less? → AI analysis failing

3. **How many tools were saved to DB in Phase 3?**
   - Most of Phase 2 count? → Database working
   - 0? → Database disconnected or insert error

4. **Are there error logs above the summary?**
   - Yes? → Check type and source
   - No? → Silent failure (shouldn't happen with new logging)

---

## Summary

**Before Fix**:
- "Manual scan completed" ✅ (always successful)
- But 0 new tools added
- No idea where they were lost

**After Fix**:
- Clear phase-by-phase reporting
- Individual tool logging
- Exception details with stack traces
- Can immediately spot which scraper/phase is broken

The logging changes make debugging trivial: Run the scan, check the log, see exactly where tools were lost.
