@echo off
title Telegram Bot Runner

echo 🤖 Starting Worlds Most Advanced Telegram Bot...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

REM Check required files
if not exist ".env" (
    echo ❌ Error: .env file not found!
    echo Please copy .env.example to .env and edit it
    pause
    exit /b 1
)

if not exist "firebase-key.json" (
    echo ❌ Error: firebase-key.json not found!
    echo Please download Firebase service account key
    pause
    exit /b 1
)

REM Create directories
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

REM Create virtual environment if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Run the bot
echo 🚀 Starting bot...
python main.py

if %errorlevel% equ 0 (
    echo ✅ Bot stopped normally
) else (
    echo 🔄 Bot crashed, restarting in 5 seconds...
    timeout /t 5 /nobreak >nul
    goto :restart
)

pause
exit /b 0

:restart
call %0