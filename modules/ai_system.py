"""
Self-Learning AI System
"""

import pickle
import re
import random
import time
import os
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import numpy as np

class SelfLearningAI:
    """Advanced Self-Learning AI System"""
    
    def __init__(self, data_path="data/ai_knowledge.pkl"):
        self.data_path = data_path
        self.knowledge = self._load_knowledge()
        self.session_memory = defaultdict(list)
        
    def _load_knowledge(self):
        """Load AI knowledge from file"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading AI knowledge: {e}")
        
        # Initialize new knowledge base
        return {
            'patterns': defaultdict(list),
            'responses': defaultdict(list),
            'contexts': defaultdict(dict),
            'user_profiles': defaultdict(dict),
            'group_knowledge': defaultdict(dict),
            'word_weights': defaultdict(float),
            'stats': {
                'total_learned': 0,
                'responses_given': 0,
                'patterns_stored': 0,
                'users_learned': 0,
                'accuracy_score': 0.5,
                'knowledge_size': 0,
                'recent_learning': 0,
                'avg_learning': 0,
                'optimized': False
            }
        }
    
    def save_knowledge(self):
        """Save AI knowledge to file"""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'wb') as f:
                pickle.dump(self.knowledge, f)
            self.knowledge['stats']['knowledge_size'] = os.path.getsize(self.data_path) / 1024
            return True
        except Exception as e:
            print(f"Error saving AI knowledge: {e}")
            return False
    
    def learn(self, input_text: str, response: str, user_id: int = None, group_id: int = None):
        """Learn from input and response"""
        input_text = input_text.lower().strip()
        response = response.strip()
        
        if not input_text or not response:
            return
        
        # Extract features
        words = self._extract_words(input_text)
        phrases = self._extract_phrases(input_text)
        intent = self._detect_intent(input_text)
        
        # Store in knowledge base
        timestamp = time.time()
        
        # Store by words
        for word in words:
            if len(word) > 2:  # Ignore short words
                self.knowledge['patterns'][word].append({
                    'input': input_text,
                    'response': response,
                    'timestamp': timestamp,
                    'weight': 1.0,
                    'user_id': user_id,
                    'group_id': group_id,
                    'intent': intent
                })
        
        # Store by phrases
        for phrase in phrases:
            self.knowledge['patterns'][phrase].append({
                'input': input_text,
                'response': response,
                'timestamp': timestamp,
                'weight': 1.5,  # Phrases have higher weight
                'user_id': user_id,
                'group_id': group_id,
                'intent': intent
            })
        
        # Store in responses
        self.knowledge['responses'][response].append({
            'input': input_text,
            'timestamp': timestamp,
            'user_id': user_id,
            'group_id': group_id
        })
        
        # User-specific learning
        if user_id:
            if user_id not in self.knowledge['user_profiles']:
                self.knowledge['user_profiles'][user_id] = {
                    'patterns': defaultdict(list),
                    'preferences': defaultdict(float),
                    'learning_count': 0,
                    'last_learned': timestamp
                }
                self.knowledge['stats']['users_learned'] += 1
            
            user_data = self.knowledge['user_profiles'][user_id]
            user_data['patterns'][input_text].append({
                'response': response,
                'count': 1,
                'last_used': timestamp
            })
            user_data['learning_count'] += 1
            user_data['last_learned'] = timestamp
        
        # Group-specific learning
        if group_id:
            if group_id not in self.knowledge['group_knowledge']:
                self.knowledge['group_knowledge'][group_id] = defaultdict(list)
            
            self.knowledge['group_knowledge'][group_id][input_text].append({
                'response': response,
                'user_id': user_id,
                'timestamp': timestamp
            })
        
        # Update statistics
        self.knowledge['stats']['total_learned'] += 1
        self.knowledge['stats']['patterns_stored'] = len(self.knowledge['patterns'])
        self.knowledge['stats']['recent_learning'] += 1
        
        # Update word weights
        for word in words:
            self.knowledge['word_weights'][word] = min(
                self.knowledge['word_weights'].get(word, 0) + 0.1, 2.0
            )
        
        # Auto-optimize if needed
        if self.knowledge['stats']['total_learned'] % 100 == 0:
            self._optimize_knowledge()
    
    def generate_response(self, input_text: str, user_id: int = None, group_id: int = None) -> str:
        """Generate response based on learned knowledge"""
        input_text = input_text.lower().strip()
        
        # Check exact matches first
        if input_text in self.knowledge['patterns']:
            responses = self.knowledge['patterns'][input_text]
            if responses:
                latest = max(responses, key=lambda x: x['timestamp'])
                self.knowledge['stats']['responses_given'] += 1
                return latest['response']
        
        # Check user-specific responses
        if user_id and user_id in self.knowledge['user_profiles']:
            user_patterns = self.knowledge['user_profiles'][user_id]['patterns']
            if input_text in user_patterns:
                user_responses = user_patterns[input_text]
                if user_responses:
                    best = max(user_responses, key=lambda x: x['count'])
                    self.knowledge['stats']['responses_given'] += 1
                    return best['response']
        
        # Check group-specific responses
        if group_id and group_id in self.knowledge['group_knowledge']:
            group_patterns = self.knowledge['group_knowledge'][group_id]
            if input_text in group_patterns:
                group_responses = group_patterns[input_text]
                if group_responses:
                    latest = max(group_responses, key=lambda x: x['timestamp'])
                    self.knowledge['stats']['responses_given'] += 1
                    return latest['response']
        
        # Find similar patterns using word matching
        input_words = set(self._extract_words(input_text))
        possible_responses = []
        
        for word in input_words:
            if word in self.knowledge['patterns']:
                for pattern in self.knowledge['patterns'][word]:
                    # Calculate similarity score
                    pattern_words = set(self._extract_words(pattern['input']))
                    similarity = len(input_words.intersection(pattern_words)) / len(input_words.union(pattern_words))
                    
                    if similarity > 0.3:  # Minimum similarity threshold
                        # Calculate weight
                        weight = pattern['weight']
                        weight *= similarity
                        
                        # Adjust for recency
                        recency = (time.time() - pattern['timestamp']) / 86400
                        if recency < 7:  # Recent patterns
                            weight *= 1.5
                        
                        # Adjust for user/group relevance
                        if user_id and pattern['user_id'] == user_id:
                            weight *= 2.0
                        if group_id and pattern['group_id'] == group_id:
                            weight *= 1.5
                        
                        possible_responses.append((pattern['response'], weight))
        
        if possible_responses:
            # Remove duplicates and sum weights
            response_weights = defaultdict(float)
            for response, weight in possible_responses:
                response_weights[response] += weight
            
            # Select response with highest weight
            if response_weights:
                best_response = max(response_weights.items(), key=lambda x: x[1])
                if best_response[1] > 0.5:  # Confidence threshold
                    self.knowledge['stats']['responses_given'] += 1
                    return best_response[0]
        
        # Default responses if nothing matches
        default_responses = [
            "Interesting! Can you tell me more?",
            "I'm still learning. Could you explain that differently?",
            "That's something new! I'll remember that.",
            "হুঁ, বুঝলাম! আরো কিছু বলুন।",
            "আপনি কি বলতে চাচ্ছেন?",
            "এটা তো নতুন শিখলাম! ধন্যবাদ।",
            "আমি এখনো শিখছি, একটু সহজ করে বলুন।",
            "মজার বিষয়! আরো জানতে চাই।"
        ]
        
        self.knowledge['stats']['responses_given'] += 1
        return random.choice(default_responses)
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text"""
        # Bengali and English words
        words = re.findall(r'[\u0980-\u09FF]+|[a-zA-Z]+', text.lower())
        return [w for w in words if len(w) > 1]
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text"""
        words = text.split()
        phrases = []
        
        # Create 2-3 word phrases
        for i in range(len(words) - 1):
            # 2-word phrases
            phrase2 = ' '.join(words[i:i+2])
            if len(phrase2) > 3:
                phrases.append(phrase2)
            
            # 3-word phrases
            if i < len(words) - 2:
                phrase3 = ' '.join(words[i:i+3])
                if len(phrase3) > 5:
                    phrases.append(phrase3)
        
        return phrases
    
    def _detect_intent(self, text: str) -> str:
        """Detect intent from text"""
        text_lower = text.lower()
        
        # Question intent
        question_words = ['what', 'where', 'when', 'why', 'how', 'who', 'which', 'কি', 'কোন', 'কখন', 'কোথায়', 'কেন', 'কীভাবে']
        if any(word in text_lower for word in question_words) or text_lower.endswith('?'):
            return 'question'
        
        # Greeting intent
        greeting_words = ['hello', 'hi', 'hey', 'hola', 'নমস্কার', 'সালাম', 'হ্যালো', 'হাই']
        if any(word in text_lower for word in greeting_words):
            return 'greeting'
        
        # Thanks intent
        thanks_words = ['thanks', 'thank', 'ধন্যবাদ', 'শুকরিয়া']
        if any(word in text_lower for word in thanks_words):
            return 'thanks'
        
        # Farewell intent
        farewell_words = ['bye', 'goodbye', 'বিদায়', 'খোদা হাফেজ']
        if any(word in text_lower for word in farewell_words):
            return 'farewell'
        
        return 'general'
    
    def _optimize_knowledge(self):
        """Optimize knowledge base by removing old/duplicate patterns"""
        current_time = time.time()
        
        for word, patterns in list(self.knowledge['patterns'].items()):
            # Remove patterns older than 30 days
            patterns = [p for p in patterns if current_time - p['timestamp'] < 2592000]
            
            # Keep only top 10 patterns per word
            if len(patterns) > 10:
                patterns.sort(key=lambda x: x['weight'], reverse=True)
                patterns = patterns[:10]
            
            self.knowledge['patterns'][word] = patterns
        
        self.knowledge['stats']['optimized'] = True
    
    def get_stats(self):
        """Get AI statistics"""
        return self.knowledge['stats']
    
    def clear_memory(self):
        """Clear session memory"""
        self.session_memory.clear()
    
    def get_user_profile(self, user_id: int) -> Dict:
        """Get user learning profile"""
        if user_id in self.knowledge['user_profiles']:
            return self.knowledge['user_profiles'][user_id]
        return {}
    
    def get_group_knowledge(self, group_id: int) -> Dict:
        """Get group-specific knowledge"""
        if group_id in self.knowledge['group_knowledge']:
            return self.knowledge['group_knowledge'][group_id]
        return {}