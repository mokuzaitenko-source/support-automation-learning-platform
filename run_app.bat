@echo off
setlocal

title Python Learning Platform
color 0A

echo.
echo ========================================
echo  Python Learning Platform
echo ========================================
echo.

REM Resolve script directory so this works on any machine/path
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Starting server...
echo.

if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo [INFO] .venv not found. Using system Python.
)

start "" http://127.0.0.1:5000
python app.py

echo.
echo Server stopped.
pause
endlocal
