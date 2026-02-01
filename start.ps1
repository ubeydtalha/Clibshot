# ClipShot Quick Start Script (Windows PowerShell)

Write-Host "🎮 ClipShot Quick Start" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "apps/desktop") -or !(Test-Path "apps/backend")) {
    Write-Host "❌ Error: Please run this script from the ClipShot root directory" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
Write-Host ""

# Install desktop dependencies
Write-Host "  → Installing desktop app dependencies (npm)..." -ForegroundColor Gray
Push-Location apps/desktop
if (!(Test-Path "node_modules")) {
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ npm install failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
}
Pop-Location

# Install backend dependencies
Write-Host "  → Installing backend dependencies (pip)..." -ForegroundColor Gray
Push-Location apps/backend

if (!(Test-Path "venv")) {
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ pip install failed" -ForegroundColor Red
    deactivate
    Pop-Location
    exit 1
}
deactivate
Pop-Location

Write-Host ""
Write-Host "✅ Dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Starting ClipShot..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Terminal 1: Backend API (FastAPI)" -ForegroundColor Cyan
Write-Host "  Terminal 2: Desktop App (Tauri)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to start the backend API..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Start backend in new terminal
Write-Host ""
Write-Host "  → Starting backend API..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\apps\backend'; .\venv\Scripts\Activate.ps1; Write-Host '🚀 Starting FastAPI backend...' -ForegroundColor Cyan; uvicorn src.main:app --reload --port 8000"

Write-Host "  → Waiting for backend to start..." -ForegroundColor Gray
Start-Sleep -Seconds 3

# Check if backend is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ Backend is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Backend might still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to start the desktop app..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Start desktop app
Write-Host ""
Write-Host "  → Starting desktop app (this may take a while on first run)..." -ForegroundColor Gray
Push-Location apps/desktop
npm run tauri:dev
Pop-Location
