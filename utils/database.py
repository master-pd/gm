"""
Database Operations for Telegram Bot
"""

import json
import pickle
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import firebase_admin
from firebase_admin import firestore

class Database:
    """Database operations using Firebase Firestore"""
    
    def __init__(self):
        self.db = firestore.client()
        self.local_data_path = "data/local_data.json"
        self.backup_path = "backups/"
        
        # Initialize local storage
        os.makedirs(os.path.dirname(self.local_data_path), exist_ok=True)
        os.makedirs(self.backup_path, exist_ok=True)
        
        self.local_data = self._load_local_data()
    
    def _load_local_data(self) -> Dict:
        """Load local data from file"""
        if os.path.exists(self.local_data_path):
            try:
                with open(self.local_data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_local_data(self):
        """Save local data to file"""
        with open(self.local_data_path, 'w', encoding='utf-8') as f:
            json.dump(self.local_data, f, ensure_ascii=False, indent=2)
    
    # ==================== USER OPERATIONS ====================
    
    async def save_user(self, user_id: int, data: Dict):
        """Save user data to Firebase and local"""
        user_ref = self.db.collection('users').document(str(user_id))
        
        # Prepare data
        user_data = {
            **data,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'last_seen': firestore.SERVER_TIMESTAMP
        }
        
        # Save to Firebase
        user_ref.set(user_data, merge=True)
        
        # Save to local cache
        if 'users' not in self.local_data:
            self.local_data['users'] = {}
        
        self.local_data['users'][str(user_id)] = user_data
        self._save_local_data()
        
        return True
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        # Check local cache first
        if 'users' in self.local_data and str(user_id) in self.local_data['users']:
            return self.local_data['users'][str(user_id)]
        
        # Fetch from Firebase
        try:
            user_ref = self.db.collection('users').document(str(user_id))
            doc = user_ref.get()
            
            if doc.exists:
                user_data = doc.to_dict()
                
                # Cache locally
                if 'users' not in self.local_data:
                    self.local_data['users'] = {}
                self.local_data['users'][str(user_id)] = user_data
                self._save_local_data()
                
                return user_data
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")
        
        return None
    
    async def update_user_balance(self, user_id: int, amount: int, reason: str = ""):
        """Update user balance"""
        user_data = await self.get_user(user_id) or {}
        current_balance = user_data.get('balance', 1000)
        new_balance = current_balance + amount
        
        # Update user data
        user_data['balance'] = new_balance
        
        # Add transaction
        if 'transactions' not in user_data:
            user_data['transactions'] = []
        
        user_data['transactions'].append({
            'amount': amount,
            'type': 'credit' if amount > 0 else 'debit',
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'balance_after': new_balance
        })
        
        # Keep only last 100 transactions
        if len(user_data['transactions']) > 100:
            user_data['transactions'] = user_data['transactions'][-100:]
        
        # Save updated data
        await self.save_user(user_id, user_data)
        
        return new_balance
    
    # ==================== GROUP OPERATIONS ====================
    
    async def save_group(self, group_id: int, data: Dict):
        """Save group data"""
        group_ref = self.db.collection('groups').document(str(group_id))
        
        group_data = {
            **data,
            'updated_at': firestore.SERVER_TIMESTAMP
        }
        
        group_ref.set(group_data, merge=True)
        
        # Cache locally
        if 'groups' not in self.local_data:
            self.local_data['groups'] = {}
        
        self.local_data['groups'][str(group_id)] = group_data
        self._save_local_data()
        
        return True
    
    async def get_group(self, group_id: int) -> Optional[Dict]:
        """Get group data"""
        if 'groups' in self.local_data and str(group_id) in self.local_data['groups']:
            return self.local_data['groups'][str(group_id)]
        
        try:
            group_ref = self.db.collection('groups').document(str(group_id))
            doc = group_ref.get()
            
            if doc.exists:
                group_data = doc.to_dict()
                
                if 'groups' not in self.local_data:
                    self.local_data['groups'] = {}
                self.local_data['groups'][str(group_id)] = group_data
                self._save_local_data()
                
                return group_data
        except Exception as e:
            print(f"Error fetching group {group_id}: {e}")
        
        return None
    
    # ==================== MESSAGE OPERATIONS ====================
    
    async def save_message(self, user_id: int, chat_id: int, text: str):
        """Save message for analytics"""
        message_data = {
            'user_id': user_id,
            'chat_id': chat_id,
            'text': text[:1000],  # Limit text length
            'timestamp': firestore.SERVER_TIMESTAMP,
            'length': len(text)
        }
        
        # Save to Firebase
        messages_ref = self.db.collection('messages')
        messages_ref.add(message_data)
        
        # Update statistics
        await self.update_statistics('messages_processed')
        
        return True
    
    async def update_statistics(self, stat_name: str, increment: int = 1):
        """Update bot statistics"""
        stats_ref = self.db.collection('statistics').document('bot_stats')
        
        try:
            stats_ref.set({
                stat_name: firestore.Increment(increment),
                'updated_at': firestore.SERVER_TIMESTAMP
            }, merge=True)
        except:
            pass
    
    # ==================== GAME OPERATIONS ====================
    
    async def save_game_result(self, game_id: str, game_data: Dict):
        """Save game result"""
        games_ref = self.db.collection('games').document(game_id)
        
        game_data['ended_at'] = firestore.SERVER_TIMESTAMP
        games_ref.set(game_data, merge=True)
        
        return True
    
    async def get_user_games(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's recent games"""
        try:
            games_ref = self.db.collection('games')
            query = games_ref.where('players', 'array_contains', user_id)\
                            .order_by('ended_at', direction=firestore.Query.DESCENDING)\
                            .limit(limit)
            
            docs = query.get()
            games = [doc.to_dict() for doc in docs]
            return games
        except:
            return []
    
    # ==================== LEARNING OPERATIONS ====================
    
    async def save_learning(self, question: str, answer: str, user_id: int):
        """Save learning data"""
        learning_data = {
            'question': question,
            'answer': answer,
            'user_id': user_id,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'source': 'user_teaching'
        }
        
        learnings_ref = self.db.collection('learnings')
        learnings_ref.add(learning_data)
        
        return True
    
    # ==================== BACKUP OPERATIONS ====================
    
    async def create_backup(self):
        """Create database backup"""
        try:
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'users_count': 0,
                'groups_count': 0,
                'messages_count': 0
            }
            
            # Count users
            users_ref = self.db.collection('users')
            users_docs = users_ref.get()
            backup_data['users_count'] = len(users_docs)
            
            # Count groups
            groups_ref = self.db.collection('groups')
            groups_docs = groups_ref.get()
            backup_data['groups_count'] = len(groups_docs)
            
            # Save backup
            backup_file = f"{self.backup_path}backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    async def cleanup_old_backups(self, keep_last: int = 7):
        """Cleanup old backups"""
        try:
            if not os.path.exists(self.backup_path):
                return
            
            backup_files = []
            for file in os.listdir(self.backup_path):
                if file.startswith('backup_') and file.endswith('.json'):
                    file_path = os.path.join(self.backup_path, file)
                    backup_files.append((file_path, os.path.getmtime(file_path)))
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x[1])
            
            # Remove old backups
            for i in range(len(backup_files) - keep_last):
                os.remove(backup_files[i][0])
                print(f"🧹 Removed old backup: {backup_files[i][0]}")
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")