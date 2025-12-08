"""
Configuration File for GROUP MASTER Telegram Bot
Complete Configuration - No Secrets Included
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    GROUP MASTER Bot Configuration
    All sensitive data loaded from environment variables
    """
    
    # ==================== BOT CONFIGURATION ====================
    BOT_NAME = "GROUP MASTER"
    BOT_USERNAME = "newgroup1o2bot"
    VERSION = "2.0.0"
    CREATOR = "MASTER"
    SUPPORT_CHAT = "@rana_editz_00"
    
    # ==================== SECURITY CONFIGURATION ====================
    # Get sensitive data from environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    # Firebase configuration
    FIREBASE_KEY = os.getenv("FIREBASE_KEY_PATH", "firebase-key.json")
    
    # ==================== VALIDATION ====================
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.BOT_TOKEN:
            errors.append("❌ BOT_TOKEN is required in .env file")
        
        if not cls.ADMIN_IDS:
            print("⚠️ Warning: ADMIN_IDS not configured")
        
        if not os.path.exists(cls.FIREBASE_KEY):
            print(f"⚠️ Warning: {cls.FIREBASE_KEY} not found")
        
        if errors:
            for error in errors:
                print(error)
            raise ValueError("Configuration validation failed")
    
    # ==================== AI SYSTEM CONFIGURATION ====================
    AI_CONFIG = {
        "name": "GM AI Brain",
        "learning_rate": 0.8,
        "memory_size": 1000,
        "min_confidence": 0.3,
        "max_patterns_per_word": 10,
        "forget_old_patterns": True,
        "forget_after_days": 30,
        "auto_save_interval": 300,  # 5 minutes
        "knowledge_file": "data/ai_knowledge.pkl",
        "supported_languages": ["bn", "en"],
        "default_language": "bn",
    }
    
    # ==================== GAME SYSTEM CONFIGURATION ====================
    GAME_CONFIG = {
        "max_active_games": 50,
        "game_timeout": 3600,  # 1 hour
        "max_players_per_game": 10,
        "auto_cleanup": True,
        "default_timeout": 300,  # 5 minutes
        
        # Game rewards
        "rewards": {
            "tic_tac_toe_win": 50,
            "tic_tac_toe_draw": 25,
            "quiz_correct": 10,
            "quiz_complete": 100,
            "hangman_win": 30,
            "math_correct": 5,
        },
        
        # Available games
        "available_games": [
            "tictactoe",
            "quiz",
            "hangman",
            "math",
            "chess",
            "ludo",
            "carrom",
            "word_chain",
            "riddle",
            "trivia"
        ],
    }
    
    # ==================== ECONOMY SYSTEM CONFIGURATION ====================
    ECONOMY_CONFIG = {
        "currency_name": "GM Coin",
        "currency_symbol": "🪙",
        "starting_balance": 1000,
        
        "daily_bonus": {
            "base_amount": 100,
            "streak_multiplier": 1.5,
            "max_streak": 30,
            "max_bonus": 5000,
        },
        
        "activity_rewards": {
            "message_sent": 1,
            "daily_active": 10,
            "invite_user": 100,
            "group_creator": 500,
        },
        
        "shop_items": {
            "shield": {"price": 500, "duration": 86400},
            "megaphone": {"price": 300, "uses": 3},
            "vip_badge": {"price": 1000, "duration": 2592000},
            "rainbow_name": {"price": 800, "duration": 604800},
        },
        
        "tax_rate": 0.05,  # 5% tax on transfers
        "interest_rate": 0.01,  # 1% daily interest
    }
    
    # ==================== MODERATION SYSTEM CONFIGURATION ====================
    MODERATION_CONFIG = {
        "max_warnings": 3,
        "warning_expiry_days": 30,
        
        "mute_durations": {
            "1st_warning": 3600,      # 1 hour
            "2nd_warning": 86400,     # 1 day
            "3rd_warning": 604800,    # 1 week
            "auto_mute": 3600,        # 1 hour for auto violations
        },
        
        "ban_duration": 2592000,  # 30 days
        "flood_limit": 5,  # messages per 10 seconds
        "max_message_length": 4000,
        
        "auto_moderation": {
            "enabled": True,
            "check_links": True,
            "check_flood": True,
            "check_caps": True,
            "check_spam": True,
        },
        
        "blacklist": {
            "words": [
                # English bad words
                "badword1", "badword2", "spam", "scam", "fraud",
                
                # Bengali bad words
                "অশ্লীল", "গালি", "স্প্যাম", "প্রতারণা", "জালিয়াতি",
                
                # Common spam phrases
                "earn money", "make money fast", "free money",
                "টাকা আয়", "দ্রুত টাকা", "ফ্রি টাকা",
            ],
            
            "links": [
                "spam.com",
                "scam.org",
                "free-money.com",
                "malware.site",
            ],
        },
    }
    
    # ==================== MINI APPS CONFIGURATION ====================
    APP_CONFIG = {
        "calculator": {
            "max_expression_length": 100,
            "allowed_functions": ["sin", "cos", "tan", "sqrt", "log"],
        },
        
        "converter": {
            "supported_units": {
                "length": ["meter", "km", "cm", "inch", "foot", "mile"],
                "weight": ["kg", "gram", "pound", "ounce"],
                "temperature": ["celsius", "fahrenheit", "kelvin"],
                "currency": ["bdt", "usd", "eur", "inr"],
            },
            "currency_rates": {
                "usd_bdt": 110.0,
                "eur_bdt": 120.0,
                "inr_bdt": 1.3,
            },
        },
        
        "dictionary": {
            "languages": ["en", "bn"],
            "max_word_length": 50,
        },
        
        "password_generator": {
            "min_length": 4,
            "max_length": 32,
            "default_length": 12,
        },
        
        "bmi_calculator": {
            "min_height": 50,   # cm
            "max_height": 300,  # cm
            "min_weight": 10,   # kg
            "max_weight": 300,  # kg
        },
    }
    
    # ==================== GROUP MANAGEMENT CONFIGURATION ====================
    GROUP_CONFIG = {
        "welcome_message": """
🎉 Welcome {user_mention} to {group_name}! 🎉

🤖 I am **GROUP MASTER** - Your AI-powered group assistant!

🌟 **Features Available:**
• 🤖 Self-learning AI
• 🎮 Interactive Games
• 📱 Mini Applications
• 🛡️ Smart Moderation
• 💰 Virtual Economy

📋 **Quick Commands:**
/help - See all commands
/rules - Group rules
/game - Play games
/ai - Chat with AI

📢 **Important:**
Please read the group rules using /rules
Be respectful to all members
Enjoy your stay! 😊
""",
        
        "rules_message": """
📜 **GROUP RULES**

1. 𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐄𝐯𝐞𝐫𝐲𝐨𝐧𝐞
   • No harassment or bullying
   • No hate speech
   • Be kind and respectful

2. 𝐍𝐨 𝐒𝐩𝐚𝐦𝐦𝐢𝐧𝐠
   • No excessive forwarding
   • No advertising without permission
   • No bot promotions

3. 𝐀𝐩𝐩𝐫𝐨𝐩𝐫𝐢𝐚𝐭𝐞 𝐂𝐨𝐧𝐭𝐞𝐧𝐭
   • No NSFW content
   • No illegal content
   • Keep it family-friendly

4. 𝐍𝐨 𝐏𝐨𝐥𝐢𝐭𝐢𝐜𝐬/𝐑𝐞𝐥𝐢𝐠𝐢𝐨𝐧
   • Avoid sensitive topics
   • No heated debates

5. 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞
   • Bengali & English allowed
   • No excessive use of other languages

🚨 **Violations:**
1st: Warning
2nd: 1-hour mute
3rd: 1-day mute
4th: Ban

🤝 Let's keep this group friendly and enjoyable for everyone!
""",
        
        "goodbye_message": "👋 Goodbye {user_name}! We'll miss you!",
        
        "report_channels": {
            "user_reports": -1001234567890,  # Channel ID for reports
            "admin_logs": -1001234567891,    # Channel ID for admin logs
        },
    }
    
    # ==================== SYSTEM CONFIGURATION ====================
    SYSTEM_CONFIG = {
        "log_level": "INFO",
        "log_to_file": True,
        "log_max_size": 10 * 1024 * 1024,  # 10 MB
        "log_backup_count": 5,
        
        "backup": {
            "enabled": True,
            "interval": 86400,  # 24 hours
            "keep_last": 7,
            "compress": True,
        },
        
        "maintenance": {
            "auto_restart": True,
            "restart_interval": 86400,  # 24 hours
            "maintenance_mode": False,
        },
        
        "performance": {
            "max_memory_usage": 512,  # MB
            "cleanup_interval": 3600,  # 1 hour
            "cache_ttl": 300,  # 5 minutes
        },
    }
    
    # ==================== FEATURE FLAGS ====================
    FEATURES = {
        "ai_learning": True,
        "games": True,
        "economy": True,
        "moderation": True,
        "apps": True,
        "analytics": True,
        "backup": True,
        "notifications": True,
        "multi_language": True,
        "web_dashboard": False,  # Future feature
    }
    
    # ==================== DATABASE CONFIGURATION ====================
    DATABASE_CONFIG = {
        "collections": {
            "users": "users",
            "groups": "groups",
            "messages": "messages",
            "games": "games",
            "transactions": "transactions",
            "warnings": "warnings",
            "logs": "logs",
            "analytics": "analytics",
        },
        
        "indexes": {
            "users": ["user_id", "username", "joined_at"],
            "groups": ["group_id", "created_at"],
            "messages": ["user_id", "chat_id", "timestamp"],
        },
        
        "cache": {
            "enabled": True,
            "ttl": 300,  # 5 minutes
            "max_size": 1000,
        },
    }
    
    # ==================== COMMAND CONFIGURATION ====================
    COMMAND_CONFIG = {
        "prefix": "/",
        "cooldown": 1,  # seconds between commands
        "max_args": 10,
        
        "categories": {
            "ai": ["ai", "chat", "teach", "ask", "brain"],
            "games": ["game", "play", "games", "stopgame", "score"],
            "apps": ["calc", "convert", "dict", "wiki", "weather", "time", "date"],
            "moderation": ["warn", "kick", "ban", "mute", "unban", "purge"],
            "economy": ["balance", "daily", "transfer", "shop", "buy", "inventory"],
            "group": ["rules", "welcome", "report", "admins", "settings"],
            "utility": ["start", "help", "ping", "about", "stats"],
        },
    }
    
    # ==================== MESSAGES & TEXTS ====================
    MESSAGES = {
        "errors": {
            "permission_denied": "❌ You don't have permission to use this command!",
            "user_not_found": "❌ User not found!",
            "invalid_input": "❌ Invalid input provided!",
            "game_not_found": "❌ Game not found!",
            "insufficient_balance": "❌ Insufficient balance!",
            "cooldown_active": "⏳ Please wait before using this command again!",
            "maintenance_mode": "🔧 Bot is under maintenance. Please try again later!",
        },
        
        "success": {
            "command_executed": "✅ Command executed successfully!",
            "user_warned": "⚠️ User has been warned!",
            "user_muted": "🔇 User has been muted!",
            "user_banned": "🚫 User has been banned!",
            "game_started": "🎮 Game started successfully!",
            "transaction_complete": "✅ Transaction completed!",
            "setting_updated": "⚙️ Setting updated successfully!",
        },
        
        "info": {
            "bot_started": "🤖 GROUP MASTER Bot has started!",
            "bot_stopped": "🛑 Bot has been stopped!",
            "backup_created": "💾 Backup created successfully!",
            "ai_learned": "🧠 AI learned new information!",
            "new_user": "👤 New user detected!",
            "new_group": "👥 New group detected!",
        },
    }


# Initialize and validate configuration
try:
    Config.validate()
    print(f"✅ {Config.BOT_NAME} Configuration loaded successfully!")
    print(f"📱 Version: {Config.VERSION}")
    print(f"👤 Creator: {Config.CREATOR}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    print("💡 Please check your .env file and configuration")