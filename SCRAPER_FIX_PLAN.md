# AI Tool Tracker - Scraper Fix Plan

## 📊 Information Gathered

### Current State Analysis:
1. **HuggingFace Scraper** (`huggingface_scraper.py`):
   - Uses `sort=trending` which is NOT a valid Hugging Face API parameter
   - Returns empty results silently
   - Has proper parsing logic but gets no data to parse

2. **Product Hunt Scraper** (`producthunt_scraper.py`):
   - Uses BeautifulSoup HTML scraping
   - Product Hunt blocks simple HTTP requests with JS rendering
   - Likely returns 0 AI products

3. **GitHub Scraper** (`github_scraper.py`):
   - EXISTS and works well
   - NOT integrated into main.py or daily_job.py
   - NO ingestion file (`github_ingest.py` missing)

4. **Main.py**:
   - `/api/scan/manual` only calls HF and PH ingestors
   - GitHub scraper exists but is NEVER USED

### Root Cause Summary:
- ✅ API routes work
- ✅ Scheduler works  
- ✅ Database connection works
- ✅ Insert logic works
- ❌ Scrapers return empty data (HF: bad params, PH: blocked, GitHub: not integrated)

---

## 🎯 Plan: Fix Scrapers & Add GitHub Integration

### Phase 1: Fix Hugging Face Scraper
**File:** `backend/scraper/huggingface_scraper.py`

**Changes:**
1. Remove invalid `sort=trending` parameter
2. Add `sort=None` or remove the sort key entirely
3. Add manual sorting by likes after API response
4. Add logging for raw response count

```python
# OLD (BROKEN):
params = {
    'sort': 'trending',  # ❌ Invalid parameter
    'limit': limit,
    'full': 'true'
}

# NEW (FIXED):
params = {
    'limit': limit,
    'full': 'true'
}
# Then sort manually by likes
models_data = sorted(models_data, key=lambda x: x.get('likes', 0), reverse=True)
```

### Phase 2: Create GitHub Ingestion Layer
**New File:** `backend/scraper/github_ingest.py`

**Purpose:**
- Integrate the working GitHub scraper with database
- Create ingestion stats (scraped, inserted, skipped, failed)
- Follow same pattern as `huggingface_ingest.py`

### Phase 3: Update Main.py
**File:** `backend/main.py`

**Changes:**
1. Import `github_ingest`
2. Add GitHub to `/api/scan/manual` endpoint
3. Add GitHub stats to response

### Phase 4: Update Daily Job
**File:** `backend/scheduler/daily_job.py`

**Changes:**
1. Import `github_ingest`
2. Add GitHub ingestion to daily scan

### Phase 5: Add Enhanced Logging
**Files:** `huggingface_ingest.py`, `producthunt_ingest.py`

**Changes:**
1. Log raw scraped counts BEFORE processing
2. Log duplicate skips with tool names
3. Log successful inserts with details

### Phase 6: Create Test Script
**New File:** `backend/test_scrapers.py`

**Purpose:**
- Test each scraper independently
- Show raw counts for debugging
- Quick verification that scrapers work

---

## 📝 Files to Create/Edit

### New Files:
1. `backend/scraper/github_ingest.py` - GitHub ingestion layer
2. `backend/test_scrapers.py` - Test script for verification

### Modified Files:
1. `backend/scraper/huggingface_scraper.py` - Fix API params + add sorting
2. `backend/scraper/huggingface_ingest.py` - Add enhanced logging
3. `backend/scraper/producthunt_ingest.py` - Add enhanced logging
4. `backend/main.py` - Add GitHub integration
5. `backend/scheduler/daily_job.py` - Add GitHub to daily scan

---

## ✅ Expected Outcome

After fixes, `/api/scan/manual` should return:
```json
{
  "huggingface": {
    "models": {"scraped": 20, "inserted": 15, "skipped": 5},
    "spaces": {"scraped": 10, "inserted": 8, "skipped": 2}
  },
  "github": {
    "repos": {"scraped": 15, "inserted": 12, "skipped": 3}
  },
  "producthunt": {
    "scraped": 0,
    "inserted": 0
  }
}
```

**Total Expected:** ~35 new tools per scan

---

## 🔜 Followup Steps

1. Run test script to verify scrapers work
2. Trigger `/api/scan/manual` via Postman/curl
3. Check Supabase dashboard for new records
4. Verify frontend shows new tools

