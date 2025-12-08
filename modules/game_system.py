"""
Game System for Telegram Bot
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from enum import Enum

class GameType(Enum):
    TIC_TAC_TOE = "tictactoe"
    QUIZ = "quiz"
    HANGMAN = "hangman"
    MATH = "math"
    CHESS = "chess"
    LUDO = "ludo"
    CARROM = "carrom"
    WORD_CHAIN = "word_chain"
    RIDDLE = "riddle"
    TRIVIA = "trivia"

class GameSystem:
    """Complete Game System"""
    
    def __init__(self):
        self.active_games = {}
        self.game_data = self._load_game_data()
        
    def _load_game_data(self) -> Dict:
        """Load game questions and data"""
        return {
            'quiz_questions': [
                {
                    'question': 'বাংলাদেশের রাজধানী কোথায়?',
                    'options': ['ঢাকা', 'চট্টগ্রাম', 'খুলনা', 'রাজশাহী'],
                    'answer': 0,
                    'category': 'সাধারণ জ্ঞান'
                },
                {
                    'question': 'পৃথিবীর সবচেয়ে বড় মহাদেশ কোনটি?',
                    'options': ['এশিয়া', 'আফ্রিকা', 'ইউরোপ', 'উত্তর আমেরিকা'],
                    'answer': 0,
                    'category': 'ভূগোল'
                },
                {
                    'question': 'পাইথন কোন ধরনের প্রোগ্রামিং ভাষা?',
                    'options': ['ইন্টারপ্রেটেড', 'কম্পাইলড', 'মেশিন', 'অ্যাসেম্বলি'],
                    'answer': 0,
                    'category': 'কম্পিউটার'
                }
            ],
            'hangman_words': [
                'বাংলাদেশ', 'কম্পিউটার', 'প্রোগ্রামিং', 'টেলিগ্রাম',
                'পাইথন', 'ফায়ারবেস', 'ডাটাবেস', 'অ্যালগরিদম'
            ],
            'math_questions': [
                {'type': 'addition', 'range': (1, 100)},
                {'type': 'subtraction', 'range': (1, 100)},
                {'type': 'multiplication', 'range': (1, 20)},
                {'type': 'division', 'range': (1, 50)}
            ],
            'riddles': [
                {
                    'riddle': 'আমাকে খেলে ভাঙে, কাজে লাগলে বাঁধে, কী আমি?',
                    'answer': 'ডিম'
                },
                {
                    'riddle': 'চলে কিন্তু পা নেই, কথা বলে কিন্তু মুখ নেই, কী আমি?',
                    'answer': 'ঘড়ি'
                }
            ]
        }
    
    async def start_game(self, game_type: str, chat_id: int, user_id: int) -> Dict:
        """Start a new game"""
        game_id = f"{chat_id}_{int(time.time())}_{random.randint(1000, 9999)}"
        
        if game_type == GameType.TIC_TAC_TOE.value:
            game_data = await self._create_tictactoe_game(game_id, user_id)
        elif game_type == GameType.QUIZ.value:
            game_data = await self._create_quiz_game(game_id, user_id)
        elif game_type == GameType.HANGMAN.value:
            game_data = await self._create_hangman_game(game_id, user_id)
        elif game_type == GameType.MATH.value:
            game_data = await self._create_math_game(game_id, user_id)
        else:
            return {'success': False, 'message': 'Invalid game type'}
        
        self.active_games[game_id] = game_data
        return {'success': True, 'game_id': game_id, 'data': game_data}
    
    async def _create_tictactoe_game(self, game_id: str, user_id: int) -> Dict:
        """Create Tic Tac Toe game"""
        return {
            'id': game_id,
            'type': 'tictactoe',
            'players': [user_id],
            'board': [' '] * 9,
            'current_player': user_id,
            'symbols': {user_id: 'X'},
            'status': 'waiting',
            'created_at': time.time(),
            'moves': []
        }
    
    async def _create_quiz_game(self, game_id: str, user_id: int) -> Dict:
        """Create Quiz game"""
        questions = random.sample(self.game_data['quiz_questions'], 5)
        
        return {
            'id': game_id,
            'type': 'quiz',
            'player': user_id,
            'questions': questions,
            'current_question': 0,
            'score': 0,
            'start_time': time.time(),
            'answers': []
        }
    
    async def game_move(self, game_id: str, user_id: int, move: str) -> Dict:
        """Make a move in game"""
        if game_id not in self.active_games:
            return {'success': False, 'message': 'Game not found'}
        
        game = self.active_games[game_id]
        
        if game['type'] == 'tictactoe':
            return await self._tictactoe_move(game, user_id, move)
        elif game['type'] == 'quiz':
            return await self._quiz_answer(game, user_id, move)
        elif game['type'] == 'hangman':
            return await self._hangman_guess(game, user_id, move)
        elif game['type'] == 'math':
            return await self._math_answer(game, user_id, move)
        
        return {'success': False, 'message': 'Invalid game type'}
    
    async def _tictactoe_move(self, game: Dict, user_id: int, move: str) -> Dict:
        """Tic Tac Toe move logic"""
        try:
            pos = int(move) - 1
            if pos < 0 or pos > 8:
                return {'success': False, 'message': 'Invalid position (1-9)'}
            
            if game['board'][pos] != ' ':
                return {'success': False, 'message': 'Position already taken'}
            
            symbol = game['symbols'][user_id]
            game['board'][pos] = symbol
            game['moves'].append({'player': user_id, 'position': pos, 'symbol': symbol})
            
            # Check win
            win_patterns = [
                [0,1,2], [3,4,5], [6,7,8],  # Rows
                [0,3,6], [1,4,7], [2,5,8],  # Columns
                [0,4,8], [2,4,6]            # Diagonals
            ]
            
            for pattern in win_patterns:
                if (game['board'][pattern[0]] == game['board'][pattern[1]] == 
                    game['board'][pattern[2]] == symbol):
                    game['status'] = 'finished'
                    game['winner'] = user_id
                    return {
                        'success': True,
                        'message': f'🎉 Player {user_id} wins!',
                        'finished': True,
                        'winner': user_id
                    }
            
            # Check draw
            if ' ' not in game['board']:
                game['status'] = 'finished'
                game['winner'] = None
                return {
                    'success': True,
                    'message': '🤝 It\'s a draw!',
                    'finished': True,
                    'winner': None
                }
            
            # Switch player (for multiplayer)
            return {
                'success': True,
                'message': 'Move successful',
                'finished': False
            }
            
        except ValueError:
            return {'success': False, 'message': 'Invalid move format'}
    
    async def _quiz_answer(self, game: Dict, user_id: int, answer: str) -> Dict:
        """Quiz answer logic"""
        try:
            answer_num = int(answer) - 1
            current_q = game['current_question']
            question = game['questions'][current_q]
            
            if answer_num == question['answer']:
                game['score'] += 10
                correct = True
                message = '✅ Correct!'
            else:
                correct = False
                correct_answer = question['options'][question['answer']]
                message = f'❌ Wrong! Correct answer: {correct_answer}'
            
            game['answers'].append({
                'question': current_q,
                'answer': answer_num,
                'correct': correct
            })
            
            # Move to next question
            game['current_question'] += 1
            
            if game['current_question'] >= len(game['questions']):
                # Game finished
                game['status'] = 'finished'
                return {
                    'success': True,
                    'message': f'{message}\n🎯 Final Score: {game["score"]}/{len(game["questions"])*10}',
                    'finished': True,
                    'score': game['score']
                }
            else:
                # Next question
                next_q = game['questions'][game['current_question']]
                return {
                    'success': True,
                    'message': f'{message}\n\nNext question: {next_q["question"]}',
                    'finished': False,
                    'next_question': next_q
                }
                
        except (ValueError, IndexError):
            return {'success': False, 'message': 'Please enter a valid option number'}
    
    def get_game_state(self, game_id: str) -> Optional[Dict]:
        """Get current game state"""
        return self.active_games.get(game_id)
    
    async def end_game(self, game_id: str):
        """End a game"""
        if game_id in self.active_games:
            del self.active_games[game_id]
            return True
        return False
    
    async def get_active_games(self, user_id: int = None) -> List[Dict]:
        """Get active games"""
        if user_id:
            return [
                game for game in self.active_games.values()
                if user_id in game.get('players', []) or user_id == game.get('player')
            ]
        return list(self.active_games.values())