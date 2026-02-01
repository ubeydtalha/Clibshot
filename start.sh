#!/bin/bash

# ClipShot Quick Start Script (macOS/Linux)

echo "🎮 ClipShot Quick Start"
echo "======================"
echo ""

# Check if we're in the right directory
if [ ! -d "apps/desktop" ] || [ ! -d "apps/backend" ]; then
    echo "❌ Error: Please run this script from the ClipShot root directory"
    exit 1
fi

echo "📦 Installing dependencies..."
echo ""

# Install desktop dependencies
echo "  → Installing desktop app dependencies (npm)..."
cd apps/desktop
if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ npm install failed"
        exit 1
    fi
fi
cd ../..

# Install backend dependencies
echo "  → Installing backend dependencies (pip)..."
cd apps/backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "❌ pip install failed"
    deactivate
    exit 1
fi
deactivate
cd ../..

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🚀 Starting ClipShot..."
echo ""

# Start backend in background
echo "  → Starting backend API..."
cd apps/backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ../..

# Wait for backend
echo "  → Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo "  ✅ Backend is running!"
else
    echo "  ⚠️  Backend might still be starting..."
fi

echo ""
echo "  → Starting desktop app (this may take a while on first run)..."
cd apps/desktop
npm run tauri:dev

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
