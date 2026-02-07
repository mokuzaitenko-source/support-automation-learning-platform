@echo off
title Python Learning Platform
color 0A
echo.
echo ========================================
echo  Python Learning Platform
echo ========================================
echo.
echo Starting server...
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
start http://127.0.0.1:5000
python PyLearn_app.py

pause
