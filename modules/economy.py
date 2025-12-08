"""
Virtual Economy System for Telegram Bot
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class VirtualEconomy:
    """Virtual Economy System"""
    
    def __init__(self):
        self.daily_bonus_tracking = {}
        self.transaction_history = defaultdict(list)
        
    async def daily_bonus(self, user_id: int) -> Dict:
        """Give daily bonus to user"""
        current_time = time.time()
        today = datetime.now().date().isoformat()
        
        # Check if already claimed today
        if user_id in self.daily_bonus_tracking:
            last_claim = self.daily_bonus_tracking[user_id]
            if last_claim['date'] == today:
                next_claim = datetime.now() + timedelta(days=1)
                return {
                    'success': False,
                    'message': 'Already claimed today',
                    'next_time': next_claim.strftime('%H:%M')
                }
        
        # Calculate bonus amount
        base_bonus = 100
        streak = self.daily_bonus_tracking.get(user_id, {}).get('streak', 0) + 1
        bonus_amount = base_bonus * (1 + (streak * 0.1))  # 10% increase per streak
        
        # Update tracking
        self.daily_bonus_tracking[user_id] = {
            'date': today,
            'streak': streak,
            'amount': bonus_amount,
            'total_claimed': self.daily_bonus_tracking.get(user_id, {}).get('total_claimed', 0) + bonus_amount
        }
        
        # Record transaction
        self.transaction_history[user_id].append({
            'type': 'daily_bonus',
            'amount': bonus_amount,
            'timestamp': current_time,
            'streak': streak
        })
        
        return {
            'success': True,
            'amount': int(bonus_amount),
            'streak': streak,
            'next_bonus': '24 hours',
            'total_bonus': self.daily_bonus_tracking[user_id]['total_claimed']
        }
    
    async def get_daily_streak(self, user_id: int) -> int:
        """Get user's daily streak"""
        if user_id in self.daily_bonus_tracking:
            return self.daily_bonus_tracking[user_id].get('streak', 0)
        return 0