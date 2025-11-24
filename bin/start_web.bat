@echo off
REM Hash Cracker - Web Interface Launcher for Windows

cd /d "%~dp0\.."

echo ==========================================
echo   Hash Cracker - Web Interface
echo ==========================================
echo.
echo Starting web server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7+ first.
    pause
    exit /b 1
)

REM Kill any existing process on port 8080 (optional, may require admin)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1

REM Start the web server
python web_server.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Server stopped with error
    pause
)
