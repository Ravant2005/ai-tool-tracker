# 🚀 PRODUCTION DEPLOYMENT GUIDE

## ⚠️ CRITICAL: Static Rendering Issue - RESOLVED

### Problem
Next.js App Router was **statically generating** the homepage at build time, causing:
- Homepage showed "0 tools" in production
- API calls executed during build, not runtime
- Wrong/empty data baked into static HTML
- Production never refetched data

### Root Cause
1. Next.js defaults to static rendering
2. Client components (`'use client'`) don't prevent static generation
3. Environment variables resolved at build time
4. Data frozen in static HTML

### Solution Applied
✅ Added `export const dynamic = 'force-dynamic'` to root layout
✅ Added `export const revalidate = 0` to prevent caching
✅ Configured axios with no-cache headers
✅ Strict environment variable enforcement (no fallbacks)
✅ Environment-aware backend logging

## 🔧 VERCEL DEPLOYMENT

### Required Environment Variables
```
NEXT_PUBLIC_API_BASE_URL=https://ai-tool-tracker-backend.onrender.com
```

**CRITICAL:** Must be set in:
- Production
- Preview  
- Development

### Deployment Steps
1. Set environment variable in Vercel dashboard
2. Trigger **FULL REDEPLOY** (not cached build)
3. Verify build logs show dynamic rendering
4. Test on multiple devices

### Verification
After deployment, check:
- ✅ Console shows: `🔗 API Base URL: https://ai-tool-tracker-backend.onrender.com`
- ✅ Network tab shows API calls to Render backend
- ✅ Tools display correctly (not "0 tools")
- ✅ Works on mobile/incognito/other devices

## 🔍 DEBUGGING

### If Frontend Shows 0 Tools
1. Check browser console for API URL
2. Check Network tab for failed requests
3. Verify CORS allows your Vercel domain
4. Ensure environment variable is set
5. Force full redeploy (clear cache)

### Build Logs
Look for:
- ✅ `ƒ (Dynamic)` - Page is dynamically rendered
- ❌ `○ (Static)` - Page is statically generated (BAD)

## 🎯 ARCHITECTURE

```
GitHub Actions → Supabase (data storage)
                     ↓
Render Backend → Reads from Supabase
                     ↓
Vercel Frontend → Calls Render API (runtime)
```

## 📋 CHECKLIST

- [x] Root layout has `dynamic = 'force-dynamic'`
- [x] No localhost fallbacks in code
- [x] Environment variables strictly enforced
- [x] CORS allows Vercel domain
- [x] Backend logging is environment-aware
- [x] Health check endpoint exists
- [ ] Vercel environment variable set
- [ ] Full redeploy triggered
- [ ] Production verified on multiple devices