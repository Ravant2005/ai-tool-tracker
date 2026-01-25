# TODO: Fix Supabase JSON Serialization Issue

## Problem
- GitHub Actions scan finds 14 AI tools but Supabase inserts fail
- Error: "Object of type Url is not JSON serializable"
- New tools saved: 0, frontend shows only 3 old tools

## Root Cause Analysis
1. `_normalize_dict()` function is referenced in `connection.py` but never defined
2. URL fields may contain Pydantic `Url` or `HttpUrl` objects that aren't JSON serializable
3. Supabase client requires pure Python dicts with string values

## Solution Plan

### Step 1: Fix connection.py - Add _normalize_dict function
Location: `/home/s-ravant-vignesh/Documents/ai-tool-tracker/backend/database/connection.py`

Add a helper function that:
- Converts all `Url`/`HttpUrl` objects to strings
- Handles datetime objects by converting to ISO format strings
- Handles any other non-serializable types recursively

### Step 2: Verify models.py URL handling
Location: `/home/s-ravant-vignesh/Documents/ai-tool-tracker/backend/database/models.py`

Ensure the validator properly converts URL objects to strings before serialization.

### Step 3: Verify all ingest files use proper data types
- `github_ingest.py`
- `huggingface_ingest.py`
- `producthunt_ingest.py`

### Step 4: Test the fix
Run the scrapers locally to verify inserts work.

## Files to Modify
1. `backend/database/connection.py` - Add `_normalize_dict()` function
2. `backend/database/models.py` - Fix URL validator imports (if needed)

## Success Criteria
- All 14 tools from GitHub Actions scan are saved to Supabase
- No "Url is not JSON serializable" errors
- Frontend displays all tools correctly

