#!/usr/bin/env python3
"""
Setup Script for Telegram Bot
"""

import os
import sys
import subprocess
import requests

def setup_bot():
    """Setup the bot environment"""
    
    print("""
    🤖 TELEGRAM BOT SETUP WIZARD
    ============================
    
    This script will help you setup the bot.
    """)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Create directories
    directories = ['data', 'logs', 'backups', 'modules', 'utils']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install requirements
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to install requirements automatically")
        print("Please install manually: pip install -r requirements.txt")
    
    # Create .env file if not exists
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file...")
        bot_token = input("Enter your bot token from @BotFather: ").strip()
        admin_ids = input("Enter admin IDs (comma separated): ").strip()
        
        with open(".env", "w") as f:
            f.write(f"BOT_TOKEN={bot_token}\n")
            f.write(f"ADMIN_IDS={admin_ids}\n")
        
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")
    
    # Check Firebase key
    if not os.path.exists("firebase-key.json"):
        print("\n🔑 Firebase key not found!")
        print("Please download firebase-key.json from Firebase Console")
        print("and place it in the project root directory")
    else:
        print("✅ Firebase key found")
    
    # Create run script
    with open("run.sh", "w") as f:
        f.write("""#!/bin/bash
# Run the bot
source venv/bin/activate  # If using virtual environment
python main.py
""")
    os.chmod("run.sh", 0o755)
    
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETE!")
    print("="*50)
    print("\nNext steps:")
    print("1. Make sure firebase-key.json is in the project root")
    print("2. Edit .env file if needed")
    print("3. Run the bot: python main.py")
    print("4. Or use: ./run.sh")
    print("\nFor help, check README.md")
    print("\n🌟 Happy botting! 🤖")

if __name__ == "__main__":
    setup_bot()