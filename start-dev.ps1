#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start ClipShot development environment
.DESCRIPTION
    Starts backend API server, frontend Vite dev server, and Tauri desktop app
#>

Write-Host "🚀 Starting ClipShot Development Environment..." -ForegroundColor Cyan
Write-Host ""

# Check if backend venv exists
if (-not (Test-Path "apps\backend\venv\Scripts\python.exe")) {
    Write-Host "❌ Backend virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run: cd apps\backend; python -m venv venv; .\venv\Scripts\pip.exe install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check if node_modules exists for desktop
if (-not (Test-Path "apps\desktop\node_modules")) {
    Write-Host "❌ Desktop dependencies not installed!" -ForegroundColor Red
    Write-Host "   Run: cd apps\desktop; npm install" -ForegroundColor Yellow
    exit 1
}

# Add Cargo to PATH
$env:PATH += ";$env:USERPROFILE\.cargo\bin"

# Start Backend
Write-Host "📡 Starting Backend API Server (Port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$PSScriptRoot\apps\backend'; " +
    "Write-Host '🔧 Backend Server Starting...' -ForegroundColor Cyan; " +
    "& '$PSScriptRoot\apps\backend\venv\Scripts\python.exe' -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"

# Wait for backend to start
Write-Host "⏳ Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test backend connection
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -TimeoutSec 5
    Write-Host "✅ Backend is running: $($health.service) v$($health.version)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""

# Start Desktop App (includes Vite dev server)
Write-Host "🖥️  Starting Desktop App (Vite + Tauri)..." -ForegroundColor Green
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
    "cd '$PSScriptRoot\apps\desktop'; " +
    "`$env:PATH += ';$env:USERPROFILE\.cargo\bin'; " +
    "Write-Host '🔧 Desktop App Starting...' -ForegroundColor Cyan; " +
    "npm run tauri:dev"

Write-Host ""
Write-Host "✨ ClipShot Development Environment Started!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Service URLs:" -ForegroundColor Cyan
Write-Host "   Backend API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Health:       http://localhost:8000/api/v1/health" -ForegroundColor White
Write-Host "   Frontend:     http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "📝 Logs:" -ForegroundColor Cyan
Write-Host "   Backend:      apps\backend\logs\clipshot.log" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop: Close the opened PowerShell windows" -ForegroundColor Yellow
Write-Host ""
