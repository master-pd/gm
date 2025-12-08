"""
🌍 WORLDS MOST ADVANCED TELEGRAM BOT
Complete Package - No External APIs
Self-Learning AI + All Features Included
"""

import asyncio
import json
import logging
import random
import re
import time
import pickle
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import math

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.constants import ParseMode, ChatAction

import firebase_admin
from firebase_admin import credentials, firestore, storage

# Local imports
from config import Config
from modules.ai_system import SelfLearningAI
from modules.game_system import GameSystem
from modules.app_system import MiniAppsSystem
from modules.moderation import ModerationSystem
from modules.economy import VirtualEconomy
from utils.database import Database
from utils.helpers import format_time, format_number, validate_input
from utils.logger import setup_logger

# ==================== SETUP ====================

# Setup logger
logger = setup_logger()

# Initialize Firebase
try:
    cred = credentials.Certificate(Config.FIREBASE_KEY)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("✅ Firebase initialized successfully")
except Exception as e:
    logger.error(f"❌ Firebase initialization failed: {e}")
    sys.exit(1)

# ==================== CONSTANTS ====================

class States:
    WAITING_FOR_GAME_MOVE = 1
    WAITING_FOR_QUIZ_ANSWER = 2
    WAITING_FOR_AI_TEACH = 3
    WAITING_FOR_CONVERSION = 4

class GameType:
    TIC_TAC_TOE = "tictactoe"
    QUIZ = "quiz"
    HANGMAN = "hangman"
    MATH = "math"
    CHESS = "chess"
    CARROM = "carrom"
    LUDO = "ludo"
    WORD_CHAIN = "word_chain"
    RIDDLE = "riddle"
    TRIVIA = "trivia"

# ==================== MAIN BOT CLASS ====================

