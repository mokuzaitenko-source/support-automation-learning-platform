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

cd /d "C:\Users\alvin\TEst\introtodeeplearning\aca"
call .venv\Scripts\activate.bat
start http://127.0.0.1:5000
python app.py

pause
