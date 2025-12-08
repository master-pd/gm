#!/usr/bin/env python3
"""
Run Script for Telegram Bot
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def run_bot():
    """Run the bot with monitoring"""
    
    print("""
    🚀 TELEGRAM BOT RUNNER
    ======================
    """)
    
    # Check if required files exist
    required_files = [".env", "firebase-key.json"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please run setup.py first!")
        sys.exit(1)
    
    # Check Python requirements
    try:
        import telegram
        import firebase_admin
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start the bot
    print("\n🤖 Starting bot...")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    try:
        from main import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)
        run_bot()  # Restart

if __name__ == "__main__":
    run_bot()