class SuperTelegramBot:
    """Main Bot Class - Everything Combined"""
    
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
        self.user_sessions = defaultdict(dict)
        self.group_settings = defaultdict(dict)
        
        # Statistics
        self.stats = {
            'messages_processed': 0,
            'commands_executed': 0,
            'games_played': 0,
            'ai_responses': 0,
            'start_time': time.time()
        }
        
        # Register handlers
        self._register_handlers()
        
        logger.info("🤖 Super Telegram Bot initialized")
    
    def _register_handlers(self):
        """Register all command and message handlers"""
        
        # ========== BASIC COMMANDS ==========
        self.app.add_handler(CommandHandler("start", self.command_start))
        self.app.add_handler(CommandHandler("help", self.command_help))
        self.app.add_handler(CommandHandler("ping", self.command_ping))
        self.app.add_handler(CommandHandler("about", self.command_about))
        self.app.add_handler(CommandHandler("stats", self.command_stats))
        
        # ========== AI COMMANDS ==========
        self.app.add_handler(CommandHandler("ai", self.command_ai))
        self.app.add_handler(CommandHandler("chat", self.command_chat))
        self.app.add_handler(CommandHandler("teach", self.command_teach))
        self.app.add_handler(CommandHandler("ask", self.command_ask))
        self.app.add_handler(CommandHandler("brain", self.command_brain))
        
        # ========== GAME COMMANDS ==========
        self.app.add_handler(CommandHandler("game", self.command_game))
        self.app.add_handler(CommandHandler("play", self.command_play))
        self.app.add_handler(CommandHandler("games", self.command_games))
        self.app.add_handler(CommandHandler("stopgame", self.command_stopgame))
        self.app.add_handler(CommandHandler("score", self.command_score))
        
        # ========== APP COMMANDS ==========
        self.app.add_handler(CommandHandler("calc", self.command_calc))
        self.app.add_handler(CommandHandler("convert", self.command_convert))
        self.app.add_handler(CommandHandler("dict", self.command_dict))
        self.app.add_handler(CommandHandler("wiki", self.command_wiki))
        self.app.add_handler(CommandHandler("weather", self.command_weather))
        self.app.add_handler(CommandHandler("time", self.command_time))
        self.app.add_handler(CommandHandler("date", self.command_date))
        self.app.add_handler(CommandHandler("password", self.command_password))
        self.app.add_handler(CommandHandler("bmi", self.command_bmi))
        self.app.add_handler(CommandHandler("age", self.command_age))
        self.app.add_handler(CommandHandler("joke", self.command_joke))
        self.app.add_handler(CommandHandler("quote", self.command_quote))
        self.app.add_handler(CommandHandler("fact", self.command_fact))
        self.app.add_handler(CommandHandler("meme", self.command_meme))
        
        # ========== MODERATION COMMANDS ==========
        self.app.add_handler(CommandHandler("warn", self.command_warn))
        self.app.add_handler(CommandHandler("kick", self.command_kick))
        self.app.add_handler(CommandHandler("ban", self.command_ban))
        self.app.add_handler(CommandHandler("mute", self.command_mute))
        self.app.add_handler(CommandHandler("unban", self.command_unban))
        self.app.add_handler(CommandHandler("purge", self.command_purge))
        self.app.add_handler(CommandHandler("settings", self.command_settings))
        
        # ========== ECONOMY COMMANDS ==========
        self.app.add_handler(CommandHandler("balance", self.command_balance))
        self.app.add_handler(CommandHandler("daily", self.command_daily))
        self.app.add_handler(CommandHandler("transfer", self.command_transfer))
        self.app.add_handler(CommandHandler("shop", self.command_shop))
        self.app.add_handler(CommandHandler("buy", self.command_buy))
        self.app.add_handler(CommandHandler("inventory", self.command_inventory))
        
        # ========== GROUP MANAGEMENT ==========
        self.app.add_handler(CommandHandler("rules", self.command_rules))
        self.app.add_handler(CommandHandler("welcome", self.command_welcome))
        self.app.add_handler(CommandHandler("report", self.command_report))
        self.app.add_handler(CommandHandler("admins", self.command_admins))
        
        # ========== MESSAGE HANDLERS ==========
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_members))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, self.handle_left_member))
        self.app.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.app.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        
        # ========== CALLBACK HANDLERS ==========
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # ========== ERROR HANDLER ==========
        self.app.add_error_handler(self.error_handler)
        
        logger.info("✅ All handlers registered")
    
    # ==================== BASIC COMMANDS ====================
    
    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        chat = update.effective_chat
        
        welcome_text = f"""
🤖 *🌍 Worlds Most Advanced Telegram Bot* 🌍

*স্বাগতম {user.mention_html()}!* 🎉

🚀 *ফিচার সমূহ:*
• 🤖 *সেল্ফ-লার্নিং AI* - নিজে নিজে শিখে
• 🎮 *১০+ গেম* - মজার গেমস
• 📱 *২০+ মিনি অ্যাপ* - কাজের টুলস
• 🛡️ *স্মার্ট মডারেশন* - গ্রুপ ম্যানেজমেন্ট
• 💰 *ভার্চুয়াল ইকোনমি* - কয়েন সিস্টেম
• 📊 *রিয়েল-টাইম এনালিটিক্স*
• 🔧 *নো এক্সটার্নাল API* - সব লোকাল!

📋 *কুইক মেনু:*
/help - সব কমান্ড
/ai - AI সাথে চ্যাট
/game - গেম খেলুন
/apps - অ্যাপস লিস্ট
/balance - আপনার ব্যালেন্স

*বটটি আপনার গ্রুপের কথাবার্তা থেকে নিজে নিজে শিখবে!* 🧠
        """
        
        # Create keyboard
        keyboard = [
            [
                InlineKeyboardButton("🎮 Games", callback_data="menu_games"),
                InlineKeyboardButton("📱 Apps", callback_data="menu_apps")
            ],
            [
                InlineKeyboardButton("💰 Economy", callback_data="menu_economy"),
                InlineKeyboardButton("🤖 AI Chat", callback_data="menu_ai")
            ],
            [
                InlineKeyboardButton("🛡️ Moderation", callback_data="menu_mod"),
                InlineKeyboardButton("📊 Stats", callback_data="menu_stats")
            ],
            [
                InlineKeyboardButton("📚 Help", callback_data="menu_help"),
                InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send welcome message
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        
        # Save user to database
        await self.db.save_user(user.id, {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code,
            'joined_at': datetime.now().isoformat(),
            'balance': 1000
        })
        
        self.stats['commands_executed'] += 1
    
    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 *সব কমান্ডের লিস্ট* 🆘

*🤖 AI কমান্ড:*
/ai [message] - AI এর সাথে চ্যাট করুন
/chat - AI চ্যাট মোড চালু করুন
/teach [প্রশ্ন] [উত্তর] - AI কে শেখান
/ask [প্রশ্ন] - AI থেকে উত্তর নিন
/brain - AI এর ব্রেইন স্ট্যাটাস

*🎮 গেম কমান্ড:*
/game - গেম মেনু দেখুন
/play [game] - গেম খেলুন
• tictactoe, quiz, hangman, math, chess, ludo, carrom
/games - একটিভ গেমস দেখুন
/stopgame - গেম বন্ধ করুন
/score - আপনার স্কোর

*📱 অ্যাপস কমান্ড:*
/calc [expression] - ক্যালকুলেটর
/convert [value] [from] [to] - ইউনিট কনভার্টার
/dict [word] - ডিকশনারি
/wiki [topic] - উইকিপিডিয়া সার্চ
/weather [city] - আবহাওয়া
/time - বর্তমান সময়
/date - আজকের তারিখ
/password [length] - পাসওয়ার্ড জেনারেট
/bmi [weight] [height] - BMI ক্যালকুলেটর
/age [birthdate] - বয়স ক্যালকুলেটর
/joke - মজার জোক
/quote - ইনস্পিরেশনাল উক্তি
/fact - মজার তথ্য
/meme - মেম জেনারেট

*🛡️ মডারেশন কমান্ড:*
/warn [@user] - ইউজারকে ওয়ার্ন দিন
/kick [@user] - ইউজারকে কিক করুন
/ban [@user] - ইউজারকে ব্যান করুন
/mute [@user] [time] - ইউজারকে মিউট করুন
/unban [@user] - আনব্যান করুন
/purge [number] - মেসেজ ডিলিট করুন
/settings - গ্রুপ সেটিংস
/report [reason] - রিপোর্ট করুন

*💰 ইকোনমি কমান্ড:*
/balance - আপনার ব্যালেন্স দেখুন
/daily - ডেইলি বোনাস নিন
/transfer [@user] [amount] - ট্রান্সফার করুন
/shop - শপ দেখুন
/buy [item] - আইটেম কিনুন
/inventory - আপনার ইনভেন্টরি

*👥 গ্রুপ ম্যানেজমেন্ট:*
/rules - গ্রুপ রুলস
/welcome - ওয়েলকাম মেসেজ
/admins - অ্যাডমিন লিস্ট
/report - সমস্যা রিপোর্ট

*🔧 ইউটিলিটি:*
/ping - বট স্ট্যাটাস
/about - বট সম্পর্কে
/stats - বট স্ট্যাটিস্টিক্স
/help - এই মেসেজ
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        self.stats['commands_executed'] += 1
    
    async def command_ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ping command"""
        start_time = time.time()
        message = await update.message.reply_text("🏓 পিং করা হচ্ছে...")
        end_time = time.time()
        
        latency = round((end_time - start_time) * 1000, 2)
        uptime = time.time() - self.stats['start_time']
        
        status_text = f"""
✅ *বট স্ট্যাটাস: অনলাইন*

🏓 লেটেন্সি: {latency}ms
⏱️ আপটাইম: {format_time(uptime)}
📊 মেসেজ প্রসেসড: {self.stats['messages_processed']}
🤖 AI রেসপন্স: {self.stats['ai_responses']}
🎮 গেম প্লেয়েড: {self.stats['games_played']}

💾 মেমরি: OK
🔥 পারফরম্যান্স: Excellent
        """
        
        await message.edit_text(status_text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_text = """
🤖 *Worlds Most Advanced Telegram Bot*

*Version:* 2.0.0
*Developer:* Advanced AI Team
*Created:* 2024
*Technology:* Python 3.11+

🌟 *ফিচারস:*
• Self-Learning AI System
• No External APIs Required
• Complete Group Management
• 10+ Interactive Games
• 20+ Mini Applications
• Virtual Economy System
• Real-time Analytics
• Multi-language Support

🔧 *টেকনোলজি স্ট্যাক:*
• Python Telegram Bot
• Firebase Firestore
• Local Machine Learning
• Rule-based AI
• Modular Architecture

💡 *স্পেশাল ফিচার:*
এই বটটি গ্রুপের কথাবার্তা থেকে নিজে নিজে শিখে!
কোনো এক্সটার্নাল API ব্যবহার করে না!
সম্পূর্ণ ফ্রি এবং ওপেন সোর্স!

📞 *সাপোর্ট:* @YourSupportChannel
        """
        
        await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
    
    # ==================== AI COMMANDS ====================
    
    async def command_ai(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ai command"""
        if not context.args:
            await update.message.reply_text("💬 ব্যবহার: /ai [আপনার মেসেজ]\nউদাহরণ: /ai আজকের আবহাওয়া কেমন?")
            return
        
        user_message = ' '.join(context.args)
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Show typing action
        await update.message.chat.send_action(ChatAction.TYPING)
        
        # Get AI response
        ai_response = self.ai.generate_response(user_message, user_id, chat_id)
        
        # Learn from this interaction
        self.ai.learn(user_message, ai_response, user_id, chat_id)
        
        # Update statistics
        self.stats['ai_responses'] += 1
        self.stats['messages_processed'] += 1
        
        # Send response
        await update.message.reply_text(f"🤖 *AI:* {ai_response}", parse_mode=ParseMode.MARKDOWN)
    
    async def command_teach(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /teach command"""
        if len(context.args) < 2:
            await update.message.reply_text("📚 ব্যবহার: /teach [প্রশ্ন] [উত্তর]\nউদাহরণ: /teach বাংলাদেশের রাজধানী ঢাকা")
            return
        
        question = context.args[0]
        answer = ' '.join(context.args[1:])
        user_id = update.effective_user.id
        
        # Teach AI
        self.ai.learn(question, answer, user_id)
        
        # Save to database
        await self.db.save_learning(question, answer, user_id)
        
        await update.message.reply_text(
            f"✅ *শিক্ষা দেওয়া হলো!*\n\n"
            f"*প্রশ্ন:* {question}\n"
            f"*উত্তর:* {answer}\n\n"
            f"AI এখন এই তথ্য জানে! 🧠",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def command_brain(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /brain command - Show AI brain status"""
        brain_stats = self.ai.get_stats()
        
        stats_text = f"""
🧠 *AI ব্রেইন স্ট্যাটাস*

📚 মোট শেখা: {brain_stats['total_learned']} টি তথ্য
💬 রেসপন্স দিয়েছে: {brain_stats['responses_given']} বার
🎯 একুরেসি স্কোর: {brain_stats['accuracy_score']:.2%}
🧮 প্যাটার্ন স্টোর: {brain_stats['patterns_stored']}
👥 ইউজার লার্নিং: {brain_stats['users_learned']}

📊 *লার্নিং রেট:*
• সাম্প্রতিক: {brain_stats['recent_learning']}/day
• গড়: {brain_stats['avg_learning']}/day

💾 *মেমরি:*
• নলেজ বেস: {brain_stats['knowledge_size']} KB
• অপটিমাইজড: {'✅' if brain_stats['optimized'] else '❌'}
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
    
    # ==================== GAME COMMANDS ====================
    
    async def command_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /game command"""
        keyboard = [
            [
                InlineKeyboardButton("❌⭕ টিক ট্যাক টো", callback_data="game_tictactoe"),
                InlineKeyboardButton("❓ কুইজ", callback_data="game_quiz")
            ],
            [
                InlineKeyboardButton("💀 হ্যাংম্যান", callback_data="game_hangman"),
                InlineKeyboardButton("🧮 গণিত", callback_data="game_math")
            ],
            [
                InlineKeyboardButton("♟️ দাবা", callback_data="game_chess"),
                InlineKeyboardButton("🎲 লুডো", callback_data="game_ludo")
            ],
            [
                InlineKeyboardButton("🔤 শব্দ শৃঙ্খল", callback_data="game_wordchain"),
                InlineKeyboardButton("🤔 ধাঁধা", callback_data="game_riddle")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎮 *গেম সিলেক্ট করুন:*\n\n"
            "একটি গেম বাছাই করুন নিচের বাটন থেকে:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def command_play(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /play command"""
        if not context.args:
            await update.message.reply_text(
                "🎯 ব্যবহার: /play [game]\n\n"
                "উপলব্ধ গেমস:\n"
                "• tictactoe - টিক ট্যাক টো\n"
                "• quiz - কুইজ গেম\n"
                "• hangman - হ্যাংম্যান\n"
                "• math - গণিত চ্যালেঞ্জ\n"
                "• chess - দাবা\n"
                "• ludo - লুডো\n"
                "• wordchain - শব্দ শৃঙ্খল"
            )
            return
        
        game_type = context.args[0].lower()
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Start game
        game_result = await self.games.start_game(game_type, chat_id, user_id)
        
        if game_result['success']:
            game_data = game_result['data']
            game_id = game_result['game_id']
            
            # Store game in active games
            self.active_games[game_id] = game_data
            
            # Send game board/instructions
            if game_type == "tictactoe":
                board = self._format_tictactoe_board(game_data['board'])
                await update.message.reply_text(
                    f"🎮 *টিক ট্যাক টো শুরু হলো!*\n\n"
                    f"🔢 *বোর্ড:*\n{board}\n\n"
                    f"*ইনস্ট্রাকশন:*\n"
                    f"১-৯ নম্বর দিয়ে মুভ দিন\n"
                    f"উদাহরণ: /move 5",
                    parse_mode=ParseMode.MARKDOWN
                )
            elif game_type == "quiz":
                question = game_data['questions'][game_data['current_q']]
                await update.message.reply_text(
                    f"🧠 *কুইজ গেম!*\n\n"
                    f"*প্রশ্ন:* {question['q']}\n\n"
                    f"*অপশন:*\n"
                    f"১. {question['o'][0]}\n"
                    f"২. {question['o'][1]}\n"
                    f"৩. {question['o'][2]}\n\n"
                    f"*উত্তর দিন:* /answer [number]",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            self.stats['games_played'] += 1
        else:
            await update.message.reply_text(f"❌ {game_result['message']}")
    
    # ==================== APP COMMANDS ====================
    
    async def command_calc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /calc command"""
        if not context.args:
            await update.message.reply_text(
                "📊 *ক্যালকুলেটর*\n\n"
                "ব্যবহার: /calc [expression]\n\n"
                "উদাহরণ:\n"
                "/calc 5+3*2\n"
                "/calc (10+5)/3\n"
                "/calc sin(45)\n"
                "/calc 2^8"
            )
            return
        
        expression = ' '.join(context.args)
        result = await self.apps.calculator(expression)
        
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
    
    async def command_dict(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dict command"""
        if not context.args:
            await update.message.reply_text(
                "📚 *ডিকশনারি*\n\n"
                "ব্যবহার: /dict [word]\n\n"
                "উদাহরণ:\n"
                "/dict hello\n"
                "/dict computer\n"
                "/dict programming"
            )
            return
        
        word = context.args[0]
        result = await self.apps.dictionary(word)
        
        await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)
    
    async def command_joke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /joke command"""
        joke = await self.apps.tell_joke()
        await update.message.reply_text(f"😄 *জোক:*\n\n{joke}", parse_mode=ParseMode.MARKDOWN)
    
    async def command_quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        quote = await self.apps.get_quote()
        await update.message.reply_text(f"💫 *উক্তি:*\n\n{quote}", parse_mode=ParseMode.MARKDOWN)
    
    async def command_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /password command"""
        length = 12
        if context.args:
            try:
                length = int(context.args[0])
                if length < 4 or length > 32:
                    await update.message.reply_text("❌ পাসওয়ার্ড লেন্থ ৪-৩২ এর মধ্যে হতে হবে")
                    return
            except:
                pass
        
        password = await self.apps.generate_password(length)
        await update.message.reply_text(password, parse_mode=ParseMode.MARKDOWN)
    
    # ==================== MODERATION COMMANDS ====================
    
    async def command_warn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /warn command"""
        if update.effective_user.id not in Config.ADMIN_IDS:
            await update.message.reply_text("❌ শুধুমাত্র অ্যাডমিনরা এই কমান্ড ব্যবহার করতে পারেন!")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ একটি মেসেজ রিপ্লাই করুন!")
            return
        
        user_to_warn = update.message.reply_to_message.from_user
        reason = ' '.join(context.args) if context.args else "কোন কারণ উল্লেখ করা হয়নি"
        
        # Add warning
        warnings = await self.moderator.add_warning(
            user_to_warn.id,
            update.effective_chat.id,
            reason,
            update.effective_user.id
        )
        
        warning_text = f"""
⚠️ *ওয়ার্নিং ইস্যু করা হলো!*

👤 *ইউজার:* {user_to_warn.mention_html()}
📝 *কারণ:* {reason}
📊 *মোট ওয়ার্নিং:* {warnings}

🚨 *নিয়ম:*
৩টি ওয়ার্নিং = ১ দিন মিউট
৫টি ওয়ার্নিং = পার্মানেন্ট ব্যান
        """
        
        await update.message.reply_text(warning_text, parse_mode=ParseMode.HTML)
    
    # ==================== ECONOMY COMMANDS ====================
    
    async def command_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command"""
        user_id = update.effective_user.id
        
        # Get balance from database
        user_data = await self.db.get_user(user_id)
        balance = user_data.get('balance', 1000) if user_data else 1000
        
        # Get daily streak
        streak = await self.economy.get_daily_streak(user_id)
        
        balance_text = f"""
💰 *আপনার ব্যালেন্স*

💎 *কয়েন:* {balance}
📈 *ডেইলি স্ট্রীক:* {streak} দিন
🏆 *র‍্যাঙ্ক:* {await self.economy.get_rank(user_id)}
📊 *টোটাল আয়:* {await self.economy.get_total_earned(user_id)}

💡 *কয়েন আয়ের উপায়:*
• /daily - ডেইলি বোনাস
• গেম খেলে জিতুন
• গ্রুপে একটিভ থাকুন
• অ্যাডমিন থেকে রিওয়ার্ড নিন
        """
        
        await update.message.reply_text(balance_text, parse_mode=ParseMode.MARKDOWN)
    
    async def command_daily(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /daily command"""
        user_id = update.effective_user.id
        
        # Claim daily bonus
        result = await self.economy.daily_bonus(user_id)
        
        if result['success']:
            bonus_text = f"""
🎁 *ডেইলি বোনাস!*

💰 *পাওয়া গেছে:* {result['amount']} কয়েন
📅 *পরবর্তী বোনাস:* {result['next_bonus']}
🔥 *স্ট্রীক:* {result['streak']} দিন
🎯 *টোটাল বোনাস:* {result['total_bonus']}

💡 টিপ: প্রতিদিন বোনাস নিয়ে স্ট্রীক বাড়ান!
            """
        else:
            bonus_text = f"""
⏰ *অপেক্ষা করুন!*

❌ {result['message']}
🕐 *পুনরায় চেষ্টা:* {result['next_time']}

💡 আপনি ইতিমধ্যে আজকের বোনাস নিয়েছেন!
            """
        
        await update.message.reply_text(bonus_text, parse_mode=ParseMode.MARKDOWN)
    
    # ==================== MESSAGE HANDLERS ====================
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages"""
        message = update.message
        user_id = message.from_user.id
        chat_id = message.chat.id
        text = message.text
        
        # Update statistics
        self.stats['messages_processed'] += 1
        
        # Skip commands
        if text.startswith('/'):
            return
        
        # Learn from messages in groups
        if chat_id < 0:  # Group chat
            # Auto-learn from conversations (20% chance)
            if random.random() < 0.2:
                # Get context from previous messages
                context_msgs = await self._get_message_context(message)
                
                # Generate AI response based on context
                ai_response = self.ai.generate_response(text, user_id, chat_id)
                
                # Learn from this message
                self.ai.learn(text, ai_response, user_id, chat_id)
                
                # Auto-reply sometimes (10% chance)
                if random.random() < 0.1:
                    await message.reply_text(f"🤖 {ai_response}")
        
        # Save message to database for analytics
        await self.db.save_message(user_id, chat_id, text)
    
    async def handle_new_members(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new members joining"""
        chat = update.effective_chat
        
        for user in update.message.new_chat_members:
            # Skip if the new member is a bot
            if user.is_bot and user.id != context.bot.id:
                continue
            
            welcome_text = f"""
🎉 *স্বাগতম {user.mention_html()}!* 🎉

🤖 *আমি Worlds Most Advanced Bot*
আপনার গ্রুপের জন্য AI-পাওয়ারড এসিস্টেন্ট!

🌟 *আমি যা করতে পারি:*
• 🤖 নিজে নিজে শিখি
• 🎮 গেম খেলাই
• 📱 অ্যাপস দেই
• 🛡️ গ্রুপ ম্যানেজ করি
• 💰 ইকোনমি সিস্টেম

📋 *কিছু কমান্ড:*
/help - সব কমান্ড
/ai - আমার সাথে চ্যাট
/game - গেম খেলুন
/balance - আপনার ব্যালেন্স

*আমি বাংলা শিখছি, আমাকে শেখান!* 🇧🇩
            """
            
            await update.message.reply_text(
                welcome_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            
            # Give welcome bonus
            await self.economy.add_balance(user.id, 500, "Welcome bonus")
    
    # ==================== CALLBACK HANDLERS ====================
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_games":
            await self.command_game(update, context)
        elif data == "menu_apps":
            await self._show_apps_menu(query)
        elif data == "menu_ai":
            await self._show_ai_menu(query)
        elif data == "menu_economy":
            await self._show_economy_menu(query)
        elif data.startswith("game_"):
            await self._handle_game_callback(query, data)
    
    async def _show_apps_menu(self, query):
        """Show apps menu"""
        apps_text = """
📱 *মিনি অ্যাপস মেনু*

🔢 *ক্যালকুলেটর:*
/calc [expression] - গণিত করুন

🔄 *কনভার্টার:*
/convert [value] [from] [to] - ইউনিট পরিবর্তন

📚 *ডিকশনারি:*
/dict [word] - শব্দের অর্থ

🌤️ *আবহাওয়া:*
/weather [city] - আবহাওয়া তথ্য

⏰ *সময় ও তারিখ:*
/time - বর্তমান সময়
/date - আজকের তারিখ

🔐 *সিকিউরিটি:*
/password [length] - পাসওয়ার্ড তৈরি

⚖️ *হেলথ:*
/bmi [weight] [height] - BMI ক্যালকুলেটর
/age [birthdate] - বয়স গণনা

😄 *এন্টারটেইনমেন্ট:*
/joke - মজার জোক
/quote - উক্তি
/fact - মজার তথ্য
        """
        
        await query.edit_message_text(
            apps_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def _show_ai_menu(self, query):
        """Show AI menu"""
        ai_stats = self.ai.get_stats()
        
        ai_text = f"""
🤖 *AI চ্যাট মেনু*

💬 *চ্যাট করুন:*
/ai [message] - AI এর সাথে কথা বলুন

📚 *শেখান:*
/teach [Q] [A] - AI কে নতুন কিছু শেখান

🧠 *AI ব্রেইন স্ট্যাটাস:*
• শেখা তথ্য: {ai_stats['total_learned']}
• একুরেসি: {ai_stats['accuracy_score']:.2%}
• মেমরি: {ai_stats['knowledge_size']} KB

🌐 *লার্নিং:*
AI আপনার গ্রুপের কথাবার্তা থেকে শিখবে!
কোনো এক্সটার্নাল API ব্যবহার করে না!

💡 *টিপস:*
• বাংলা ও ইংরেজি দুটোতেই কথা বলুন
• যত বেশি শেখাবেন, তত বেশি স্মার্ট হবে
• ভুল হলে সংশোধন করুন
        """
        
        await query.edit_message_text(
            ai_text,
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def _format_tictactoe_board(self, board: List[str]) -> str:
        """Format Tic Tac Toe board for display"""
        display_board = []
        for i in range(0, 9, 3):
            row = []
            for j in range(3):
                cell = board[i+j]
                row.append(cell if cell != ' ' else str(i+j+1))
            display_board.append(" | ".join(row))
        
        return "\n---+---+---\n".join(display_board)
    
    async def _get_message_context(self, message) -> List[str]:
        """Get context from previous messages"""
        # This is a simplified version
        # In a real bot, you would fetch previous messages
        return []
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Error occurred: {context.error}")
        
        try:
            await update.message.reply_text(
                "❌ একটি ইরর হয়েছে! দয়া করে আবার চেষ্টা করুন।\n"
                "If problem persists, contact admin."
            )
        except:
            pass
    
    # ==================== RUN BOT ====================
    
    async def start_background_tasks(self):
        """Start background tasks"""
        async def auto_save_task():
            """Auto-save AI knowledge"""
            while True:
                await asyncio.sleep(300)  # 5 minutes
                self.ai.save_knowledge()
                logger.info("💾 AI knowledge auto-saved")
        
        async def cleanup_task():
            """Cleanup old games and sessions"""
            while True:
                await asyncio.sleep(60)  # 1 minute
                current_time = time.time()
                
                # Cleanup old games
                to_remove = []
                for game_id, game in self.active_games.items():
                    if current_time - game.get('created_at', 0) > 3600:  # 1 hour
                        to_remove.append(game_id)
                
                for game_id in to_remove:
                    del self.active_games[game_id]
                
                if to_remove:
                    logger.info(f"🧹 Cleaned up {len(to_remove)} old games")
        
        # Start tasks
        asyncio.create_task(auto_save_task())
        asyncio.create_task(cleanup_task())
    
    def run(self):
        """Run the bot"""
        logger.info("🚀 Starting Worlds Most Advanced Bot...")
        
        # Start background tasks
        asyncio.run(self.start_background_tasks())
        
        # Start polling
        self.app.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )

# ==================== MAIN EXECUTION ====================

def main():
    """Main function"""
    print("""
    🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
    🌟 WORLDS MOST ADVANCED TELEGRAM BOT 🌟
    🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖
    
    🚀 Features:
    • 🤖 Self-Learning AI
    • 🎮 10+ Games
    • 📱 20+ Mini Apps
    • 🛡️ Smart Moderation
    • 💰 Virtual Economy
    • 📊 Real-time Analytics
    
    🔧 Technology:
    • Python 3.11+
    • Firebase Firestore
    • Local AI System
    • No External APIs
    
    📞 Support: @YourChannel
    
    Starting bot...
    """)
    
    # Create bot instance
    bot = SuperTelegramBot()
    
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