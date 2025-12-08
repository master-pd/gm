#!/usr/bin/env python3
"""
GROUP MASTER Bot Setup Script
Complete Automated Setup for Telegram Bot
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path
from datetime import datetime

class SetupGroupMasterBot:
    """Complete setup for GROUP MASTER Telegram Bot"""
    
    def __init__(self):
        self.project_name = "GROUP MASTER Bot"
        self.version = "2.0.0"
        self.creator = "GM Team"
        
        # Platform detection
        self.system = platform.system()
        self.is_windows = self.system == "Windows"
        self.is_linux = self.system == "Linux"
        self.is_mac = self.system == "Darwin"
        
        # Paths
        self.root_dir = Path.cwd()
        self.data_dir = self.root_dir / "data"
        self.logs_dir = self.root_dir / "logs"
        self.backups_dir = self.root_dir / "backups"
        self.modules_dir = self.root_dir / "modules"
        self.utils_dir = self.root_dir / "utils"
        
        # Colors for output
        self.COLORS = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
        }
    
    def print_header(self):
        """Print setup header"""
        header = f"""
{self.COLORS['HEADER']}{self.COLORS['BOLD']}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🤖 GROUP MASTER BOT SETUP 🤖               ║
║                                                          ║
║              Version: {self.version}                          ║
║              Creator: {self.creator}                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{self.COLORS['ENDC']}
"""
        print(header)
    
    def print_step(self, step_num, message):
        """Print step message"""
        print(f"\n{self.COLORS['OKBLUE']}[{step_num}] {message}{self.COLORS['ENDC']}")
    
    def print_success(self, message):
        """Print success message"""
        print(f"{self.COLORS['OKGREEN']}✅ {message}{self.COLORS['ENDC']}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"{self.COLORS['WARNING']}⚠️  {message}{self.COLORS['ENDC']}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"{self.COLORS['FAIL']}❌ {message}{self.COLORS['ENDC']}")
    
    def check_python_version(self):
        """Check Python version"""
        self.print_step("1", "Checking Python version...")
        
        python_version = sys.version_info
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            self.print_error(f"Python 3.8 or higher required (current: {python_version.major}.{python_version.minor}.{python_version.micro})")
            sys.exit(1)
        
        self.print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
        return True
    
    def create_directory_structure(self):
        """Create project directory structure"""
        self.print_step("2", "Creating directory structure...")
        
        directories = [
            self.data_dir,
            self.logs_dir,
            self.backups_dir,
            self.modules_dir,
            self.utils_dir,
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            self.print_success(f"Created: {directory.name}/")
            
            # Create __init__.py for Python packages
            init_file = directory / "__init__.py"
            if not init_file.exists():
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write('"""Package initialization file"""\n')
        
        # Create subdirectories inside data
        data_subdirs = ['ai', 'games', 'users', 'cache']
        for subdir in data_subdirs:
            (self.data_dir / subdir).mkdir(exist_ok=True)
        
        self.print_success("Directory structure created successfully")
        return True
    
    def check_git(self):
        """Check if Git is installed"""
        self.print_step("3", "Checking Git installation...")
        
        try:
            subprocess.run(['git', '--version'], 
                          capture_output=True, 
                          check=True,
                          text=True)
            self.print_success("Git is installed")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_warning("Git is not installed or not in PATH")
            
            if self.is_windows:
                self.print_warning("Download Git from: https://git-scm.com/download/win")
            elif self.is_mac:
                self.print_warning("Install Git using: brew install git")
            else:
                self.print_warning("Install Git using: sudo apt-get install git")
            
            return False
    
    def create_gitignore(self):
        """Create .gitignore file"""
        self.print_step("4", "Creating .gitignore file...")
        
        gitignore_content = """# SECRETS - NEVER COMMIT
firebase-key.json
.env
.env.local
.env.*
secrets/
keys/
*.key
*.pem

# LOCAL DATA
data/
!data/__init__.py
data/*
logs/
!logs/__init__.py
logs/*
backups/
!backups/__init__.py
backups/*

# AI KNOWLEDGE
*.pkl
*.pickle
*.model

# DATABASE
*.db
*.sqlite
*.sqlite3

# PYTHON
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
pyvenv.cfg
venv/
env/
ENV/
.python-version

# VIRTUAL ENVIRONMENT
venv/
venv*/
env/
env*/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.project
.classpath
.settings/

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# TEMP FILES
temp/
tmp/
*.tmp
*.temp

# LOGS
*.log
*.logs

