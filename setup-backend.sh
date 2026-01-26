#!/bin/bash

# 🚀 Backend Setup Script
# Automatically sets up Python virtual environment and installs dependencies

echo "🔧 Setting up backend environment..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend" || exit 1

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ All dependencies installed!"
echo ""

# Verify critical imports
echo "🔍 Verifying imports..."
python -c "
try:
    from dotenv import load_dotenv
    from supabase import create_client
    from fastapi import FastAPI
    print('✅ All critical imports working!')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Backend setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo ""
echo "To run the backend server:"
echo "  python main.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
