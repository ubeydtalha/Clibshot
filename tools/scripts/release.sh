#!/bin/bash
# Release script for ClipShot - creates release artifacts

set -e

echo "📦 Creating ClipShot release..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get version from argument or use default
VERSION=${1:-"0.1.0"}

echo -e "${BLUE}Version: ${VERSION}${NC}"

# Create release directory
RELEASE_DIR="release/v${VERSION}"
mkdir -p "${RELEASE_DIR}"

# Build all components
echo -e "${BLUE}🏗️  Building components...${NC}"
./tools/scripts/build.sh

# Package backend
echo -e "${BLUE}📦 Packaging backend...${NC}"
cd apps/backend
tar -czf "../../${RELEASE_DIR}/clipshot-backend-${VERSION}.tar.gz" \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.venv' \
    --exclude='venv' \
    .
cd ../..
echo -e "${GREEN}✓ Backend packaged${NC}"

# Copy Tauri installers
echo -e "${BLUE}📦 Collecting installers...${NC}"
if [ -d "apps/desktop/src-tauri/target/release/bundle" ]; then
    # Windows
    if [ -f "apps/desktop/src-tauri/target/release/bundle/msi/"*.msi ]; then
        cp apps/desktop/src-tauri/target/release/bundle/msi/*.msi "${RELEASE_DIR}/"
        echo -e "${GREEN}✓ Windows installer copied${NC}"
    fi
    
    # macOS
    if [ -f "apps/desktop/src-tauri/target/release/bundle/dmg/"*.dmg ]; then
        cp apps/desktop/src-tauri/target/release/bundle/dmg/*.dmg "${RELEASE_DIR}/"
        echo -e "${GREEN}✓ macOS installer copied${NC}"
    fi
    
    # Linux
    if [ -f "apps/desktop/src-tauri/target/release/bundle/appimage/"*.AppImage ]; then
        cp apps/desktop/src-tauri/target/release/bundle/appimage/*.AppImage "${RELEASE_DIR}/"
        echo -e "${GREEN}✓ Linux AppImage copied${NC}"
    fi
    
    if [ -f "apps/desktop/src-tauri/target/release/bundle/deb/"*.deb ]; then
        cp apps/desktop/src-tauri/target/release/bundle/deb/*.deb "${RELEASE_DIR}/"
        echo -e "${GREEN}✓ Linux .deb copied${NC}"
    fi
else
    echo "⚠️  No Tauri bundles found"
fi

# Create checksums
echo -e "${BLUE}🔐 Creating checksums...${NC}"
cd "${RELEASE_DIR}"
sha256sum * > checksums.txt
cd ../..
echo -e "${GREEN}✓ Checksums created${NC}"

# Create release notes
echo -e "${BLUE}📝 Creating release notes...${NC}"
cat > "${RELEASE_DIR}/RELEASE_NOTES.md" << EOF
# ClipShot v${VERSION}

Released: $(date +%Y-%m-%d)

## Downloads

- Windows: \`ClipShot-${VERSION}-setup.msi\`
- macOS: \`ClipShot-${VERSION}.dmg\`
- Linux: \`clipshot-${VERSION}.AppImage\`

## Installation

### Windows
1. Download \`ClipShot-${VERSION}-setup.msi\`
2. Run the installer
3. Follow the installation wizard

### macOS
1. Download \`ClipShot-${VERSION}.dmg\`
2. Open the DMG file
3. Drag ClipShot to Applications

### Linux
1. Download \`clipshot-${VERSION}.AppImage\`
2. Make it executable: \`chmod +x clipshot-${VERSION}.AppImage\`
3. Run: \`./clipshot-${VERSION}.AppImage\`

## Verification

Verify checksums:
\`\`\`bash
sha256sum -c checksums.txt
\`\`\`

## What's New

See CHANGELOG.md for details.
EOF

echo -e "${GREEN}✅ Release ${VERSION} created in ${RELEASE_DIR}${NC}"
echo ""
echo "Release contents:"
ls -lh "${RELEASE_DIR}"
