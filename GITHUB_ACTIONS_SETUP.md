# ✅ GITHUB ACTIONS SETUP GUIDE

## 🎯 YOUR QUESTION

**Q: Should I copy-paste the code in daily-scan.yml or just add environment variables?**

**A: Just add environment variables! ✅ The YAML file is already perfect!**

---

## ✅ WHAT'S ALREADY DONE

### GitHub Actions Workflow File ✅
**File:** `.github/workflows/daily-scan.yml`

**Status:** ✅ **ALREADY CONFIGURED - NO CHANGES NEEDED!**

**What it does:**
- ✅ Runs daily at 12:00 PM UTC
- ✅ Can be triggered manually
- ✅ Installs Python dependencies
- ✅ Runs daily scan
- ✅ Uses environment variables from secrets

**Code is correct:** ✅ **DO NOT MODIFY**

---

## 🔧 WHAT YOU NEED TO DO

### ONLY Add GitHub Secrets (3 Variables)

**Step 1: Go to GitHub Repository**
1. Visit: `https://github.com/YOUR_USERNAME/ai-tool-tracker`
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"

**Step 2: Add These 3 Secrets**

#### Secret 1: SUPABASE_URL
```
Name: SUPABASE_URL
Value: https://xxxxx.supabase.co
```

#### Secret 2: SUPABASE_SERVICE_ROLE_KEY
```
Name: SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Secret 3: HUGGINGFACE_API_KEY
```
Name: HUGGINGFACE_API_KEY
Value: hf_xxxxxxxxxxxxx
```

**That's it!** ✅

---

## 📋 VERIFICATION

### Check Your YAML File ✅
**File:** `.github/workflows/daily-scan.yml` (lines 28-31)

```yaml
env:
  SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
  SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
  HUGGINGFACE_API_KEY: ${{ secrets.HUGGINGFACE_API_KEY }}
```

**Status:** ✅ **CORRECT - Matches secret names**

---

## 🎯 WHAT HAPPENS

### Automatic Daily Scan:
```
1. Every day at 12:00 PM UTC
2. GitHub Actions starts workflow
3. Installs Python dependencies
4. Runs daily_job.run_daily_scan()
5. Scrapes GitHub + Hugging Face
6. Analyzes tools with AI
7. Stores in Supabase database
8. Your frontend shows new tools!
```

### Manual Trigger:
```
1. Go to GitHub → Actions tab
2. Click "Daily AI Tool Scan"
3. Click "Run workflow"
4. Select branch (main)
5. Click "Run workflow" button
6. Scan runs immediately!
```

---

## ✅ CHECKLIST

### GitHub Secrets (Required):
- [ ] `SUPABASE_URL` added
- [ ] `SUPABASE_SERVICE_ROLE_KEY` added
- [ ] `HUGGINGFACE_API_KEY` added

### YAML File (Already Done):
- [x] Workflow file exists
- [x] Schedule configured (12:00 PM UTC)
- [x] Manual trigger enabled
- [x] Environment variables mapped
- [x] Python setup correct
- [x] Dependencies install command correct
- [x] Scan command correct

---

## 🚀 HOW TO TEST

### Test Immediately (Manual Trigger):

1. **Go to GitHub Actions:**
   - Repository → Actions tab
   - Click "Daily AI Tool Scan" workflow

2. **Run Workflow:**
   - Click "Run workflow" dropdown
   - Select "main" branch
   - Click green "Run workflow" button

3. **Watch Progress:**
   - Click on the running workflow
   - See real-time logs
   - Check for errors

4. **Verify Results:**
   - Check Supabase database
   - Should see new tools added
   - Check frontend for new tools

---

## 📊 COMPARISON

| Action | Need to Do? | Status |
|--------|-------------|--------|
| Modify YAML file | ❌ NO | Already correct |
| Copy-paste code | ❌ NO | Already done |
| Add GitHub secrets | ✅ YES | Required |
| Push to GitHub | ✅ YES | If not already |
| Test workflow | ✅ YES | Recommended |

---

## 🎯 STEP-BY-STEP GUIDE

### Step 1: Add GitHub Secrets (5 minutes)

**Navigate:**
```
GitHub Repository
  → Settings
    → Secrets and variables
      → Actions
        → New repository secret
```

**Add 3 secrets:**
1. `SUPABASE_URL`
2. `SUPABASE_SERVICE_ROLE_KEY`
3. `HUGGINGFACE_API_KEY`

---

### Step 2: Verify YAML File (1 minute)

**Check:** `.github/workflows/daily-scan.yml`

**Should have:**
```yaml
env:
  SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
  SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
  HUGGINGFACE_API_KEY: ${{ secrets.HUGGINGFACE_API_KEY }}
```

**Status:** ✅ Already correct - no changes needed

---

### Step 3: Test Workflow (2 minutes)

**Manual trigger:**
1. Actions tab
2. Daily AI Tool Scan
3. Run workflow
4. Watch logs

**Expected output:**
```
✓ Checkout code
✓ Set up Python
✓ Install dependencies
✓ Run daily scan
  - Running Hugging Face ingestion...
  - Running GitHub ingestion...
  - Found X tools discovered today
✓ Scan complete
```

---

## ⚠️ IMPORTANT NOTES

### DO NOT Modify YAML File ✅
- File is already correct
- Environment variables properly mapped
- Schedule configured correctly
- Manual trigger enabled

### ONLY Add Secrets ✅
- Add 3 GitHub secrets
- Use exact names shown above
- Get values from Supabase/Hugging Face

### Test Before Relying On It ✅
- Run manual trigger first
- Check logs for errors
- Verify database has new tools
- Then let it run automatically

---

## 🐛 TROUBLESHOOTING

### Workflow Fails?

**Check:**
1. All 3 secrets added? ✅
2. Secret names match YAML? ✅
3. Supabase credentials correct? ✅
4. Hugging Face key valid? ✅

**View logs:**
- Actions tab → Click failed workflow → View logs

### No New Tools?

**Possible reasons:**
1. Tools already in database (duplicates skipped)
2. No new trending tools today
3. Scraping blocked (rare)

**Check:**
- Workflow logs for "inserted" count
- Supabase database for new entries

---

## ✅ SUMMARY

### What You Need to Do:
1. ✅ Add 3 GitHub secrets
2. ✅ Test manual trigger
3. ✅ Done!

### What You DON'T Need to Do:
- ❌ Modify YAML file (already correct)
- ❌ Copy-paste code (already done)
- ❌ Change workflow schedule (already set)

### Result:
- ✅ Daily automatic scans at 12:00 PM UTC
- ✅ Manual trigger available anytime
- ✅ New tools added to database daily
- ✅ Frontend shows fresh tools

---

## 🎉 FINAL ANSWER

**Q: Should I copy-paste code or just add env variables?**

**A: JUST ADD ENVIRONMENT VARIABLES! ✅**

**The YAML file is already perfect. Just add 3 GitHub secrets and you're done!**

---

## 📝 QUICK REFERENCE

**GitHub Secrets to Add:**
```
1. SUPABASE_URL
2. SUPABASE_SERVICE_ROLE_KEY
3. HUGGINGFACE_API_KEY
```

**Where to Add:**
```
Repository → Settings → Secrets and variables → Actions
```

**Test:**
```
Repository → Actions → Daily AI Tool Scan → Run workflow
```

**That's all you need!** 🚀
