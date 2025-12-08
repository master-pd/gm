"""
🤖 GROUP MASTER Telegram Bot - SQLite Version
Complete Package - No Firebase Required
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Local imports
from config import Config
from modules.ai_system import SelfLearningAI
from modules.game_system import GameSystem
from modules.app_system import MiniAppsSystem
from modules.moderation import ModerationSystem
from modules.economy import VirtualEconomy
from utils.database import Database
from utils.logger import setup_logger

# Setup logger
logger = setup_logger()

class GroupMasterBot:
    """Main Bot Class - SQLite Database"""
    
    def __init__(self):
        self.token = Config.BOT_TOKEN
        self.app = Application.builder().token(self.token).build()
        
        # Initialize all systems
        self.ai = SelfLearningAI()
        self.games = GameSystem()
        self.apps = MiniAppsSystem()
        self.moderator = ModerationSystem()
        self.economy = VirtualEconomy()
        self.db = Database()
        
        # Active sessions
        self.active_games = {}
        self.user_sessions = {}
        
        # Statistics
        self.stats = {
            'start_time': datetime.now(),
            'messages_processed': 0,
            'commands_executed': 0,
        }
        
        # Register handlers
        self._register_handlers()
        
        logger.info("🤖 GROUP MASTER Bot initialized with SQLite")
    
    def _register_handlers(self):
        """Register all command handlers"""
        
        # Basic commands
        self.app.add_handler(CommandHandler("start", self.command_start))
        self.app.add_handler(CommandHandler("help", self.command_help))
        self.app.add_handler(CommandHandler("ping", self.command_ping))
        
        # AI commands
        self.app.add_handler(CommandHandler("ai", self.command_ai))
        self.app.add_handler(CommandHandler("teach", self.command_teach))
        
        # Game commands
        self.app.add_handler(CommandHandler("game", self.command_game))
        self.app.add_handler(CommandHandler("play", self.command_play))
        
        # App commands
        self.app.add_handler(CommandHandler("calc", self.command_calc))
        self.app.add_handler(CommandHandler("dict", self.command_dict))
        self.app.add_handler(CommandHandler("joke", self.command_joke))
        self.app.add_handler(CommandHandler("quote", self.command_quote))
        
        # Moderation commands (admin only)
        self.app.add_handler(CommandHandler("warn", self.command_warn))
        self.app.add_handler(CommandHandler("kick", self.command_kick))
        
        # Economy commands
        self.app.add_handler(CommandHandler("balance", self.command_balance))
        self.app.add_handler(CommandHandler("daily", self.command_daily))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_members))
        
        # Callback handler
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        logger.info("✅ All handlers registered")
    
    # ==================== COMMAND HANDLERS ====================
    
    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_text = f"""
🤖 *GROUP MASTER Bot* 🚀

*স্বাগতম {user.mention_html()}!*

🎯 *ফিচার সমূহ:*
• 🤖 সেল্ফ-লার্নিং AI
• 🎮 ইন্টার‍্যাক্টিভ গেমস
• 📱 ইউজফুল অ্যাপস
• 🛡️ স্মার্ট মডারেশন
• 💰 ভার্চুয়াল ইকোনমি

📋 *কুইক কমান্ড:*
/help - সব কমান্ড
/ai - AI সাথে চ্যাট
/game - গেম খেলুন
/balance - আপনার ব্যালেন্স

*বটটি নিজে নিজে শিখবে!* 🧠
        """
        
        await update.message.reply_text(welcome_text, parse_mode='HTML')
        
        # Save user to database
        await self.db.save_user(user.id, {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code,
        })
        
        self.stats['commands_executed'] += 1
    
    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 *সব কমান্ড:*

*🤖 AI:*
/ai [message] - AI এর সাথে চ্যাট
/teach [প্রশ্ন] [উত্তর] - AI কে শেখান

*🎮 গেমস:*
/game - গেম মেনু
/play [game] - গেম খেলুন

*📱 অ্যাপস:*
/calc [expression] - ক্যালকুলেটর
/dict [word] - ডিকশনারি
/joke - মজার জোক
/quote - ইনস্পিরেশনাল উক্তি

*💰 ইকোনমি:*
/balance - ব্যালেন্স দেখুন
/daily - ডেইলি বোনাস নিন

*🛡️ মডারেশন (অ্যাডমিন):*
/warn [@user] - ওয়ার্ন দিন
/kick [@user] - কিক করুন

*🔧 ইউটিলিটি:*
/ping - বট স্ট্যাটাস
/help - এই মেসেজ
        """
        
        await update.message.reply_text(help_text)
    
    async def command_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ping command"""
        import time
        start_time = time.time()
        message = await update.message.reply_text("🏓 পিং...")
        end_time = time.time()
        
        latency = round((end_time - start_time) * 1000, 2)
        
        # Get database stats
        stats = await self.db.get_statistics()
        
        status_text = f"""
✅ *বট স্ট্যাটাস*

🏓 লেটেন্সি: {latency}ms
📊 মেসেজ প্রসেসড: {self.stats['messages_processed']}
👤 রেজিস্টার্ড ইউজার: {stats['users']}
💾 ডাটাবেস সাইজ: {stats['database_size'] / 1024:.1f} KB

