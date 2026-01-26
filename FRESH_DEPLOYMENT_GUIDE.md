# 🚀 FRESH DEPLOYMENT GUIDE - Render + Netlify

## ✅ CODE CHANGES NEEDED

### 1. Update CORS for Netlify (REQUIRED)

**File:** `backend/main.py`

**Current CORS (lines 30-37):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ai-tool-tracker-six.vercel.app",  # OLD
        "https://*.vercel.app",  # OLD
    ],
```

**Change to:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://*.netlify.app",  # Netlify deployments
        "https://your-app-name.netlify.app",  # Your specific Netlify URL
    ],
```

**OR use wildcard (easier for testing):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (less secure but works everywhere)
```

---

## 🔧 DEPLOYMENT STEPS

### STEP 1: Deploy Backend on Render

#### A. Create Render Account
1. Go to https://render.com
2. Sign up with GitHub

#### B. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `ai-tool-tracker` repo

#### C. Configure Service
```
Name: ai-tool-tracker-backend
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

#### D. Add Environment Variables
Click "Environment" → "Add Environment Variable"

**REQUIRED Variables (2):**
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

**OPTIONAL Variable (for AI summaries):**
```
HUGGINGFACE_API_KEY=hf_xxxxx  # Optional - enables AI-powered summaries
```

**Note:** App works perfectly without Hugging Face key. It will use simple text truncation instead of AI summaries.

**Get Supabase Credentials:**
1. Go to https://supabase.com/dashboard
2. Select your project
3. Settings → API
4. Copy:
   - Project URL → `SUPABASE_URL`
   - service_role key → `SUPABASE_SERVICE_ROLE_KEY`

**Get Hugging Face Key (Optional):**
1. Go to https://huggingface.co
2. Sign up (free)
3. Settings → Access Tokens
4. Create token → Copy `hf_xxxxx`

#### E. Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Note your backend URL: `https://your-app-name.onrender.com`

#### F. Test Backend
```bash
curl https://your-app-name.onrender.com/health
# Should return: {"status": "healthy", "database": "healthy"}
```

---

### STEP 2: Deploy Frontend on Netlify

#### A. Create Netlify Account
1. Go to https://netlify.com
2. Sign up with GitHub

#### B. Create New Site
1. Click "Add new site" → "Import an existing project"
2. Choose "Deploy with GitHub"
3. Select `ai-tool-tracker` repository
4. Configure build settings:

```
Base directory: frontend
Build command: npm run build
Publish directory: frontend/.next
```

#### C. Add Environment Variables
Click "Site settings" → "Environment variables" → "Add a variable"

**Required Variable:**
```
Key: NEXT_PUBLIC_API_BASE_URL
Value: https://your-backend-name.onrender.com
```

**IMPORTANT:** Use your actual Render backend URL from Step 1E

#### D. Deploy
1. Click "Deploy site"
2. Wait 3-5 minutes
3. Note your frontend URL: `https://your-app-name.netlify.app`

#### E. Test Frontend
1. Visit `https://your-app-name.netlify.app`
2. Should see dashboard with tools

---

## 🔄 UPDATE CORS AFTER DEPLOYMENT

After you get your Netlify URL, update backend CORS:

1. Edit `backend/main.py` line 33:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-actual-app.netlify.app",  # Your real URL
    "https://*.netlify.app",
],
```

2. Commit and push:
```bash
git add backend/main.py
git commit -m "Update CORS for Netlify"
git push origin main
```

3. Render will auto-redeploy

---

## 📋 CHECKLIST

### Before Deployment
- [ ] Have Supabase account with project created
- [ ] Have GitHub repository pushed
- [ ] Know your Supabase URL and service role key

### Backend (Render)
- [ ] Service created
- [ ] Environment variables set (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
- [ ] Deployment successful
- [ ] `/health` endpoint returns healthy
- [ ] `/api/tools` returns data

### Frontend (Netlify)
- [ ] Site created
- [ ] Environment variable set (NEXT_PUBLIC_API_BASE_URL)
- [ ] Build successful
- [ ] Site loads in browser
- [ ] Dashboard shows tools

### Final
- [ ] CORS updated with actual Netlify URL
- [ ] Backend redeployed
- [ ] Frontend can fetch data
- [ ] Filters work
- [ ] No console errors

---

## 🐛 TROUBLESHOOTING

### Backend Issues

**"Module not found" error:**
- Check `Root Directory` is set to `backend`
- Verify `requirements.txt` exists

**"Database unhealthy":**
- Check Supabase credentials in environment variables
- Verify Supabase project is active

**"Port already in use":**
- Use `--port $PORT` in start command (Render provides PORT variable)

### Frontend Issues

**"NEXT_PUBLIC_API_BASE_URL is not defined":**
- Add environment variable in Netlify
- Redeploy site after adding

**"Failed to fetch" / CORS errors:**
- Update CORS in `backend/main.py`
- Add your Netlify URL to `allow_origins`
- Redeploy backend

**Build fails:**
- Check `Base directory` is set to `frontend`
- Verify `package.json` exists
- Check build logs for specific errors

**Shows "0 tools":**
- Check backend URL in environment variable
- Test backend API directly: `curl https://your-backend.onrender.com/api/tools`
- Check browser console for errors

---

## 🎯 QUICK ANSWER TO YOUR QUESTION

**Q: Should I change anything in code or just deploy with proper environment variables?**

**A: You need ONE code change:**

1. **Update CORS in `backend/main.py`** (line 30-37)
   - Change from Vercel URLs to Netlify URLs
   - OR use `allow_origins=["*"]` for testing

2. **Everything else is just environment variables:**
   - Backend: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
   - Frontend: NEXT_PUBLIC_API_BASE_URL

**That's it! No other code changes needed.**

---

## 📝 SUMMARY

### Code Changes Required: 1
- Update CORS in `backend/main.py` for Netlify

### Environment Variables Required: 3
- Backend: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
- Frontend: `NEXT_PUBLIC_API_BASE_URL`

### Deployment Order:
1. Deploy Backend first (get URL)
2. Deploy Frontend with backend URL
3. Update CORS with frontend URL
4. Redeploy backend

**Total Time: ~20 minutes**

---

## 🚀 READY TO DEPLOY!

Your code is production-ready. Just:
1. Update CORS for Netlify
2. Set environment variables
3. Deploy!
