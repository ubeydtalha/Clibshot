@echo off
:: ClipShot Desktop App Launcher
:: Sets up Visual Studio and Rust environment then launches the app

echo ========================================
echo ClipShot Desktop App Launcher
echo ========================================
echo.

:: Load Visual Studio Build Tools environment
echo [1/3] Loading Visual Studio Build Tools...
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat" >nul 2>&1

:: Add Rust to PATH
echo [2/3] Adding Rust to PATH...
set PATH=%PATH%;C:\Users\utabj\.cargo\bin

:: Verify tools
echo [3/3] Verifying tools...
cargo --version
echo.

:: Navigate to desktop app directory
cd /d E:\Clibshot\apps\desktop

:: Launch the app
echo.
echo Starting Tauri Desktop App...
echo ========================================
npm run tauri:dev
