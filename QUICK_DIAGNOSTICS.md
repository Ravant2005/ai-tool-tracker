# Quick Diagnostics Checklist

## Run Manual Scan and Check These Logs

### PHASE 1: Scraping Results
Look for this pattern:
```
📡 PHASE 1: WEB SCRAPING
[1/4] 🔍 Scraping GitHub Trending...
✅ GitHub: [X] repos found
```

**Expected**:
- GitHub: 5-20 repos
- Product Hunt: 0-2 products (JS-rendered limitation)
- HF Models: 10-15 models
- HF Spaces: 3-10 spaces
- **Total: 20-40 tools**

**If you see 0 in all sources** → Network issue or API keys missing

---

### PHASE 2: Analysis Results
Look for:
```
📊 ANALYSIS SUMMARY:
   Successfully analyzed: [X]/[Y]
   Failed: [N]
```

**Expected**:
- X should equal Y (all tools analyzed)
- Failed = 0 (unless Hugging Face API key missing)

**If Failed > 0** → Check HUGGINGFACE_API_KEY in .env

---

### PHASE 3: Database Results
Look for:
```
📊 FINAL SUMMARY:
   Phase 3 (Database):
      • ✅ New tools saved: [N]
      • 🔄 Existing tools updated: [M]
      • ⏭️  Duplicates skipped: [K]
      • ❌ Insert/Update failed: [F]
```

**Expected on first scan**:
- New tools saved: 15-25
- Existing: 0 (first run)
- Failed: 0

**Expected on subsequent scans**:
- New tools saved: 5-15 (overlapping tools)
- Existing updated: 10-20 (hype scores change)
- Failed: 0

**If Failed > 0** → Supabase connection issue

---

## Error Messages & Meanings

| Error | Cause | Fix |
|-------|-------|-----|
| `❌ HTTP Error: ConnectionError` | Network issue | Check internet, firewall |
| `❌ HTTP Error: Timeout` | Site too slow or blocked | Wait/retry, check IP block |
| `❌ HTTP Error: 403` | Blocked by site | Add delays between requests |
| `⚠️ Product Hunt: 0 products` | JS rendering | Normal; use GraphQL API in future |
| `❌ Analysis failed: APIError` | HF API down | Check their status page |
| `❌ Error saving tool: ConnectionError` | Supabase down | Check Supabase dashboard |
| `❌ Insert returned empty response` | DB insert succeeded but no data | Rare; check DB schema |

---

## Environment Variables Check

```bash
# In backend/.env (or Render dashboard)

# Required for scraping
USER_AGENT=Mozilla/5.0...  # Optional but helpful

# Required for AI analysis (optional - falls back to truncation)
HUGGINGFACE_API_KEY=hf_...

# Required for database
SUPABASE_URL=https://...supabase.co
SUPABASE_KEY=eyJ0...
```

Test if they're loaded:
```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('SUPABASE_URL:', 'OK' if os.getenv('SUPABASE_URL') else 'MISSING')"
```

---

## Common Scenarios

### ✅ Everything Working
```log
Phase 1: Total tools collected: 35
Phase 2: Successfully analyzed: 35/35
Phase 3: New tools saved: 15
         Existing updated: 20
```
✅ Check `/api/tools` - should see new tools

---

### 🔴 GitHub Broken
```log
[1/4] 🔍 Scraping GitHub Trending...
   ✅ GitHub HTTP 403
   📊 Found 0 total trending repos on page
```
**Cause**: GitHub blocking requests  
**Fix**: Add longer delays, rotate user-agents, or use GitHub API

---

### 🟡 Product Hunt 0 Results (Normal)
```log
[2/4] 🔍 Scraping Product Hunt...
⚠️ Note: Product Hunt uses heavy JavaScript rendering
💡 For production: Use Product Hunt GraphQL API
✅ Product Hunt: 0 products found
```
**Cause**: Product Hunt is JS-rendered, not HTML-scrapable  
**Fix**: Expected behavior; implement GraphQL API instead

---

### 🔴 HuggingFace Models Broken
```log
[3/4] 🔍 Scraping HF Models...
   ❌ HTTP Error: 401
   Error: Invalid token
```
**Cause**: Bad/missing HUGGINGFACE_API_KEY  
**Fix**: Get key from https://huggingface.co/settings/tokens

---

### 🔴 Database Connection Broken
```log
Phase 3: New tools saved: 0
❌ Error saving tool: ProgrammingError
   Error: connection refused
```
**Cause**: Supabase offline or bad credentials  
**Fix**: Verify SUPABASE_URL and SUPABASE_KEY

---

## Verify Data Was Saved

```bash
# From frontend directory
curl http://localhost:8000/api/tools | jq '.[0]'

# Should show:
{
  "id": 1,
  "name": "Tool Name",
  "description": "...",
  "hype_score": 75,
  "category": "NLP",
  "pricing": "freemium",
  ...
}
```

If empty: `[]`  
→ Run manual scan again, check logs

---

## Performance Baselines

| Metric | Expected Time |
|--------|---|
| Scraping Phase 1 | 30-60 seconds |
| Analysis Phase 2 | 15-30 seconds (depends on HF API) |
| Database Phase 3 | 5-10 seconds |
| **Total** | **50-100 seconds** |

If much slower:
- HF API rate limited
- Supabase slow response
- Network latency

---

## Debug Flag: Detailed Output

To see extra debug logs, in `main.py`:

```python
# Change from:
logging.basicConfig(level=logging.INFO)

# To:
logging.basicConfig(level=logging.DEBUG)

# Then you'll see:
DEBUG: HF URL: https://huggingface.co/api/models
DEBUG: Searching for tool: 'ChatGPT'
DEBUG: Found existing tool: ChatGPT
```

---

## Next Steps After Verification

1. **Test endpoint**: `POST /api/scan/manual`
2. **Check logs**: Watch for Phase 1 → 2 → 3 progression
3. **Verify data**: `GET /api/tools` shows new tools
4. **Monitor**: Periodically check `/api/scan/manual` returns meaningful data

---

## When to Contact Support

**Provide these details**:
1. Full log output from one manual scan
2. Which phase failed (Scraping/Analysis/Database)
3. Exact error message from logs
4. `.env` file (without secrets):
   ```
   USER_AGENT=Mozilla/5.0...
   HUGGINGFACE_API_KEY=hf_[REDACTED]
   SUPABASE_URL=https://[PROJECT_ID].supabase.co
   SUPABASE_KEY=eyJ[REDACTED]
   ```

---

## Key Takeaway

**The logging now makes debugging trivial**:

❌ **Before**: "Manual scan completed" → Check database → Still only 3 tools

✅ **After**: "Phase 1: Found 0 tools" → Immediately know GitHub scraper broken

The phase-by-phase breakdown pinpoints exactly where tools are lost in the pipeline.
