"""
AI-Powered Multi-Agent Framework for KidSafe Alphabet Tutor
Uses actual language models for intelligent conversation
Author: Nouran Darwish
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import AI libraries
try:
    import openai
    from langchain.llms import OpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate, PromptTemplate
    from langchain.chains import LLMChain
    from langchain.memory import ConversationSummaryBufferMemory
    from langchain.schema import HumanMessage, AIMessage, SystemMessage
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    logger.warning("AI libraries not available. Install with: pip install openai langchain")

# Try Ollama for local models
try:
    from langchain.llms import Ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

@dataclass
class AgentResponse:
    """Response from an agent"""
    agent_name: str
    response: str
    confidence: float = 1.0
    metadata: Dict = None
    extracted_data: Dict = None

class AlphabetTutorAI:
    """
    AI-Powered multi-agent system for KidSafe Alphabet Tutor
    Uses actual language models for intelligent interaction
    """
    
    def __init__(self, session_memory, model_type="ollama", api_key=None):
        """
        Initialize the AI-powered agent system
        
        Args:
            session_memory: SessionMemory instance for state management
            model_type: "openai", "ollama", or "fallback"
            api_key: OpenAI API key if using OpenAI
        """
        self.session_memory = session_memory
        self.model_type = model_type
        self.llm = None
        
        # Load curriculum
        try:
            with open('app/curriculum.json', 'r') as f:
                self.curriculum = json.load(f)
        except:
            self.curriculum = {}
        
        # Initialize LLM
        self._initialize_llm(model_type, api_key)
        
        # System prompts for different agents
        self.system_prompts = {
            "understanding": """You are an AI assistant helping children learn the alphabet. 
            Extract the following from the child's message:
            1. Intent (what they want to do): learn_letter, next_letter, repeat, play_game, ask_question
            2. Any letter mentioned (A-Z)
            3. Child's name if mentioned
            4. Emotional state (excited, confused, frustrated, happy)
            5. Any specific questions
            
            Respond in JSON format with keys: intent, letter, name, emotion, question""",
            
            "lesson": """You are Bubbly, a friendly alphabet tutor for children aged 3-7.
            Create engaging, age-appropriate lessons about letters.
            Use simple language, be encouraging, and make learning fun.
            Include examples children can relate to.""",
            
            "feedback": """You are a supportive tutor providing feedback to children learning letters.
            Always be positive and encouraging. Never criticize.
            Celebrate successes and gently guide when they need help.""",
            
            "safety": """You are a safety filter for children's content.
            Check if the message contains:
            1. Personal information requests
            2. Inappropriate content
            3. Adult topics
            Return 'safe' or 'unsafe' with explanation."""
        }
        
        logger.info(f"AI-Powered Alphabet Tutor initialized with {model_type}")
    
    def _initialize_llm(self, model_type: str, api_key: Optional[str]):
        """Initialize the language model"""
        
        if model_type == "openai" and AI_AVAILABLE:
            if api_key or os.getenv("OPENAI_API_KEY"):
                try:
                    self.llm = ChatOpenAI(
                        temperature=0.7,
                        model_name="gpt-3.5-turbo",
                        openai_api_key=api_key or os.getenv("OPENAI_API_KEY")
                    )
                    logger.info("Using OpenAI GPT-3.5-turbo")
                    return
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI: {e}")
        
        if model_type == "ollama" and OLLAMA_AVAILABLE:
            try:
                # Try to use Ollama with llama2 or mistral
                self.llm = Ollama(
                    model="llama2",  # or "mistral", "phi"
                    temperature=0.7,
                    base_url="http://localhost:11434"
                )
                logger.info("Using Ollama with llama2")
                return
            except Exception as e:
                logger.warning(f"Ollama not available: {e}")
        
        # Fallback to rule-based if no AI available
        logger.info("No AI model available, using enhanced rule-based system")
        self.llm = None
    
    def extract_information(self, user_input: str) -> Dict:
        """
        Use AI to extract information from user input
        """
        if self.llm:
            try:
                prompt = f"""
                Analyze this message from a child learning the alphabet:
                "{user_input}"
                
                Extract:
                1. Intent: (learn_letter/next_letter/repeat/play_game/chat)
                2. Letter mentioned: (A-Z or none)
                3. Child's name: (if mentioned)
                4. Emotion: (happy/confused/excited/neutral)
                5. Question: (any question asked)
                
                Respond in this format:
                Intent: [intent]
                Letter: [letter or none]
                Name: [name or none]
                Emotion: [emotion]
                Question: [question or none]
                """
                
                response = self.llm.predict(prompt)
                
                # Parse the response
                extracted = {}
                for line in response.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        extracted[key.strip().lower()] = value.strip()
                
                return extracted
            except Exception as e:
                logger.error(f"AI extraction failed: {e}")
        
        # Enhanced rule-based fallback
        return self._rule_based_extraction(user_input)
    
    def _rule_based_extraction(self, user_input: str) -> Dict:
        """Enhanced rule-based extraction when AI is not available"""
        input_lower = user_input.lower()
        
        extracted = {
            "intent": "chat",
            "letter": None,
            "name": None,
            "emotion": "neutral",
            "question": None
        }
        
        # Intent detection with more patterns
        intent_patterns = {
            "learn_letter": [
                r"teach.*letter", r"learn.*letter", r"show.*letter",
                r"what.*letter", r"tell.*about.*[a-z]", r"explain.*[a-z]"
            ],
            "next_letter": [
                r"next", r"another", r"different letter", r"move on",
                r"what.*after", r"continue", r"keep going"
            ],
            "repeat": [
                r"again", r"repeat", r"say.*again", r"one more",
                r"didn't hear", r"what did you"
            ],
            "play_game": [
                r"play", r"game", r"fun", r"activity", r"exercise",
                r"practice", r"quiz"
            ]
        }
        
        for intent, patterns in intent_patterns.items():
            if any(re.search(pattern, input_lower) for pattern in patterns):
                extracted["intent"] = intent
                break
        
        # Letter extraction with context
        letter_matches = re.findall(r'\b([a-zA-Z])\b', user_input)
        if letter_matches:
            # Prioritize letters mentioned after keywords
            for match in letter_matches:
                if len(match) == 1:
                    extracted["letter"] = match.upper()
                    break
        
        # Name extraction with more patterns
        name_patterns = [
            r"my name is (\w+)",
            r"i'?m (\w+)",
            r"call me (\w+)",
            r"this is (\w+)",
            r"i am (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, input_lower)
            if match:
                extracted["name"] = match.group(1).capitalize()
                break
        
        # Emotion detection
        emotion_keywords = {
            "happy": ["happy", "good", "great", "awesome", "yay", "love"],
            "confused": ["don't understand", "confused", "what", "help", "don't know"],
            "excited": ["excited", "wow", "amazing", "cool", "yes"],
            "frustrated": ["hard", "difficult", "can't", "wrong", "bad"]
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                extracted["emotion"] = emotion
                break
        
        # Question detection
        if '?' in user_input or any(q in input_lower for q in ['what', 'how', 'why', 'when', 'where', 'who']):
            extracted["question"] = user_input
        
        return extracted
    
    def generate_lesson(self, letter: str, context: Dict) -> str:
        """Generate an AI-powered lesson for a letter"""
        
        if self.llm:
            try:
                letter_info = self.curriculum.get('letters', {}).get(letter, {})
                
                prompt = f"""
                You are Bubbly, a friendly alphabet tutor for young children.
                Create a fun, engaging lesson for the letter {letter}.
                
                Include:
                - How the letter sounds
                - 2-3 example words that start with {letter}
                - A fun fact or memory trick
                - Encouragement
                
                Letter info: {json.dumps(letter_info)}
                Child's emotion: {context.get('emotion', 'neutral')}
                
                Keep it under 3 sentences, use simple language.
                """
                
                return self.llm.predict(prompt)
            except Exception as e:
                logger.error(f"AI lesson generation failed: {e}")
        
        # Fallback to curriculum-based response
        letter_info = self.curriculum.get('letters', {}).get(letter, {})
        response = f"Let's learn {letter}! "
        response += f"{letter} sounds like {letter_info.get('sound_description', 'the letter ' + letter)}. "
        response += f"Like in {', '.join(letter_info.get('example_words', ['Apple'])[:2])}!"
        return response
    
    def generate_feedback(self, context: Dict) -> str:
        """Generate personalized AI feedback"""
        
        if self.llm:
            try:
                prompt = f"""
                You are a supportive tutor. A child learning the letter {context.get('letter', 'A')} 
                just {context.get('action', 'tried to say the letter')}.
                
                Their emotion seems: {context.get('emotion', 'neutral')}
                Performance: {context.get('confidence', 0.7)}
                
                Give encouraging, age-appropriate feedback in 1-2 sentences.
                Always be positive. If they're struggling, offer gentle help.
                """
                
                return self.llm.predict(prompt)
            except:
                pass
        
        # Enhanced fallback feedback
        confidence = context.get('confidence', 0.7)
        letter = context.get('letter', 'A')
        emotion = context.get('emotion', 'neutral')
        
        if confidence > 0.8:
            responses = [
                f"Amazing! You've got {letter} perfectly! 🌟",
                f"Wonderful! {letter} sounds great when you say it!",
                f"Excellent work with {letter}! You're a star!"
            ]
        elif confidence > 0.5:
            responses = [
                f"Good try with {letter}! You're getting closer!",
                f"Nice work! Let's practice {letter} once more together.",
                f"You're doing well with {letter}! Keep going!"
            ]
        else:
            responses = [
                f"Great effort! {letter} can be tricky. Let's try together!",
                f"Good try! Let me help you with {letter}.",
                f"You're working hard on {letter}! Let's practice together."
            ]
        
        import random
        return random.choice(responses)
    
    def process_interaction(self, user_input: str) -> Dict:
        """
        Main method to process interaction with AI enhancement
        """
        try:
            # Extract information from input
            extracted = self.extract_information(user_input)
            
            # Check safety first
            if not self._is_safe(user_input):
                return {
                    'success': True,
                    'response': "Let's keep learning letters! What letter would you like to practice?",
                    'extracted_data': extracted
                }
            
            # Update session state
            if extracted.get('name'):
                self.session_memory.derived_state.child_name = extracted['name']
            
            if extracted.get('letter'):
                self.session_memory.derived_state.current_letter = extracted['letter']
            
            # Generate appropriate response based on intent
            intent = extracted.get('intent', 'chat')
            current_letter = extracted.get('letter') or self.session_memory.derived_state.current_letter
            
            context = {
                'letter': current_letter,
                'emotion': extracted.get('emotion', 'neutral'),
                'confidence': 0.7,
                'user_input': user_input
            }
            
            if intent == 'learn_letter':
                response = self.generate_lesson(current_letter, context)
            elif intent == 'next_letter':
                next_letter = self._get_next_letter(current_letter)
                self.session_memory.derived_state.current_letter = next_letter
                response = f"Great job with {current_letter}! Now let's learn {next_letter}. "
                response += self.generate_lesson(next_letter, context)
            elif intent == 'repeat':
                response = f"Of course! Let me say that again. "
                response += self.generate_lesson(current_letter, context)
            elif intent == 'play_game':
                response = self._generate_game(current_letter)
            else:
                # General conversation with context
                response = self.generate_feedback(context)
            
            # Add to session memory
            self.session_memory.add_turn(user_input, response)
            
            return {
                'success': True,
                'response': response,
                'extracted_data': extracted,
                'state': self.session_memory.get_derived_state_dict()
            }
            
        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            return {
                'success': False,
                'response': "Let's learn letters together! What letter interests you?",
                'error': str(e)
            }
    
    def _is_safe(self, text: str) -> bool:
        """Check content safety using AI or rules"""
        
        if self.llm:
            try:
                prompt = f"""
                Is this message from a child safe and appropriate?
                Message: "{text}"
                
                Check for:
                - Personal information (address, phone, passwords)
                - Inappropriate content
                - Adult topics
                
                Reply with just 'SAFE' or 'UNSAFE'.
                """
                
                result = self.llm.predict(prompt)
                return 'SAFE' in result.upper()
            except:
                pass
        
        # Rule-based safety check
        unsafe_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Phone numbers
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
            r'\b\d{1,5}\s+[\w\s]+(?:street|st|avenue|ave|road|rd|drive|dr)\b',  # Addresses
            'password', 'credit card', 'social security'
        ]
        
        text_lower = text.lower()
        for pattern in unsafe_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False
        
        return True
    
    def _get_next_letter(self, current: str) -> str:
        """Get the next letter in sequence"""
        if current == 'Z':
            return 'A'
        return chr(ord(current) + 1)
    
    def _generate_game(self, letter: str) -> str:
        """Generate a letter-based game"""
        games = [
            f"Let's play 'I Spy'! I spy something that starts with {letter}. Can you guess what it is?",
            f"Can you find 3 things around you that start with {letter}? I'll wait!",
            f"Let's clap the letter {letter}! Clap once for each time you say it: {letter}! {letter}! {letter}!",
            f"Can you make the shape of {letter} with your body? Stand up and try!",
            f"Let's think of animals that start with {letter}. I'll start: {letter} is for {self.curriculum.get('letters', {}).get(letter, {}).get('example_words', ['Ant'])[0]}!"
        ]
        import random
        return random.choice(games)