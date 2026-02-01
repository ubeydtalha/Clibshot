# 🚀 ClipShot Deployment Guide

**Version:** 0.1.0  
**Last Updated:** February 1, 2026

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Build](#production-build)
4. [Deployment Options](#deployment-options)
5. [Environment Configuration](#environment-configuration)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| **Node.js** | 20.x+ | Frontend build & Tauri |
| **Python** | 3.11+ | Backend API |
| **Rust** | 1.70+ | Tauri desktop app |
| **Git** | Latest | Version control |

### Platform-Specific

**Windows:**
- Visual Studio 2022 Build Tools
- WebView2 (usually pre-installed)

**macOS:**
- Xcode Command Line Tools
- WebKit framework

**Linux:**
- webkit2gtk-4.0
- libappindicator3
- librsvg2

---

## 💻 Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/clipshot.git
cd clipshot
```

### 2. Backend Setup
```bash
cd apps/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "from src.main import app; print('✅ Backend ready')"
```

### 3. Desktop App Setup
```bash
cd apps/desktop

# Install dependencies
npm install

# Verify installation
npm run tauri --version
```

### 4. Start Development Servers

**Option A: Use Start Script (Windows)**
```powershell
cd ../../
.\start-dev.ps1
```

**Option B: Manual Start**

Terminal 1 (Backend):
```bash
cd apps/backend
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 (Desktop):
```bash
cd apps/desktop
npm run tauri:dev
```

### 5. Verify Setup
```powershell
# Test API
.\test-api.ps1

# Or manual test
curl http://localhost:8000/api/v1/health
```

---

## 🏗️ Production Build

### Backend Production

#### 1. Prepare Environment
```bash
cd apps/backend

# Create production venv
python -m venv venv-prod
source venv-prod/bin/activate  # Windows: venv-prod\Scripts\activate

# Install production dependencies
pip install -r requirements.txt
```

#### 2. Configuration
Create `.env` file:
```env
# Production settings
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
DATABASE_URL=sqlite:///./data/clipshot.db

# Optional: PostgreSQL
# DATABASE_URL=postgresql://user:pass@localhost/clipshot
```

#### 3. Run Production Server
```bash
# With Gunicorn (Linux/macOS)
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log

# With Uvicorn (Windows)
uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --no-access-log
```

### Desktop Production Build

#### 1. Configure Build
Edit `apps/desktop/src-tauri/tauri.conf.json`:
```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  },
  "bundle": {
    "identifier": "com.clipshot.app",
    "active": true,
    "targets": ["nsis", "msi"],  // Windows
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": ""
    }
  }
}
```

#### 2. Build Desktop App
```bash
cd apps/desktop

# Install dependencies
npm install

# Build for production
npm run tauri:build
```

#### 3. Find Build Artifacts

**Windows:**
```
apps/desktop/src-tauri/target/release/bundle/
├── nsis/ClipShot_0.1.0_x64-setup.exe
└── msi/ClipShot_0.1.0_x64_en-US.msi
```

**macOS:**
```
apps/desktop/src-tauri/target/release/bundle/
├── dmg/ClipShot_0.1.0_x64.dmg
└── macos/ClipShot.app
```

**Linux:**
```
apps/desktop/src-tauri/target/release/bundle/
├── deb/clipshot_0.1.0_amd64.deb
└── appimage/ClipShot_0.1.0_amd64.AppImage
```

---

## 🌐 Deployment Options

### Option 1: Standalone (Desktop Only)

Best for single-user, local usage.

1. Build desktop app (includes backend)
2. Distribute installer
3. Backend runs locally when app starts

### Option 2: Client-Server

Best for team usage, cloud features.

**Server Setup:**
```bash
# Deploy backend to server
# Use systemd, Docker, or cloud platform

# Example systemd service
[Unit]
Description=ClipShot Backend
After=network.target

[Service]
Type=notify
User=clipshot
WorkingDirectory=/opt/clipshot/backend
ExecStart=/opt/clipshot/backend/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Client Setup:**
Configure `apps/desktop/.env`:
```env
VITE_API_URL=https://api.clipshot.com
```

### Option 3: Docker

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./apps/backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/clipshot
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: clipshot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

---

## ⚙️ Environment Configuration

### Backend (.env)
```env
# Application
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database
DATABASE_URL=sqlite:///./data/clipshot.db

# CORS
CORS_ORIGINS=https://yourdomain.com,tauri://localhost

# Plugins
PLUGIN_DIR=/opt/clipshot/plugins

# Storage
UPLOAD_DIR=/opt/clipshot/uploads
MAX_UPLOAD_SIZE=500000000  # 500MB
```

### Frontend (.env)
```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Features
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_TELEMETRY=false
```

---

## 🔒 Security Checklist

### Pre-Deployment
- [ ] Change default secrets
- [ ] Configure CORS properly
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Review file permissions
- [ ] Disable debug mode
- [ ] Sanitize error messages
- [ ] Set secure headers

### Post-Deployment
- [ ] Monitor logs
- [ ] Set up alerts
- [ ] Regular backups
- [ ] Security updates
- [ ] Penetration testing

---

## 📊 Performance Optimization

### Backend
```python
# In src/main.py

# Enable compression
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Connection pooling (PostgreSQL)
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Caching
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()
```

### Frontend
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
})
```

---

## 🔍 Monitoring

### Logs
```bash
# Backend logs
tail -f apps/backend/logs/clipshot.log

# Systemd logs (if using systemd)
journalctl -u clipshot -f

# Docker logs
docker-compose logs -f backend
```

### Health Checks
```bash
# API health
curl http://localhost:8000/api/v1/health

# With monitoring
while true; do
  curl -s http://localhost:8000/api/v1/health | jq .
  sleep 60
done
```

### Metrics (Optional)
```python
# Add to src/main.py
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
# Metrics available at /metrics
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Issue:** Module not found
```bash
# Solution: Activate venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

**Issue:** Port already in use
```bash
# Solution: Change port or kill process
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # macOS/Linux
```

### Desktop App Build Fails

**Issue:** Rust not found
```bash
# Solution: Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**Issue:** WebView2 missing (Windows)
```
Download from: https://developer.microsoft.com/en-us/microsoft-edge/webview2/
```

### Database Issues

**Issue:** Database locked
```bash
# Solution: Close connections
rm clipshot.db  # Delete and recreate
# Or use PostgreSQL for production
```

### Performance Issues

**Issue:** Slow responses
```bash
# Check database indexes
# Enable query logging
# Use connection pooling
# Add caching layer
```

---

## 📦 Update & Rollback

### Update Deployment
```bash
# Pull latest code
git pull origin main

# Backend
cd apps/backend
source venv/bin/activate
pip install -r requirements.txt
# Restart service

# Desktop
cd apps/desktop
npm install
npm run tauri:build
# Distribute new installer
```

### Rollback
```bash
# Git rollback
git checkout <previous-commit>

# Docker rollback
docker-compose down
docker-compose up -d --build
```

---

## 🎯 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (128/128)
- [ ] No TypeScript errors
- [ ] Build succeeds locally
- [ ] Environment configured
- [ ] Secrets secured
- [ ] Database backed up

### Deployment
- [ ] Deploy backend
- [ ] Verify API health
- [ ] Deploy frontend/desktop
- [ ] Test end-to-end
- [ ] Monitor logs
- [ ] Check performance

### Post-Deployment
- [ ] Smoke tests pass
- [ ] Monitor error rates
- [ ] Check resource usage
- [ ] Verify backups
- [ ] Update documentation
- [ ] Notify users

---

## 📞 Support

**Issues:** https://github.com/yourusername/clipshot/issues  
**Docs:** https://docs.clipshot.com  
**Email:** support@clipshot.com

---

**✅ Deployment Status:** Production Ready  
**📚 Documentation:** Complete  
**🔒 Security:** Configured  
**📊 Monitoring:** Available
