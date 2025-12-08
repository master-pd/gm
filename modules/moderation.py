"""
Moderation System for Telegram Bot
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class ModerationSystem:
    """Advanced Moderation System"""
    
    def __init__(self):
        self.warnings = defaultdict(list)
        self.muted_users = {}
        self.banned_users = {}
        self.flood_control = defaultdict(list)
        
    async def add_warning(self, user_id: int, chat_id: int, reason: str, admin_id: int) -> int:
        """Add warning to user"""
        warning = {
            'reason': reason,
            'timestamp': time.time(),
            'chat_id': chat_id,
            'admin_id': admin_id
        }
        
        self.warnings[f"{chat_id}_{user_id}"].append(warning)
        
        # Return total warnings
        return len(self.warnings[f"{chat_id}_{user_id}"])
    
    async def check_flood(self, user_id: int, chat_id: int) -> bool:
        """Check for message flooding"""
        key = f"{chat_id}_{user_id}"
        now = time.time()
        
        # Remove old timestamps (older than 10 seconds)
        self.flood_control[key] = [t for t in self.flood_control[key] if now - t < 10]
        
        # Add current timestamp
        self.flood_control[key].append(now)
        
        # Check if exceeds limit (5 messages in 10 seconds)
        return len(self.flood_control[key]) > 5
    
    async def check_content(self, text: str, chat_id: int) -> Tuple[bool, str]:
        """Check message content for violations"""
        # Check for blacklisted words
        blacklist = [
            'spam', 'scam', 'fraud', 'hack', 'cheat',
            'অশ্লীল', 'গালি', 'স্প্যাম', 'প্রতারণা'
        ]
        
        text_lower = text.lower()
        for word in blacklist:
            if word in text_lower:
                return False, f"Blacklisted word detected: {word}"
        
        # Check for excessive caps
        if len(text) > 10:
            caps_count = sum(1 for c in text if c.isupper())
            if caps_count / len(text) > 0.7:  # More than 70% caps
                return False, "Excessive capital letters detected"
        
        # Check for spam links
        spam_domains = ['spam.com', 'scam.org', 'free-money.com']
        for domain in spam_domains:
            if domain in text_lower:
                return False, f"Spam link detected: {domain}"
        
        # Check message length
        if len(text) > 4000:
            return False, "Message too long (max 4000 characters)"
        
        return True, "Content OK"