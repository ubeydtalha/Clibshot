#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start ClipShot Backend API Server
#>

Write-Host "📡 Starting ClipShot Backend..." -ForegroundColor Cyan

# Check virtual environment
if (-not (Test-Path "apps\backend\venv\Scripts\python.exe")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Creating virtual environment..." -ForegroundColor Yellow
    
    Set-Location apps\backend
    python -m venv venv
    .\venv\Scripts\pip.exe install -r requirements.txt
    Set-Location ..\..
    
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Start server
Set-Location apps\backend
Write-Host "🚀 Starting Uvicorn server on http://0.0.0.0:8000" -ForegroundColor Green
& "..\..\apps\backend\venv\Scripts\python.exe" -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
