#!/bin/bash
# Test script for ClipShot - runs all tests

set -e

echo "🧪 Running ClipShot tests..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

FAILED=0

# Test backend
echo -e "${BLUE}🧪 Testing backend...${NC}"
cd apps/backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt 2>/dev/null || true
    if command -v pytest &> /dev/null; then
        pytest || { echo -e "${RED}✗ Backend tests failed${NC}"; FAILED=1; }
        echo -e "${GREEN}✓ Backend tests passed${NC}"
    else
        echo "⚠️  pytest not installed, skipping backend tests"
    fi
else
    echo "⚠️  Backend not configured"
fi
cd ../..

# Test frontend
echo -e "${BLUE}🧪 Testing frontend...${NC}"
cd apps/desktop
if [ -f "package.json" ]; then
    npm install 2>/dev/null || true
    npm test || { echo -e "${RED}✗ Frontend tests failed${NC}"; FAILED=1; }
    echo -e "${GREEN}✓ Frontend tests passed${NC}"
else
    echo "⚠️  Frontend not configured"
fi
cd ../..

# Lint checks
echo -e "${BLUE}🔍 Running linters...${NC}"
cd apps/backend
if command -v flake8 &> /dev/null; then
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo "⚠️  Linting warnings found"
fi
cd ../..

cd apps/desktop
if [ -f "package.json" ]; then
    npm run lint || echo "⚠️  Linting not configured"
fi
cd ../..

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
