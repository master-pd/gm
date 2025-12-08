#!/bin/bash

# Telegram Bot Runner Script

echo "🤖 Starting Worlds Most Advanced Telegram Bot..."

# Check Python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $python_version"

# Check required files
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and edit it"
    exit 1
fi

if [ ! -f "firebase-key.json" ]; then
    echo "❌ Error: firebase-key.json not found!"
    echo "Please download Firebase service account key"
    exit 1
fi

# Create required directories
mkdir -p data logs backups

# Install requirements if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the bot
echo "🚀 Starting bot..."
python main.py

# Handle restart
if [ $? -eq 0 ]; then
    echo "✅ Bot stopped normally"
else
    echo "🔄 Bot crashed, restarting in 5 seconds..."
    sleep 5
    exec "$0"
fi