# BACKUPS
*.bak
*.backup

# TEST
test/
tests/
*.test
*.spec

# DOCUMENTATION
docs/_build/
_build/

# DISTRIBUTION
dist/
build/
*.egg-info/
*.egg
*.whl

# CONFIGURATION
config.local.py
settings.local.py
"""
        
        gitignore_path = self.root_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        self.print_success(".gitignore file created")
        return True
    
    def create_env_template(self):
        """Create .env.example template"""
        self.print_step("5", "Creating environment configuration...")
        
        env_template = """# ============================================
# GROUP MASTER BOT CONFIGURATION
# ============================================

# REQUIRED: Your bot token from @BotFather
BOT_TOKEN=your_bot_token_here

# REQUIRED: Admin user IDs (comma separated)
ADMIN_IDS=123456789,987654321

# OPTIONAL: Firebase key path (default: firebase-key.json)
FIREBASE_KEY_PATH=firebase-key.json

# ============================================
# FEATURE CONFIGURATION
# ============================================

# AI System
AI_LEARNING_RATE=0.8
AI_MEMORY_SIZE=1000

# Economy System
STARTING_BALANCE=1000
DAILY_BONUS=100
MAX_TRANSFER_AMOUNT=10000

# Moderation System
MAX_WARNINGS=3
FLOOD_LIMIT=5
MUTE_DURATION=3600

# Game System
MAX_GAMES_PER_GROUP=10
GAME_TIMEOUT=300

# System Configuration
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_MAX_SIZE=10MB

# Backup Configuration
AUTO_BACKUP=true
BACKUP_INTERVAL=24h
MAX_BACKUPS=7

# Performance
MAX_MEMORY_USAGE=512
CLEANUP_INTERVAL=3600

# ============================================
# ADVANCED SETTINGS
# ============================================

# Database
DB_CACHE_TTL=300
DB_MAX_CONNECTIONS=10

# AI Model
AI_MODEL_PATH=data/ai_knowledge.pkl
AI_TRAINING_INTERVAL=3600

# Webhook (if using)
WEBHOOK_URL=
WEBHOOK_PORT=8443
WEBHOOK_LISTEN=0.0.0.0

# Proxy (if needed)
PROXY_URL=
PROXY_USERNAME=
PROXY_PASSWORD=
"""
        
        env_example_path = self.root_dir / ".env.example"
        with open(env_example_path, 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        # Create empty .env if not exists
        env_path = self.root_dir / ".env"
        if not env_path.exists():
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("# Copy from .env.example and edit with your values\n")
            self.print_success(".env.example created")
            self.print_warning("Please edit .env file with your configuration")
        else:
            self.print_success(".env file already exists")
        
        return True
    
    def create_requirements(self):
        """Create requirements.txt file"""
        self.print_step("6", "Creating requirements.txt...")
        
        requirements = """# Core Dependencies
python-telegram-bot==20.7
firebase-admin==6.2.0
python-dotenv==1.0.0
pytz==2023.3

# AI & Data Processing
pickle5==0.0.11
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0

# Utilities
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
python-dateutil==2.8.2
emoji==2.8.0
Pillow==10.0.0

# Security
pycryptodome==3.19.0
cryptography==41.0.7

# Performance
ujson==5.8.0
orjson==3.9.10

# Development
black==23.9.1
flake8==6.1.0
pytest==7.4.3
"""
        
        requirements_path = self.root_dir / "requirements.txt"
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(requirements)
        
        self.print_success("requirements.txt created")
        return True
    
    def create_basic_files(self):
        """Create basic project files"""
        self.print_step("7", "Creating basic project files...")
        
        # Create README.md
        readme_content = f"""# 🤖 GROUP MASTER Telegram Bot

A powerful, self-learning Telegram bot with AI capabilities, games, mini-apps, and complete group management.

## ✨ Features

### 🤖 AI System
- Self-learning from conversations
- Bengali & English support
- Pattern recognition and memory

### 🎮 Games
- Tic Tac Toe
- Quiz
- Hangman
- Math Challenge
- Chess
- Ludo
- and more...

### 📱 Mini Apps
- Calculator
- Unit Converter
- Dictionary
- Password Generator
- BMI Calculator
- Weather Info
- and more...

### 🛡️ Moderation
- Auto moderation
- Warning system
- Flood control
- Content filtering

### 💰 Economy
- Virtual currency (GM Coins)
- Daily bonuses
- Shop system
- Rewards and achievements

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/group-master-bot.git
cd group-master-bot
