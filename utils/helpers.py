"""
Helper Functions for Telegram Bot
"""

import re
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

def format_time(seconds: int) -> str:
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{int(minutes)}m"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{int(days)}d {int(hours)}h"

def format_number(num: int) -> str:
    """Format number with K, M, B suffixes"""
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num/1000:.1f}K"
    elif num < 1000000000:
        return f"{num/1000000:.1f}M"
    else:
        return f"{num/1000000000:.1f}B"

def validate_input(text: str, max_length: int = 1000) -> bool:
    """Validate user input"""
    if not text or len(text.strip()) == 0:
        return False
    
    if len(text) > max_length:
        return False
    
    # Check for excessive special characters
    special_chars = re.findall(r'[^\w\s]', text)
    if len(special_chars) > len(text) * 0.5:  # More than 50% special chars
        return False
    
    return True

def extract_mentions(text: str) -> List[str]:
    """Extract @mentions from text"""
    return re.findall(r'@(\w+)', text)

def extract_hashtags(text: str) -> List[str]:
    """Extract #hashtags from text"""
    return re.findall(r'#(\w+)', text)

def clean_text(text: str) -> str:
    """Clean text by removing extra spaces and newlines"""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with single newline
    return text.strip()

def split_message(text: str, max_length: int = 4000) -> List[str]:
    """Split long message into multiple parts"""
    if len(text) <= max_length:
        return [text]
    
    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break
        
        # Try to split at sentence boundary
        split_point = text.rfind('. ', 0, max_length)
        if split_point == -1:
            split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        
        parts.append(text[:split_point].strip())
        text = text[split_point:].strip()
    
    return parts

def generate_random_string(length: int = 8) -> str:
    """Generate random string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (0-1)"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def parse_time_duration(time_str: str) -> Optional[int]:
    """Parse time duration string to seconds"""
    time_str = time_str.lower().strip()
    
    multipliers = {
        's': 1,
        'sec': 1,
        'second': 1,
        'm': 60,
        'min': 60,
        'minute': 60,
        'h': 3600,
        'hour': 3600,
        'd': 86400,
        'day': 86400,
        'w': 604800,
        'week': 604800
    }
    
    try:
        # Extract number and unit
        match = re.match(r'(\d+)\s*([a-z]+)', time_str)
        if match:
            number = int(match.group(1))
            unit = match.group(2)
            
            if unit in multipliers:
                return number * multipliers[unit]
        
        # Try just number (default to minutes)
        if time_str.isdigit():
            return int(time_str) * 60
            
    except:
        pass
    
    return None

def get_bangla_number(num: int) -> str:
    """Convert number to Bangla digits"""
    bangla_digits = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }
    
    num_str = str(num)
    result = ''
    for char in num_str:
        result += bangla_digits.get(char, char)
    
    return result

def get_emoji_for_mood(score: float) -> str:
    """Get emoji based on sentiment score"""
    if score >= 0.8:
        return "😊"
    elif score >= 0.6:
        return "🙂"
    elif score >= 0.4:
        return "😐"
    elif score >= 0.2:
        return "😕"
    else:
        return "😢"

def format_currency(amount: int) -> str:
    """Format currency amount"""
    if amount >= 1000000:
        return f"৳{amount/1000000:.2f}M"
    elif amount >= 1000:
        return f"৳{amount/1000:.1f}K"
    else:
        return f"৳{amount}"

def get_progress_bar(percentage: float, length: int = 10) -> str:
    """Get progress bar string"""
    filled = int(percentage * length)
    empty = length - filled
    return "█" * filled + "░" * empty

def calculate_level_from_xp(xp: int) -> Tuple[int, int, int]:
    """Calculate level from XP"""
    # Simple exponential leveling system
    level = 1
    xp_needed = 100
    
    while xp >= xp_needed:
        xp -= xp_needed
        level += 1
        xp_needed = int(xp_needed * 1.5)
    
    xp_current = xp
    xp_required = xp_needed
    
    return level, xp_current, xp_required