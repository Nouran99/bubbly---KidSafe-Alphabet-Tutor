"""
Simplified CrewAI Multi-Agent Framework for KidSafe Alphabet Tutor
Using rule-based fallbacks without LLM dependency
Author: Nouran Darwish
"""

from typing import Dict, List, Optional, Any
import json
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Response from an agent"""
    agent_name: str
    response: str
    confidence: float = 1.0
    metadata: Dict = None

class AlphabetTutorAgents:
    """
    Simplified multi-agent system for KidSafe Alphabet Tutor
    Rule-based implementation that mimics CrewAI behavior
    """
    
    def __init__(self, session_memory, curriculum_path='app/curriculum.json'):
        """
        Initialize the agent system
        Args:
            session_memory: SessionMemory instance for state management
            curriculum_path: Path to curriculum JSON file
        """
        self.session_memory = session_memory
        self.curriculum = self._load_curriculum(curriculum_path)
        logger.info("Alphabet Tutor Agents initialized (rule-based mode)")
        
    def _load_curriculum(self, path: str) -> Dict:
        """Load curriculum from JSON file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load curriculum: {e}")
            return {}
    
    # Lesson Agent Functions
    def lesson_agent_process(self, context: Dict) -> AgentResponse:
        """
        Lesson Agent: Manages curriculum progression
        """
        current_letter = context.get('current_letter', 'A')
        intent = context.get('intent', 'general')
        
        if intent == 'learn_letter':
            letter_info = self.curriculum.get('letters', {}).get(current_letter, {})
            response = f"Let's learn the letter {current_letter}! "
            response += f"It sounds like {letter_info.get('sound_description', current_letter)}. "
            response += f"Like in {letter_info.get('example_words', [''])[0]}!"
            
            return AgentResponse(
                agent_name="Lesson Agent",
                response=response,
                metadata={'letter': current_letter, 'lesson': letter_info}
            )
        
        elif intent == 'next_letter':
            next_letter = self.session_memory.suggest_next_letter()
            return AgentResponse(
                agent_name="Lesson Agent",
                response=f"Great job! Let's move on to the letter {next_letter}!",
                metadata={'next_letter': next_letter}
            )
        
        return AgentResponse(
            agent_name="Lesson Agent",
            response=f"We're working on the letter {current_letter}. Keep practicing!"
        )
    
    # Feedback Agent Functions
    def feedback_agent_process(self, context: Dict) -> AgentResponse:
        """
        Feedback Agent: Provides pronunciation feedback
        """
        confidence = context.get('confidence', 0.5)
        letter = context.get('current_letter', 'A')
        
        if confidence > 0.8:
            response = f"Excellent! You said '{letter}' perfectly! ⭐"
            self.session_memory.derived_state.streak_count += 1
        elif confidence > 0.6:
            response = f"Good try! The '{letter}' sound is almost there. Let's practice once more!"
        else:
            response = f"Nice effort! Let's work on the '{letter}' sound together."
            
            # Check for common confusions
            letter_info = self.curriculum.get('letters', {}).get(letter, {})
            confusions = letter_info.get('common_confusions', [])
            if confusions:
                response += f" Remember, '{letter}' is different from '{confusions[0]}'."
        
        return AgentResponse(
            agent_name="Feedback Agent",
            response=response,
            confidence=confidence,
            metadata={'letter': letter, 'score': confidence}
        )
    
    # Personalization Agent Functions
    def personalization_agent_process(self, context: Dict) -> AgentResponse:
        """
        Personalization Agent: Manages adaptive learning
        """
        state = self.session_memory.get_derived_state_dict()
        child_name = state.get('child_name', 'friend')
        streak = state.get('streak_count', 0)
        
        # Personalized encouragement based on progress
        if streak >= 5:
            response = f"Amazing work, {child_name}! You're a letter champion! 🌟"
        elif streak >= 3:
            response = f"Great job, {child_name}! You're doing wonderfully!"
        else:
            response = f"Keep going, {child_name}! You're learning so well!"
        
        # Suggest next activity based on performance
        if state.get('last_mistake'):
            response += f" Let's practice '{state['last_mistake']}' one more time."
        else:
            next_letter = self.session_memory.suggest_next_letter()
            response += f" Ready for the letter {next_letter}?"
        
        return AgentResponse(
            agent_name="Personalization Agent",
            response=response,
            metadata={'personalization': state}
        )
    
    # Understanding Agent Functions
    def understanding_agent_process(self, user_input: str) -> AgentResponse:
        """
        Understanding Agent: Interprets user intent
        """
        input_lower = user_input.lower()
        
        # Classify intent
        intent = self._classify_intent(input_lower)
        
        # Extract entities
        entities = self._extract_entities(user_input)
        
        # Update session if name detected
        if entities.get('name'):
            self.session_memory.derived_state.child_name = entities['name']
        
        # Update current letter if detected
        if entities.get('letters'):
            self.session_memory.derived_state.current_letter = entities['letters'][0]
        
        response_map = {
            'introduction': f"Hello! I'm Bubbly, your alphabet friend!",
            'learn_letter': f"Let's learn that letter together!",
            'next_letter': f"Moving on to the next letter!",
            'repeat': f"Sure, let's try that again!",
            'help': f"I'm here to help you learn the alphabet!",
            'activity': f"Let's play a fun letter game!",
            'general': f"That's interesting! Let's keep learning letters!"
        }
        
        return AgentResponse(
            agent_name="Understanding Agent",
            response=response_map.get(intent, "Let's learn letters!"),
            metadata={'intent': intent, 'entities': entities}
        )
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent from speech"""
        if any(phrase in user_input for phrase in ['teach me', 'learn', 'show me', 'what is']):
            return 'learn_letter'
        elif any(phrase in user_input for phrase in ['next', 'another', 'more']):
            return 'next_letter'
        elif any(phrase in user_input for phrase in ['again', 'repeat', 'say that']):
            return 'repeat'
        elif any(phrase in user_input for phrase in ['my name is', "i'm", 'i am']):
            return 'introduction'
        elif any(phrase in user_input for phrase in ['help', 'how', 'what do']):
            return 'help'
        elif any(phrase in user_input for phrase in ['game', 'play', 'fun']):
            return 'activity'
        else:
            return 'general'
    
    def _extract_entities(self, user_input: str) -> Dict:
        """Extract entities from user input"""
        import re
        
        entities = {
            "letters": [],
            "name": None
        }
        
        # Extract single letters
        letter_pattern = r'\b([A-Za-z])\b'
        letters = re.findall(letter_pattern, user_input)
        entities["letters"] = [l.upper() for l in letters]
        
        # Extract name if introducing
        markers = ["my name is", "i am", "i'm", "call me"]
        input_lower = user_input.lower()
        
        for marker in markers:
            if marker in input_lower:
                idx = input_lower.index(marker) + len(marker)
                remaining = user_input[idx:].strip()
                if remaining:
                    name = remaining.split()[0] if remaining else None
                    if name:
                        entities["name"] = name.strip(".,!?").capitalize()
                        break
        
        return entities
    
    # Safety Agent Functions
    def safety_agent_process(self, content: str) -> AgentResponse:
        """
        Safety Agent: Ensures child-safe content
        """
        # Check for inappropriate content
        unsafe_keywords = [
            'personal information', 'address', 'phone', 'email',
            'password', 'credit card', 'social security',
            'school name', 'parent name', 'where do you live'
        ]
        
        content_lower = content.lower()
        is_safe = not any(keyword in content_lower for keyword in unsafe_keywords)
        
        if not is_safe:
            return AgentResponse(
                agent_name="Safety Agent",
                response="Let's keep learning letters! I can't talk about that.",
                confidence=0.0,
                metadata={'safe': False, 'blocked': True}
            )
        
        return AgentResponse(
            agent_name="Safety Agent",
            response="",  # No response needed if safe
            confidence=1.0,
            metadata={'safe': True, 'blocked': False}
        )
    
    # Main orchestration method
    def process_interaction(self, user_input: str, audio_confidence: float = None) -> Dict:
        """
        Main method to process a child's interaction
        Orchestrates all agents in sequence
        """
        try:
            # Step 1: Understanding Agent - Interpret intent
            understanding_result = self.understanding_agent_process(user_input)
            intent = understanding_result.metadata.get('intent', 'general')
            entities = understanding_result.metadata.get('entities', {})
            
            # Step 2: Safety Agent - Check content safety
            safety_result = self.safety_agent_process(user_input)
            if safety_result.metadata.get('blocked'):
                return {
                    'success': True,
                    'response': safety_result.response,
                    'state': self.session_memory.get_derived_state_dict()
                }
            
            # Prepare context for other agents
            context = {
                'user_input': user_input,
                'intent': intent,
                'entities': entities,
                'confidence': audio_confidence or 0.7,
                'current_letter': self.session_memory.derived_state.current_letter
            }
            
            # Step 3: Personalization Agent - Get personalized response
            personalization_result = self.personalization_agent_process(context)
            
            # Step 4: Lesson Agent - Get lesson content
            lesson_result = self.lesson_agent_process(context)
            
            # Step 5: Feedback Agent - Provide feedback if audio confidence available
            feedback_result = None
            if audio_confidence is not None:
                feedback_result = self.feedback_agent_process(context)
            
            # Combine responses
            responses = []
            
            if intent in ['learn_letter', 'next_letter']:
                responses.append(lesson_result.response)
            
            if feedback_result and audio_confidence is not None:
                responses.append(feedback_result.response)
            elif intent == 'introduction':
                responses.append(understanding_result.response)
                responses.append(personalization_result.response)
            else:
                responses.append(personalization_result.response)
            
            final_response = " ".join(responses)
            
            return {
                'success': True,
                'response': final_response,
                'state': self.session_memory.get_derived_state_dict(),
                'metadata': {
                    'intent': intent,
                    'entities': entities,
                    'agents_used': ['Understanding', 'Safety', 'Personalization', 'Lesson', 'Feedback']
                }
            }
            
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            return {
                'success': False,
                'response': "Let's learn letters together!",
                'state': self.session_memory.get_derived_state_dict()
            }