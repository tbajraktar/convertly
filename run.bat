@echo off
setlocal
cd /d "%~dp0"
echo ========================================
echo Starting Convertly Local Server...
echo ========================================

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found! 
    echo Please make sure you are running this from the project folder.
    echo Expected path: %CD%\.venv\Scripts\python.exe
    pause
    exit /b
)

echo [INFO] Using virtual environment at .venv
echo [INFO] Starting FastAPI on http://127.0.0.1:8000
echo.

.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Server failed to start.
    echo Possible reasons:
    echo 1. Port 8000 is already in use by another program.
    echo 2. Missing dependencies (run 'pip install -r requirements.txt').
)

pause
