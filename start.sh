#!/bin/bash

# 🚀 AI Tool Tracker - Quick Start Script
# This script starts the frontend development server

echo "🚀 Starting AI Tool Tracker..."
echo ""
echo "📊 System Status:"
echo "  ✅ Backend: https://ai-tool-tracker-backend.onrender.com (LIVE)"
echo "  ✅ Database: Supabase PostgreSQL (50 tools)"
echo "  ✅ Frontend: Starting locally..."
echo ""

cd "$(dirname "$0")/frontend"

echo "🔧 Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🌐 Starting development server..."
echo ""
echo "📍 Local:   http://localhost:3000"
echo "📍 Network: http://192.168.0.101:3000"
echo ""
echo "🎯 The frontend will connect to production backend automatically"
echo "💡 Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

npm run dev
