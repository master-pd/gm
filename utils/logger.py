"""
Logging Configuration for Telegram Bot
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Setup logger configuration"""
    
    # Create logs directory
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler for general logs
    file_handler = RotatingFileHandler(
        f"{logs_dir}/bot.log",
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    # File handler for errors
    error_handler = RotatingFileHandler(
        f"{logs_dir}/error.log",
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    # Set specific log levels for libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('firebase').setLevel(logging.WARNING)
    
    logger.info("=" * 50)
    logger.info("Logger initialized successfully")
    logger.info("=" * 50)
    
    return logger

def log_command(user_id: int, command: str, success: bool = True):
    """Log command usage"""
    logger = logging.getLogger(__name__)
    
    status = "✅" if success else "❌"
    logger.info(f"{status} Command: /{command} by user {user_id}")

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    logger = logging.getLogger(__name__)
    
    error_msg = f"❌ Error: {type(error).__name__}: {str(error)}"
    if context:
        error_msg += f" | Context: {context}"
    
    logger.error(error_msg)

def log_ai_learning(input_text: str, response: str, user_id: int):
    """Log AI learning"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"🧠 AI Learning - User: {user_id}")
    logger.info(f"   Input: {input_text[:100]}...")
    logger.info(f"   Response: {response[:100]}...")

def log_game_start(game_type: str, players: list):
    """Log game start"""
    logger = logging.getLogger(__name__)
    
    players_str = ", ".join(str(p) for p in players)
    logger.info(f"🎮 Game Started: {game_type} | Players: {players_str}")

def get_log_stats() -> Dict:
    """Get log statistics"""
    logs_dir = "logs"
    stats = {
        'total_size': 0,
        'file_count': 0,
        'last_modified': None
    }
    
    if os.path.exists(logs_dir):
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                file_path = os.path.join(logs_dir, file)
                stats['total_size'] += os.path.getsize(file_path)
                stats['file_count'] += 1
                
                # Get latest modification time
                mtime = os.path.getmtime(file_path)
                if stats['last_modified'] is None or mtime > stats['last_modified']:
                    stats['last_modified'] = mtime
        
        if stats['last_modified']:
            stats['last_modified'] = datetime.fromtimestamp(stats['last_modified']).isoformat()
    
    return stats