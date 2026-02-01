# ClipShot - Quick Reference

## 🚀 Hızlı Başlatma

### Backend
```powershell
cd E:\Clibshot\apps\backend
.\venv\Scripts\python.exe src\main.py
```

### Desktop
```cmd
E:\Clibshot\apps\desktop\launch.bat
```

## 🔗 Erişim Noktaları

| Servis | URL | Açıklama |
|--------|-----|----------|
| Desktop App | Auto-open | Tauri window |
| Frontend Dev | http://localhost:5173 | Vite dev server |
| Backend API | http://localhost:8000 | FastAPI |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/api/v1/health | Status endpoint |

## 📁 Önemli Dosyalar

### Konfigürasyon
- `apps/desktop/package.json` - npm dependencies
- `apps/desktop/vite.config.ts` - Vite config
- `apps/desktop/src-tauri/Cargo.toml` - Rust dependencies
- `apps/desktop/src-tauri/tauri.conf.json` - Tauri config
- `apps/backend/requirements.txt` - Python packages

### Kod
- `apps/desktop/src/App.tsx` - React main component
- `apps/desktop/src-tauri/src/main.rs` - Tauri main process
- `apps/desktop/src-tauri/src/commands.rs` - Tauri commands
- `apps/backend/src/main.py` - FastAPI app

### Scripts
- `apps/desktop/launch.bat` - Desktop launcher
- `start.ps1` - Full stack starter (PowerShell)
- `start.sh` - Full stack starter (Bash)

## 🛠️ Geliştirme Komutları

### Desktop App
```bash
cd apps/desktop

# Development mode
npm run tauri:dev

# Build production
npm run tauri:build

# Generate icons
npm run tauri icon path/to/icon.png

# Lint
npm run lint

# Type check
npm run type-check
```

### Backend
```bash
cd apps/backend

# Activate venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Unix

# Run server
python src/main.py

# Install packages
pip install -r requirements.txt

# Freeze packages
pip freeze > requirements.txt
```

### Rust
```bash
cd apps/desktop/src-tauri

# Build
cargo build

# Build release
cargo build --release

# Run
cargo run

# Check
cargo check

# Update dependencies
cargo update
```

## 🐛 Sorun Giderme

### Desktop app başlamıyor
```powershell
# 1. Environment kontrol
cargo --version
link.exe 2>&1 | Select-Object -First 1

# 2. Temiz build
cd apps/desktop
Remove-Item src-tauri\target -Recurse -Force
npm run tauri:dev
```

### Backend hatası
```powershell
# 1. venv kontrol
cd apps/backend
.\venv\Scripts\python.exe --version

# 2. Dependencies yeniden yükle
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Port zaten kullanımda
```powershell
# Backend (8000)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Frontend (5173)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process
```

## 📦 Yüklü Paketler

### npm (188 packages)
- react: 18.2.0
- @tauri-apps/api: 2.9.6
- vite: 5.4.21
- typescript: 5.7.3
- tailwindcss: 3.4.17
- (183 more...)

### Python (28 packages)
- fastapi: 0.128.0
- uvicorn: 0.40.0
- pydantic: 2.12.5
- aiohttp: 3.13.3
- (24 more...)

### Rust (434 crates)
- tauri: 2.9.5
- tokio: 1.49.0
- serde: 1.0.228
- reqwest: 0.11.27
- (430 more...)

## 🔑 Tauri Commands

```typescript
// Greet command
import { invoke } from '@tauri-apps/api/core';
const greeting = await invoke('greet', { name: 'User' });

// System info
const sysInfo = await invoke('get_system_info');
// Returns: { os, arch, version }

// Backend API call
const data = await invoke('call_backend_api', { 
  endpoint: '/api/v1/health' 
});
```

## 📚 Documentation

- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Detailed setup
- [SUCCESS_REPORT.md](SUCCESS_REPORT.md) - Current status
- [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Development plan
- [.ai/AGENT_PROMPTS.md](.ai/AGENT_PROMPTS.md) - Multi-agent strategy

## 🎯 Sonraki Adımlar

1. **Phase 2: Backend Infrastructure**
   - Plugin Manager
   - Database integration
   - Complete API routes

2. **Phase 3: Frontend Core**
   - Component library
   - Multiple pages
   - State management

3. **Phase 4: Plugin System**
   - SDK development
   - Example plugins
   - Hot reload

## 💡 Tips

- İlk build uzun sürer (~15-20 dk), sonrakiler hızlıdır (~5-15 sn)
- HMR sayesinde frontend değişiklikleri anında görünür
- Rust dosyaları değişince otomatik yeniden derleme olur
- Backend auto-reload aktif, kod değişiklikleri otomatik yüklenir

## 🆘 Yardım

Sorun yaşıyorsanız:
1. [SETUP.md](SETUP.md) - Kurulum kılavuzu
2. [QUICK_FIX.md](QUICK_FIX.md) - Hızlı çözümler
3. Terminal output'ları kontrol edin
4. `npm run tauri:dev` ve `python src/main.py` loglarını inceleyin

---

**Version**: 0.1.0  
**Status**: ✅ Running  
**Last Updated**: 1 Şubat 2026
