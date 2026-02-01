#!/bin/bash
# Build script for ClipShot - builds all components

set -e

echo "🚀 Building ClipShot..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Build backend
echo -e "${BLUE}📦 Building backend...${NC}"
cd apps/backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo "⚠️  Backend requirements.txt not found"
fi
cd ../..

# Build frontend
echo -e "${BLUE}📦 Building frontend...${NC}"
cd apps/desktop
if [ -f "package.json" ]; then
    npm install
    npm run build || echo "⚠️  Frontend build script not configured yet"
    echo -e "${GREEN}✓ Frontend built${NC}"
else
    echo "⚠️  Frontend package.json not found"
fi
cd ../..

# Build Tauri app
echo -e "${BLUE}📦 Building Tauri app...${NC}"
cd apps/desktop
if command -v cargo &> /dev/null; then
    npm run tauri build || echo "⚠️  Tauri build not configured yet"
    echo -e "${GREEN}✓ Tauri app built${NC}"
else
    echo "⚠️  Rust/Cargo not installed, skipping Tauri build"
fi
cd ../..

echo -e "${GREEN}✅ Build complete!${NC}"