🎮 একটিভ গেমস: {len(self.active_games)}
🧠 AI লার্নড: {self.ai.get_stats()['total_learned']}
        """
        
        await message.edit_text(status_text)
    
    async def command_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ai command"""
        if not context.args:
            await update.message.reply_text("💬 ব্যবহার: /ai [আপনার মেসেজ]")
            return
        
        user_message = ' '.join(context.args)
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Get AI response
        ai_response = self.ai.generate_response(user_message, user_id, chat_id)
        
        # Learn from this interaction
        self.ai.learn(user_message, ai_response, user_id, chat_id)
        
        await update.message.reply_text(f"🤖 *AI:* {ai_response}")
        
        self.stats['messages_processed'] += 1
    
    async def command_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /game command"""
        await update.message.reply_text(
            "🎮 *গেম মেনু*\n\n"
            "উপলব্ধ গেমস:\n"
            "• /play tictactoe - টিক ট্যাক টো\n"
            "• /play quiz - কুইজ গেম\n"
            "• /play hangman - হ্যাংম্যান\n"
            "• /play math - গণিত চ্যালেঞ্জ\n"
            "• /play wordchain - শব্দ শৃঙ্খল"
        )
    
    async def command_calc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /calc command"""
        if not context.args:
            await update.message.reply_text("📊 ব্যবহার: /calc [expression]\nউদা: /calc 5+3*2")
            return
        
        expression = ' '.join(context.args)
        result = await self.apps.calculator(expression)
        await update.message.reply_text(result)
    
    async def command_dict(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dict command"""
        if not context.args:
            await update.message.reply_text("📚 ব্যবহার: /dict [word]\nউদা: /dict hello")
            return
        
        word = context.args[0]
        result = await self.apps.dictionary(word)
        await update.message.reply_text(result)
    
    async def command_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command"""
        user_id = update.effective_user.id
        
        user_data = await self.db.get_user(user_id)
        balance = user_data.get('balance', 1000) if user_data else 1000
        
        await update.message.reply_text(
            f"💰 *আপনার ব্যালেন্স*\n\n"
            f"🪙 GM Coins: {balance}\n"
            f"📊 র‍্যাঙ্ক: Regular"
        )
    
    async def command_daily(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /daily command"""
        user_id = update.effective_user.id
        
        result = await self.economy.daily_bonus(user_id)
        
        if result['success']:
            # Add to user balance
            await self.db.update_user_balance(
                user_id, 
                result['amount'], 
                "Daily bonus"
            )
            
            await update.message.reply_text(
                f"🎁 *ডেইলি বোনাস!*\n\n"
                f"💰 পাওয়া গেছে: {result['amount']} GM Coins\n"
                f"🔥 স্ট্রীক: {result['streak']} দিন\n"
                f"🎯 টোটাল বোনাস: {result['total_bonus']}"
            )
        else:
            await update.message.reply_text(
                f"⏰ *অপেক্ষা করুন!*\n\n"
                f"❌ {result['message']}\n"
                f"🕐 পরবর্তী: {result['next_time']}"
            )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages"""
        message = update.message
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        
        # Update statistics
        self.stats['messages_processed'] += 1
        
        # Save message to database
        await self.db.save_message(user_id, chat_id, text)
        
        # Learn from messages in groups
        if chat_id < 0:  # Group chat
            # Auto-learn (20% chance)
            import random
            if random.random() < 0.2:
                ai_response = self.ai.generate_response(text, user_id, chat_id)
                self.ai.learn(text, ai_response, user_id, chat_id)
    
    async def handle_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new members joining"""
        for user in update.message.new_chat_members:
            if user.is_bot:
                continue
            
            welcome_text = f"""
🎉 *স্বাগতম {user.mention_html()}!* 🎉

🤖 আমি *GROUP MASTER Bot*
আপনার গ্রুপের AI সহকারী!

📋 *কিছু কমান্ড:*
/help - সব কমান্ড
/ai - আমার সাথে চ্যাট
/game - গেম খেলুন

*আমি বাংলা শিখছি!* 🇧🇩
            """
            
            await update.message.reply_text(welcome_text, parse_mode='HTML')
            
            # Give welcome bonus
            await self.db.update_user_balance(user.id, 500, "Welcome bonus")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_games":
            await self.command_game(update, context)
    
    async def start_background_tasks(self):
        """Start background tasks"""
        async def auto_save():
            """Auto-save AI knowledge"""
            while True:
                await asyncio.sleep(300)  # 5 minutes
                self.ai.save_knowledge()
                logger.info("💾 AI knowledge auto-saved")
        
        async def cleanup():
            """Cleanup old games"""
            while True:
                await asyncio.sleep(60)  # 1 minute
                import time
                current_time = time.time()
                
                # Cleanup old games
                to_remove = []
                for game_id, game in self.active_games.items():
                    if current_time - game.get('created', 0) > 3600:  # 1 hour
                        to_remove.append(game_id)
                
                for game_id in to_remove:
                    del self.active_games[game_id]
                
                if to_remove:
                    logger.info(f"🧹 Cleaned up {len(to_remove)} old games")
        
        # Start tasks
        asyncio.create_task(auto_save())
        asyncio.create_task(cleanup())
    
    def run(self):
        """Run the bot"""
        logger.info("🚀 Starting GROUP MASTER Bot...")
        
        # Start background tasks
        asyncio.run(self.start_background_tasks())
        
        # Start polling
        self.app.run_polling(drop_pending_updates=True)

def main():
    """Main function"""
    print(f"""
    🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
    🌟 GROUP MASTER TELEGRAM BOT 🌟
    🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
    
    🚀 Version: {Config.VERSION}
    👤 Creator: {Config.CREATOR}
    🗄️  Database: SQLite ({Config.DATABASE_PATH})
    
    Starting bot...
    """)
    
    # Create bot instance
    bot = GroupMasterBot()
    
    try:
        # Run bot
        bot.run()
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
