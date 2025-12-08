"""
Configuration File for GROUP MASTER Telegram Bot
SQLite Database Version - No Firebase Required
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    GROUP MASTER Bot Configuration
    SQLite Database - No External Services
    """
    
    # ==================== BOT CONFIGURATION ====================
    BOT_NAME = "GROUP MASTER"
    BOT_USERNAME = "GroupMasterBot"
    VERSION = "2.0.0"
    CREATOR = "GM Team"
    SUPPORT_CHAT = "@GroupMasterSupport"
    
    # ==================== DATABASE CONFIGURATION ====================
    DATABASE_TYPE = "sqlite"  # "sqlite" only - no firebase
    DATABASE_PATH = "data/bot_database.db"
    DATABASE_BACKUP_PATH = "backups/db_backup.db"
    
    # ==================== SECURITY CONFIGURATION ====================
    # Get sensitive data from environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    # ==================== VALIDATION ====================
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("❌ BOT_TOKEN is required in .env file")
        
        if not cls.ADMIN_IDS:
            print("⚠️ Warning: ADMIN_IDS not configured")
        
        # Create database directory if not exists
        db_dir = os.path.dirname(cls.DATABASE_PATH)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)
        
        if errors:
            for error in errors:
                print(error)
            raise ValueError("Configuration validation failed")
    
    # ==================== INITIALIZE DATABASE ====================
    @classmethod
    def init_database(cls):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(cls.DATABASE_PATH)
            cursor = conn.cursor()
            
            # Create tables
            tables = [
                """CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language_code TEXT,
                    balance INTEGER DEFAULT 1000,
                    warnings INTEGER DEFAULT 0,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS groups (
                    group_id INTEGER PRIMARY KEY,
                    title TEXT,
                    username TEXT,
                    welcome_message TEXT,
                    rules TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    text TEXT,
                    length INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    game_type TEXT,
                    player_id INTEGER,
                    status TEXT,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount INTEGER,
                    type TEXT,
                    reason TEXT,
                    balance_after INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    reason TEXT,
                    admin_id INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""",
                
                """CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )"""
            ]
            
            for table_sql in tables:
                cursor.execute(table_sql)
            
            conn.commit()
            conn.close()
            print(f"✅ Database initialized: {cls.DATABASE_PATH}")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    
    # ==================== AI SYSTEM CONFIGURATION ====================
    AI_CONFIG = {
        "name": "GM AI Brain",
        "learning_rate": 0.8,
        "memory_size": 1000,
        "min_confidence": 0.3,
        "knowledge_file": "data/ai_knowledge.pkl",
        "supported_languages": ["bn", "en"],
        "default_language": "bn",
    }
    
    # ==================== GAME SYSTEM CONFIGURATION ====================
    GAME_CONFIG = {
        "max_active_games": 50,
        "game_timeout": 3600,
        "max_players_per_game": 10,
        "auto_cleanup": True,
        
        "rewards": {
            "tic_tac_toe_win": 50,
            "tic_tac_toe_draw": 25,
            "quiz_correct": 10,
            "quiz_complete": 100,
            "hangman_win": 30,
            "math_correct": 5,
        },
        
        "available_games": [
            "tictactoe",
            "quiz",
            "hangman",
            "math",
            "word_chain",
            "riddle",
        ],
    }
    
    # ==================== ECONOMY SYSTEM ====================
    ECONOMY_CONFIG = {
        "currency_name": "GM Coin",
        "currency_symbol": "🪙",
        "starting_balance": 1000,
        
        "daily_bonus": {
            "base_amount": 100,
            "streak_multiplier": 1.5,
            "max_streak": 30,
        },
        
        "activity_rewards": {
            "message_sent": 1,
            "daily_active": 10,
        },
    }
    
    # ==================== MODERATION SYSTEM ====================
    MODERATION_CONFIG = {
        "max_warnings": 3,
        "warning_expiry_days": 30,
        
        "mute_durations": {
            "1st_warning": 3600,
            "2nd_warning": 86400,
            "3rd_warning": 604800,
        },
        
        "flood_limit": 5,
        "max_message_length": 4000,
        
        "blacklist": {
            "words": [
                "অশ্লীল", "গালি", "স্প্যাম", "প্রতারণা",
            ],
        },
    }
    
    # ==================== MINI APPS CONFIGURATION ====================
    APP_CONFIG = {
        "calculator": {
            "max_expression_length": 100,
        },
        
        "converter": {
            "supported_units": {
                "length": ["meter", "km", "cm", "inch", "foot"],
                "weight": ["kg", "gram", "pound"],
                "temperature": ["celsius", "fahrenheit"],
            },
        },
        
        "dictionary": {
            "languages": ["en", "bn"],
        },
        
        "password_generator": {
            "min_length": 4,
            "max_length": 32,
        },
    }
    
    # ==================== SYSTEM CONFIGURATION ====================
    SYSTEM_CONFIG = {
        "log_level": "INFO",
        "log_to_file": True,
        "log_path": "logs/bot.log",
        
        "backup": {
            "enabled": True,
            "interval": 86400,
            "keep_last": 7,
        },
        
        "performance": {
            "cleanup_interval": 3600,
        },
    }


# Initialize configuration
try:
    Config.validate()
    Config.init_database()
    
    print(f"✅ {Config.BOT_NAME} Configuration loaded successfully!")
    print(f"📱 Version: {Config.VERSION}")
    print(f"👤 Creator: {Config.CREATOR}")
    print(f"🗄️  Database: {Config.DATABASE_PATH}")
    
except Exception as e:
    print(f"❌ Configuration error: {e}")
    print("💡 Please check your .env file and configuration")
