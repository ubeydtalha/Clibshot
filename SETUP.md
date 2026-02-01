# 🚀 ClipShot Setup Guide

Complete guide to set up ClipShot development environment.

---

## 📋 Prerequisites

### Required Software

1. **Node.js** 20+
   ```bash
   # Download from https://nodejs.org/
   node --version  # Should be v20.x or higher
   ```

2. **Rust** 1.70+
   ```bash
   # Install rustup
   # Windows: https://rustup.rs/
   # macOS/Linux: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   
   rustc --version  # Should be 1.70 or higher
   ```

3. **Python** 3.11+
   ```bash
   # Download from https://www.python.org/
   python --version  # Should be 3.11 or higher
   ```

4. **Git**
   ```bash
   git --version
   ```

### Platform-Specific Requirements

**Windows:**
- Visual Studio Build Tools 2019 or newer
- WebView2 (usually pre-installed on Windows 10/11)

**macOS:**
- Xcode Command Line Tools: `xcode-select --install`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential \
  curl \
  wget \
  file \
  libssl-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev

# Fedora
sudo dnf install webkit2gtk4.1-devel \
  openssl-devel \
  curl \
  wget \
  file \
  libappindicator-gtk3-devel \
  librsvg2-devel

# Arch
sudo pacman -S webkit2gtk-4.1 \
  base-devel \
  curl \
  wget \
  file \
  openssl \
  appmenu-gtk-module \
  gtk3 \
  libappindicator-gtk3 \
  librsvg
```

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/clipshot.git
cd clipshot
```

### 2. Install Desktop App Dependencies

```bash
cd apps/desktop
npm install
```

This will install:
- React, React DOM
- Tauri CLI and API
- Vite and plugins
- Tailwind CSS
- UI libraries (Radix UI, Lucide icons)
- State management (Zustand)
- Routing (React Router)

### 3. Install Backend Dependencies

```bash
cd ../backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# In apps/backend/
cp .env.example .env

# Edit .env with your settings (optional for dev)
```

---

## 🏃 Running the Application

You'll need **2 terminal windows**.

### Terminal 1: Backend API

```bash
cd apps/backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run FastAPI server
uvicorn src.main:app --reload --port 8000

# Alternative:
python src/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
🚀 ClipShot Backend starting...
```

**Verify:** Open http://localhost:8000/api/docs

### Terminal 2: Desktop App

```bash
cd apps/desktop

# Run Tauri dev server
npm run tauri dev
```

First run will:
1. Download Rust dependencies (takes a few minutes)
2. Compile Rust backend
3. Start Vite dev server
4. Launch desktop app

**Result:** ClipShot window should open automatically!

---

## ✅ Verification

### Check 1: Frontend Running
- ClipShot window opened
- UI shows "ClipShot" title
- No errors in console

### Check 2: Backend Running
- Visit http://localhost:8000/api/docs
- You should see FastAPI Swagger UI
- Health endpoint returns `{"status": "ok"}`

### Check 3: Integration
- In ClipShot app, check "Backend Status"
- Should show "✅ Backend Online"
- Test "Greet" function (enter name, click button)

### Check 4: Hot Reload

**Frontend:**
```bash
# Edit apps/desktop/src/App.tsx
# Change any text
# Save file
# App should update instantly (<100ms)
```

**Backend:**
```bash
# Edit apps/backend/src/main.py
# Add a new endpoint
# Save file
# Server should reload automatically
```

---

## 🐛 Troubleshooting

### Issue: Tauri Build Fails

**Error:** "No such command: tauri"

**Solution:**
```bash
cd apps/desktop
npm install @tauri-apps/cli --save-dev
```

---

### Issue: Backend Import Error

**Error:** "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
# Make sure venv is activated
cd apps/backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### Issue: Port Already in Use

**Error:** "Address already in use: 8000" or "5173"

**Solution:**
```bash
# Find and kill process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

---

### Issue: CORS Error

**Error:** "Access to fetch at 'http://localhost:8000' from origin 'tauri://localhost' has been blocked by CORS policy"

**Solution:**
- Backend CORS is already configured for Tauri
- Make sure backend is running on port 8000
- Restart both frontend and backend

---

### Issue: WebView2 Missing (Windows)

**Error:** "WebView2 not found"

**Solution:**
- Download and install WebView2 Runtime
- https://developer.microsoft.com/microsoft-edge/webview2/

---

## 🎯 Next Steps

Once everything is running:

1. **Explore the UI**
   - System information panel
   - Backend status check
   - Greet command test

2. **Read Documentation**
   - [`docs/00_MASTER_AI_INSTRUCTION.md`](../docs/00_MASTER_AI_INSTRUCTION.md) — Architecture overview
   - [`docs/04_FRONTEND_ARCHITECTURE.md`](../docs/04_FRONTEND_ARCHITECTURE.md) — Frontend details
   - [`docs/03_BACKEND_ARCHITECTURE.md`](../docs/03_BACKEND_ARCHITECTURE.md) — Backend details

3. **Start Development**
   - Phase 2: Implement plugin manager
   - Phase 3: Build UI components
   - Phase 4: Create example plugins

---

## 📊 Development Workflow

### Daily Routine

1. **Start Backend**
   ```bash
   cd apps/backend
   source venv/bin/activate
   uvicorn src.main:app --reload --port 8000
   ```

2. **Start Frontend**
   ```bash
   cd apps/desktop
   npm run tauri dev
   ```

3. **Code & Test**
   - Make changes
   - Hot reload updates automatically
   - Test in running app

4. **Commit**
   ```bash
   git add .
   git commit -m "feat(component): description"
   git push
   ```

---

## 🚀 Build for Production

### Desktop App

```bash
cd apps/desktop
npm run tauri build
```

Outputs:
- Windows: `.exe` installer in `src-tauri/target/release/bundle/`
- macOS: `.dmg` and `.app` in `src-tauri/target/release/bundle/`
- Linux: `.deb`, `.AppImage` in `src-tauri/target/release/bundle/`

### Backend (Docker)

```bash
cd apps/backend
docker build -t clipshot-backend .
docker run -p 8000:8000 clipshot-backend
```

---

## 💡 Tips

1. **Use VSCode**
   - Install: rust-analyzer, Tauri, ESLint, Prettier, Pylance
   - Open workspace: `code clipshot.code-workspace`

2. **Keep Terminals Open**
   - Terminal 1: Backend (always running)
   - Terminal 2: Frontend (tauri dev)
   - Terminal 3: Git commands, testing

3. **Hot Reload**
   - Vite: <100ms reload
   - FastAPI: ~1s reload
   - Tauri Rust: Full rebuild needed (slower)

4. **Debugging**
   - Frontend: Chrome DevTools (F12 in app)
   - Backend: Print statements or debugger
   - Rust: `println!` or rust-analyzer

---

**🎉 You're Ready!**

Start building the future of gaming clip management! 🚀
