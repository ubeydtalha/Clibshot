#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test ClipShot API Endpoints
#>

param(
    [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "🧪 Testing ClipShot API..." -ForegroundColor Cyan
Write-Host "   Base URL: $BaseUrl" -ForegroundColor White
Write-Host ""

function Test-Endpoint {
    param($Name, $Url, $Method = "GET", $Body = $null)
    
    Write-Host "Testing: $Name" -ForegroundColor Yellow -NoNewline
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Body $Body -ContentType "application/json" -TimeoutSec 5
        } else {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -TimeoutSec 5
        }
        Write-Host " ✅" -ForegroundColor Green
        return $response
    } catch {
        Write-Host " ❌" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Test Health
$health = Test-Endpoint "Health Check" "$BaseUrl/api/v1/health"
if ($health) {
    Write-Host "   Service: $($health.service)" -ForegroundColor Cyan
    Write-Host "   Version: $($health.version)" -ForegroundColor Cyan
    Write-Host "   Status:  $($health.status)" -ForegroundColor Green
}
Write-Host ""

# Test Root
$root = Test-Endpoint "Root Endpoint" "$BaseUrl/"
if ($root) {
    Write-Host "   Message: $($root.message)" -ForegroundColor Cyan
}
Write-Host ""

# Test Plugins
$plugins = Test-Endpoint "List Plugins" "$BaseUrl/api/v1/plugins/"
if ($plugins) {
    Write-Host "   Plugins: $($plugins.Count)" -ForegroundColor Cyan
}
Write-Host ""

# Test Clips
$clips = Test-Endpoint "List Clips" "$BaseUrl/api/v1/clips/"
if ($clips) {
    Write-Host "   Clips: $($clips.Count)" -ForegroundColor Cyan
}
Write-Host ""

# Test Stats
$stats = Test-Endpoint "Clip Stats" "$BaseUrl/api/v1/clips/stats"
if ($stats) {
    Write-Host "   Total Clips: $($stats.total_clips)" -ForegroundColor Cyan
    Write-Host "   Processed: $($stats.processed_clips)" -ForegroundColor Cyan
    Write-Host "   Unprocessed: $($stats.unprocessed_clips)" -ForegroundColor Cyan
}
Write-Host ""

# Test API Docs
Write-Host "Testing: API Documentation" -ForegroundColor Yellow -NoNewline
try {
    $docs = Invoke-WebRequest -Uri "$BaseUrl/docs" -UseBasicParsing -TimeoutSec 5
    if ($docs.StatusCode -eq 200) {
        Write-Host " ✅" -ForegroundColor Green
    }
} catch {
    Write-Host " ❌" -ForegroundColor Red
}
Write-Host ""

Write-Host "✨ API Testing Complete!" -ForegroundColor Green
