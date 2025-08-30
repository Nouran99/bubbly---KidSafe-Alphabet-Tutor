"""
Session State Management for KidSafe Alphabet Tutor
Implements zero-retention, session-only memory with 3-turn buffer
Author: Nouran Darwish
"""

from collections import deque
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from enum import Enum

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class AgeRange(Enum):
    YOUNGER = "3-5"
    OLDER = "6-8"

@dataclass
class ConversationTurn:
    """Single conversation turn between child and tutor"""
    timestamp: str
    user_input: str
    assistant_response: str
    detected_intent: Optional[str] = None
    confidence_score: Optional[float] = None
    
@dataclass
class DerivedState:
    """Child's derived state from conversation analysis"""
    child_name: Optional[str] = None
    current_letter: str = "A"
    difficulty_level: DifficultyLevel = DifficultyLevel.EASY
    last_mistake: Optional[str] = None
    streak_count: int = 0
    age_range: AgeRange = AgeRange.YOUNGER
    letters_completed: List[str] = None
    letters_struggled: List[str] = None
    
    def __post_init__(self):
        if self.letters_completed is None:
            self.letters_completed = []
        if self.letters_struggled is None:
            self.letters_struggled = []

class SessionMemory:
    """
    Manages session-only memory with zero data retention
    Implements 3-turn rolling conversation buffer
    """
    
    def __init__(self, max_turns: int = 3):
        """
        Initialize session memory
        Args:
            max_turns: Maximum conversation turns to keep (default: 3)
        """
        self.conversation_buffer = deque(maxlen=max_turns * 2)  # User + Assistant pairs
        self.derived_state = DerivedState()
        self.session_start = datetime.now()
        self.total_interactions = 0
        self.current_activity = None
        self.vision_enabled = False
        self.tts_enabled = True
        self.asr_enabled = True
        
    def add_turn(self, user_input: str, assistant_response: str, 
                 intent: Optional[str] = None, confidence: Optional[float] = None):
        """
        Add a conversation turn to the buffer
        """
        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(),
            user_input=user_input,
            assistant_response=assistant_response,
            detected_intent=intent,
            confidence_score=confidence
        )
        
        # Add to buffer (maintains max size automatically)
        self.conversation_buffer.append(("user", user_input))
        self.conversation_buffer.append(("assistant", assistant_response))
        
        self.total_interactions += 1
        
        # Update derived state based on conversation
        self._update_derived_state(user_input, assistant_response, intent, confidence)
        
    def _update_derived_state(self, user_input: str, assistant_response: str, 
                              intent: Optional[str], confidence: Optional[float]):
        """
        Analyze conversation and update derived state
        """
        # Extract child's name if mentioned
        if not self.derived_state.child_name:
            name = self._extract_name(user_input)
            if name:
                self.derived_state.child_name = name
        
        # Update current letter based on conversation
        letter = self._extract_current_letter(user_input, assistant_response)
        if letter:
            self.derived_state.current_letter = letter
            
        # Track mistakes and successes
        if confidence:
            if confidence < 0.6:
                self.derived_state.last_mistake = self.derived_state.current_letter
                self.derived_state.streak_count = 0
                if self.derived_state.current_letter not in self.derived_state.letters_struggled:
                    self.derived_state.letters_struggled.append(self.derived_state.current_letter)
            elif confidence > 0.8:
                self.derived_state.streak_count += 1
                if self.derived_state.current_letter not in self.derived_state.letters_completed:
                    self.derived_state.letters_completed.append(self.derived_state.current_letter)
                    
        # Adjust difficulty based on performance
        self._adjust_difficulty()
        
    def _extract_name(self, user_input: str) -> Optional[str]:
        """Extract child's name from input"""
        markers = ["my name is", "i am", "i'm", "call me"]
        input_lower = user_input.lower()
        
        for marker in markers:
            if marker in input_lower:
                idx = input_lower.index(marker) + len(marker)
                remaining = user_input[idx:].strip()
                # Extract first word as name
                name = remaining.split()[0] if remaining else None
                if name:
                    # Clean up name
                    name = name.strip(".,!?")
                    return name.capitalize()
        return None
        
    def _extract_current_letter(self, user_input: str, assistant_response: str) -> Optional[str]:
        """Extract current letter being practiced"""
        # Check for explicit letter mentions
        import re
        
        # Pattern for single letter mentions
        letter_pattern = r'\b([A-Z])\b'
        
        # Check user input
        user_matches = re.findall(letter_pattern, user_input.upper())
        if user_matches and len(user_matches[0]) == 1:
            return user_matches[0]
            
        # Check assistant response
        asst_matches = re.findall(letter_pattern, assistant_response.upper())
        if asst_matches and len(asst_matches[0]) == 1:
            return asst_matches[0]
            
        return None
        
    def _adjust_difficulty(self):
        """Adjust difficulty based on performance"""
        if self.derived_state.streak_count >= 5:
            if self.derived_state.difficulty_level == DifficultyLevel.EASY:
                self.derived_state.difficulty_level = DifficultyLevel.MEDIUM
            elif self.derived_state.difficulty_level == DifficultyLevel.MEDIUM:
                self.derived_state.difficulty_level = DifficultyLevel.HARD
                
        elif len(self.derived_state.letters_struggled) >= 3:
            if self.derived_state.difficulty_level == DifficultyLevel.HARD:
                self.derived_state.difficulty_level = DifficultyLevel.MEDIUM
            elif self.derived_state.difficulty_level == DifficultyLevel.MEDIUM:
                self.derived_state.difficulty_level = DifficultyLevel.EASY
                
    def get_conversation_history(self) -> List[Tuple[str, str]]:
        """Get the conversation history as list of tuples"""
        return list(self.conversation_buffer)
        
    def get_derived_state_dict(self) -> Dict:
        """Get derived state as dictionary"""
        state_dict = {
            "child_name": self.derived_state.child_name,
            "current_letter": self.derived_state.current_letter,
            "difficulty_level": self.derived_state.difficulty_level.value,
            "last_mistake": self.derived_state.last_mistake,
            "streak_count": self.derived_state.streak_count,
            "age_range": self.derived_state.age_range.value,
            "letters_completed": self.derived_state.letters_completed,
            "letters_struggled": self.derived_state.letters_struggled,
            "total_interactions": self.total_interactions,
            "session_duration": str(datetime.now() - self.session_start)
        }
        return state_dict
        
    def get_formatted_memory(self) -> str:
        """Get formatted memory for display"""
        history = self.get_conversation_history()
        state = self.get_derived_state_dict()
        
        # Format conversation pairs
        formatted_pairs = []
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                user_msg = history[i][1]
                asst_msg = history[i + 1][1]
                formatted_pairs.append(f"Child: {user_msg}\nBubbly: {asst_msg}")
                
        memory_text = "=== Recent Conversation ===\n"
        memory_text += "\n---\n".join(formatted_pairs[-3:])  # Last 3 exchanges
        
        memory_text += "\n\n=== Derived State ===\n"
        memory_text += f"Name: {state['child_name'] or 'Unknown'}\n"
        memory_text += f"Current Letter: {state['current_letter']}\n"
        memory_text += f"Difficulty: {state['difficulty_level']}\n"
        memory_text += f"Streak: {state['streak_count']} correct\n"
        memory_text += f"Age Range: {state['age_range']}\n"
        
        if state['letters_completed']:
            memory_text += f"Mastered: {', '.join(state['letters_completed'][:5])}\n"
        if state['letters_struggled']:
            memory_text += f"Needs Practice: {', '.join(state['letters_struggled'][:3])}\n"
            
        return memory_text
        
    def suggest_next_letter(self) -> str:
        """Suggest next letter based on current progress"""
        # Simple progression through alphabet
        try:
            # Define letter pools by difficulty
            easy_letters = ['A', 'E', 'I', 'O', 'U']  # Vowels
            medium_letters = ['B', 'C', 'D', 'F', 'G', 'H', 'L', 'M', 'N', 'P', 'R', 'S', 'T']
            hard_letters = ['J', 'K', 'Q', 'V', 'W', 'X', 'Y', 'Z']
            
            # Get appropriate difficulty letters
            if self.derived_state.difficulty_level == DifficultyLevel.EASY:
                letter_pool = easy_letters
            elif self.derived_state.difficulty_level == DifficultyLevel.MEDIUM:
                letter_pool = medium_letters
            else:
                letter_pool = hard_letters
                
            # Filter out completed letters
            available = [l for l in letter_pool 
                        if l not in self.derived_state.letters_completed]
            
            # Prioritize letters that need practice
            if self.derived_state.letters_struggled:
                for letter in self.derived_state.letters_struggled:
                    if letter in available:
                        return letter
                        
            # Return next available letter
            if available:
                return available[0]
            else:
                # All letters in difficulty completed, move to next level
                if self.derived_state.difficulty_level == DifficultyLevel.EASY:
                    return progression['medium_letters'][0]
                elif self.derived_state.difficulty_level == DifficultyLevel.MEDIUM:
                    return progression['hard_letters'][0]
                else:
                    return "A"  # Start over
                    
        except Exception as e:
            print(f"Error suggesting next letter: {e}")
            return "A"
            
    def reset(self):
        """Reset session memory (for new session)"""
        self.conversation_buffer.clear()
        self.derived_state = DerivedState()
        self.session_start = datetime.now()
        self.total_interactions = 0
        self.current_activity = None
        
    def update_settings(self, age_range: str = None, vision: bool = None, 
                       tts: bool = None, asr: bool = None):
        """Update session settings"""
        if age_range:
            self.derived_state.age_range = AgeRange(age_range)
        if vision is not None:
            self.vision_enabled = vision
        if tts is not None:
            self.tts_enabled = tts
        if asr is not None:
            self.asr_enabled = asr