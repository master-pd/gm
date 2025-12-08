
import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import aiosqlite
from pathlib import Path

class Database:
    """SQLite Database operations"""
    
    def __init__(self, db_path="data/bot_database.db"):
        self.db_path = db_path
        self.local_data_path = "data/local_data.json"
        
        # Initialize directories
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.local_data_path), exist_ok=True)
        
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
    
    # ==================== SYNC OPERATIONS ====================
    
    def get_connection(self):
        """Get SQLite connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ==================== USER OPERATIONS ====================
    
    async def save_user(self, user_id: int, data: Dict) -> bool:
        """Save user data to SQLite"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                # Check if user exists
                await cursor.execute(
                    "SELECT user_id FROM users WHERE user_id = ?",
                    (user_id,)
                )
                exists = await cursor.fetchone()
                
                if exists:
                    # Update existing user
                    await cursor.execute("""
                        UPDATE users SET 
                        username = ?, first_name = ?, last_name = ?,
                        language_code = ?, last_seen = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    """, (
                        data.get('username'),
                        data.get('first_name'),
                        data.get('last_name'),
                        data.get('language_code'),
                        user_id
                    ))
                else:
                    # Insert new user
                    await cursor.execute("""
                        INSERT INTO users 
                        (user_id, username, first_name, last_name, language_code, balance)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        data.get('username'),
                        data.get('first_name'),
                        data.get('last_name'),
                        data.get('language_code'),
                        data.get('balance', 1000)
                    ))
                
                await db.commit()
                
                # Cache locally
                if 'users' not in self.local_data:
                    self.local_data['users'] = {}
                self.local_data['users'][str(user_id)] = data
                self._save_local_data()
                
                return True
                
        except Exception as e:
            print(f"Error saving user {user_id}: {e}")
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        # Check local cache first
        if 'users' in self.local_data and str(user_id) in self.local_data['users']:
            return self.local_data['users'][str(user_id)]
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = sqlite3.Row
                cursor = await db.cursor()
                
                await cursor.execute(
                    "SELECT * FROM users WHERE user_id = ?",
                    (user_id,)
                )
                row = await cursor.fetchone()
                
                if row:
                    user_data = dict(row)
                    
                    # Cache locally
                    if 'users' not in self.local_data:
                        self.local_data['users'] = {}
                    self.local_data['users'][str(user_id)] = user_data
                    self._save_local_data()
                    
                    return user_data
                    
        except Exception as e:
            print(f"Error fetching user {user_id}: {e}")
        
        return None
    
    async def update_user_balance(self, user_id: int, amount: int, reason: str = "") -> int:
        """Update user balance"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                # Get current balance
                await cursor.execute(
                    "SELECT balance FROM users WHERE user_id = ?",
                    (user_id,)
                )
                result = await cursor.fetchone()
                
                if result:
                    current_balance = result[0]
                    new_balance = current_balance + amount
                    
                    # Update balance
                    await cursor.execute(
                        "UPDATE users SET balance = ? WHERE user_id = ?",
                        (new_balance, user_id)
                    )
                    
                    # Add transaction
                    await cursor.execute("""
                        INSERT INTO transactions 
                        (user_id, amount, type, reason, balance_after)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        amount,
                        'credit' if amount > 0 else 'debit',
                        reason,
                        new_balance
                    ))
                    
                    await db.commit()
                    
                    # Update local cache
                    if 'users' in self.local_data and str(user_id) in self.local_data['users']:
                        self.local_data['users'][str(user_id)]['balance'] = new_balance
                        self._save_local_data()
                    
                    return new_balance
                    
        except Exception as e:
            print(f"Error updating balance for {user_id}: {e}")
        
        return 0
    
    # ==================== GROUP OPERATIONS ====================
    
    async def save_group(self, group_id: int, data: Dict) -> bool:
        """Save group data"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                await cursor.execute("""
                    INSERT OR REPLACE INTO groups 
                    (group_id, title, username, welcome_message, rules)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    group_id,
                    data.get('title'),
                    data.get('username'),
                    data.get('welcome_message', ''),
                    data.get('rules', '')
                ))
                
                await db.commit()
                
                # Cache locally
                if 'groups' not in self.local_data:
                    self.local_data['groups'] = {}
                self.local_data['groups'][str(group_id)] = data
                self._save_local_data()
                
                return True
                
        except Exception as e:
            print(f"Error saving group {group_id}: {e}")
            return False
    
    async def get_group(self, group_id: int) -> Optional[Dict]:
        """Get group data"""
        if 'groups' in self.local_data and str(group_id) in self.local_data['groups']:
            return self.local_data['groups'][str(group_id)]
        
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = sqlite3.Row
                cursor = await db.cursor()
                
                await cursor.execute(
                    "SELECT * FROM groups WHERE group_id = ?",
                    (group_id,)
                )
                row = await cursor.fetchone()
                
                if row:
                    group_data = dict(row)
                    
                    if 'groups' not in self.local_data:
                        self.local_data['groups'] = {}
                    self.local_data['groups'][str(group_id)] = group_data
                    self._save_local_data()
                    
                    return group_data
                    
        except Exception as e:
            print(f"Error fetching group {group_id}: {e}")
        
        return None
    
    # ==================== MESSAGE OPERATIONS ====================
    
    async def save_message(self, user_id: int, chat_id: int, text: str) -> bool:
        """Save message for analytics"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                await cursor.execute("""
                    INSERT INTO messages 
                    (user_id, chat_id, text, length)
                    VALUES (?, ?, ?, ?)
                """, (
                    user_id,
                    chat_id,
                    text[:1000],  # Limit text length
                    len(text)
                ))
                
                await db.commit()
                return True
                
        except Exception as e:
            print(f"Error saving message: {e}")
            return False
    
    # ==================== GAME OPERATIONS ====================
    
    async def save_game_result(self, game_id: str, game_data: Dict) -> bool:
        """Save game result"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                await cursor.execute("""
                    INSERT INTO games 
                    (game_id, game_type, player_id, status, data)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    game_id,
                    game_data.get('type'),
                    game_data.get('player'),
                    game_data.get('status', 'finished'),
                    json.dumps(game_data)
                ))
                
                await db.commit()
                return True
                
        except Exception as e:
            print(f"Error saving game {game_id}: {e}")
            return False
    
    async def get_user_games(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user's recent games"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = sqlite3.Row
                cursor = await db.cursor()
                
                await cursor.execute("""
                    SELECT * FROM games 
                    WHERE player_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (user_id, limit))
                
                rows = await cursor.fetchall()
                games = []
                
                for row in rows:
                    game = dict(row)
                    try:
                        game['data'] = json.loads(game['data'])
                    except:
                        game['data'] = {}
                    games.append(game)
                
                return games
                
        except Exception as e:
            print(f"Error fetching games for {user_id}: {e}")
            return []
    
    # ==================== WARNING OPERATIONS ====================
    
    async def add_warning(self, user_id: int, chat_id: int, reason: str, admin_id: int) -> int:
        """Add warning to user"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                # Add warning
                await cursor.execute("""
                    INSERT INTO warnings 
                    (user_id, chat_id, reason, admin_id)
                    VALUES (?, ?, ?, ?)
                """, (user_id, chat_id, reason, admin_id))
                
                # Count total warnings
                await cursor.execute(
                    "SELECT COUNT(*) FROM warnings WHERE user_id = ?",
                    (user_id,)
                )
                result = await cursor.fetchone()
                total_warnings = result[0] if result else 0
                
                await db.commit()
                
                # Update user warnings count
                await cursor.execute(
                    "UPDATE users SET warnings = ? WHERE user_id = ?",
                    (total_warnings, user_id)
                )
                
                await db.commit()
                return total_warnings
                
        except Exception as e:
            print(f"Error adding warning for {user_id}: {e}")
            return 0
    
    # ==================== BACKUP OPERATIONS ====================
    
    async def create_backup(self) -> str:
        """Create database backup"""
        try:
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_file = f"{backup_dir}/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            # Simple file copy for SQLite
            import shutil
            shutil.copy2(self.db_path, backup_file)
            
            print(f"✅ Backup created: {backup_file}")
            return backup_file
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return ""
    
    async def cleanup_old_backups(self, keep_last: int = 7):
        """Cleanup old backups"""
        try:
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                return
            
            backup_files = []
            for file in os.listdir(backup_dir):
                if file.startswith('backup_') and file.endswith('.db'):
                    file_path = os.path.join(backup_dir, file)
                    backup_files.append((file_path, os.path.getmtime(file_path)))
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x[1])
            
            # Remove old backups
            for i in range(len(backup_files) - keep_last):
                os.remove(backup_files[i][0])
                print(f"🧹 Removed old backup: {backup_files[i][0]}")
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
    
    # ==================== STATISTICS ====================
    
    async def get_statistics(self) -> Dict:
        """Get database statistics"""
        stats = {
            'users': 0,
            'groups': 0,
            'messages': 0,
            'games': 0,
            'warnings': 0,
            'database_size': 0
        }
        
        try:
            # Get file size
            if os.path.exists(self.db_path):
                stats['database_size'] = os.path.getsize(self.db_path)
            
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.cursor()
                
                # Count users
                await cursor.execute("SELECT COUNT(*) FROM users")
                result = await cursor.fetchone()
                stats['users'] = result[0] if result else 0
                
                # Count groups
                await cursor.execute("SELECT COUNT(*) FROM groups")
                result = await cursor.fetchone()
                stats['groups'] = result[0] if result else 0
                
                # Count messages
                await cursor.execute("SELECT COUNT(*) FROM messages")
                result = await cursor.fetchone()
                stats['messages'] = result[0] if result else 0
                
                # Count games
                await cursor.execute("SELECT COUNT(*) FROM games")
                result = await cursor.fetchone()
                stats['games'] = result[0] if result else 0
                
                # Count warnings
                await cursor.execute("SELECT COUNT(*) FROM warnings")
                result = await cursor.fetchone()
                stats['warnings'] = result[0] if result else 0
                
        except Exception as e:
            print(f"Error getting statistics: {e}")
        
        return stats
