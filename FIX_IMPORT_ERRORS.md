# 🔧 FIX IMPORT ERRORS - Quick Guide

## ❌ ERRORS YOU'RE SEEING

```
Import "dotenv" could not be resolved
Import "supabase" could not be resolved
```

## ✅ ROOT CAUSE

**Python packages not installed in your local environment.**

The packages ARE in `requirements.txt`, but not installed on your machine.

---

## 🚀 SOLUTION

### Option 1: Install Dependencies (Recommended)

**Step 1: Navigate to backend folder**
```bash
cd /home/s-ravant-vignesh/Documents/ai-tool-tracker/backend
```

**Step 2: Create virtual environment (if not exists)**
```bash
python3 -m venv venv
```

**Step 3: Activate virtual environment**
```bash
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

**Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Verify installation**
```bash
python -c "import dotenv; import supabase; print('✅ All imports working!')"
```

---

### Option 2: Install Specific Packages Only

**If you just want to fix the import errors:**
```bash
pip install python-dotenv supabase
```

---

### Option 3: Use System Python (Not Recommended)

**Install globally:**
```bash
pip3 install python-dotenv supabase
```

**Note:** This installs packages system-wide, not recommended for development.

---

## 🔍 VERIFY INSTALLATION

**Check if packages are installed:**
```bash
pip list | grep -E "dotenv|supabase"
```

**Expected output:**
```
python-dotenv    1.0.0
supabase         2.0.3
```

---

## 📋 COMPLETE REQUIREMENTS

**File:** `backend/requirements.txt`

```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
python-multipart==0.0.6

# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

# Database
supabase==2.0.3  ← This one

# Environment
python-dotenv==1.0.0  ← This one

# Scheduling
apscheduler==3.10.4

# Utilities
python-dateutil==2.8.2
pytz==2023.3
```

**Status:** ✅ All dependencies are listed correctly

---

## 🎯 WHY THIS HAPPENS

### Local Development:
- Your IDE (VS Code/PyCharm) checks if packages are installed
- Packages in `requirements.txt` but not installed locally
- Shows import errors

### Production (Render):
- Render runs `pip install -r requirements.txt` automatically
- All packages get installed
- No import errors

**Conclusion:** Import errors are LOCAL ONLY, won't affect deployment.

---

## ✅ QUICK FIX (1 Command)

**Run this in backend folder:**
```bash
cd /home/s-ravant-vignesh/Documents/ai-tool-tracker/backend && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt
```

**This will:**
1. Create virtual environment
2. Activate it
3. Install all dependencies

---

## 🔧 IDE CONFIGURATION

### VS Code:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Select Interpreter"
3. Choose the venv interpreter: `./backend/venv/bin/python`

### PyCharm:
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing environment"
4. Choose: `./backend/venv/bin/python`

---

## ⚠️ IMPORTANT NOTES

### For Local Development:
- ✅ Install dependencies in virtual environment
- ✅ Activate venv before running code
- ✅ Configure IDE to use venv interpreter

### For Deployment (Render):
- ✅ No action needed
- ✅ Render installs from requirements.txt automatically
- ✅ Import errors won't occur in production

---

## 🎯 SUMMARY

| Issue | Cause | Solution |
|-------|-------|----------|
| Import errors | Packages not installed locally | Install with pip |
| VS Code warnings | Wrong Python interpreter | Select venv interpreter |
| Production | N/A | Works automatically |

---

## ✅ VERIFICATION

**After installing, run:**
```bash
cd backend
source venv/bin/activate
python -c "
from dotenv import load_dotenv
from supabase import create_client
print('✅ All imports working!')
"
```

**Expected output:**
```
✅ All imports working!
```

---

## 🚀 READY TO GO

**Your code is correct. Just install dependencies locally:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Import errors will disappear!** ✅
