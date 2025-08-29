"""
CrewAI Multi-Agent Framework for KidSafe Alphabet Tutor
Orchestrates 5 specialized agents for educational interaction
Author: Nouran Darwish
"""

from crewai import Agent, Task, Crew, Process
from typing import Dict, List, Optional, Any
import json
from langchain.tools import Tool
from langchain_community.llms import Ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlphabetTutorCrew:
    """
    Main CrewAI orchestrator for the KidSafe Alphabet Tutor
    Manages 5 specialized agents working together
    """
    
    def __init__(self, session_memory, curriculum_path='app/curriculum.json'):
        """
        Initialize the crew with all agents
        Args:
            session_memory: SessionMemory instance for state management
            curriculum_path: Path to curriculum JSON file
        """
        self.session_memory = session_memory
        self.curriculum = self._load_curriculum(curriculum_path)
        
        # Initialize LLM (Ollama with Llama 3.2 3B)
        try:
            self.llm = Ollama(
                model="llama3.2:3b",
                temperature=0.7,
                base_url="http://localhost:11434"
            )
        except Exception as e:
            logger.warning(f"Ollama initialization failed: {e}. Using fallback mode.")
            self.llm = None
            
        # Initialize all agents
        self.lesson_agent = self._create_lesson_agent()
        self.feedback_agent = self._create_feedback_agent()
        self.personalization_agent = self._create_personalization_agent()
        self.understanding_agent = self._create_understanding_agent()
        self.safety_agent = self._create_safety_agent()
        
        # Create the crew
        self.crew = self._create_crew()
        
    def _load_curriculum(self, path: str) -> Dict:
        """Load curriculum from JSON file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load curriculum: {e}")
            return {}
            
    def _create_lesson_agent(self) -> Agent:
        """
        Create Lesson Agent for curriculum management
        """
        return Agent(
            role='Lesson Coordinator',
            goal='Manage alphabet curriculum progression and select appropriate letters based on child performance',
            backstory="""You are Bubbly's lesson coordinator, an expert in early childhood education 
            specializing in alphabet learning. You understand how children learn letters progressively,
            starting with easier letters and advancing based on their mastery. You know which letters
            are commonly confused and how to sequence lessons for optimal learning.""",
            tools=[
                Tool(
                    name="get_lesson_content",
                    func=self._get_lesson_content,
                    description="Get lesson content for a specific letter"
                ),
                Tool(
                    name="select_next_letter",
                    func=self._select_next_letter,
                    description="Select the next appropriate letter based on progress"
                )
            ],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
    def _create_feedback_agent(self) -> Agent:
        """
        Create Feedback Agent for pronunciation analysis
        """
        return Agent(
            role='Pronunciation Coach',
            goal='Analyze child pronunciation and provide gentle, encouraging corrective guidance',
            backstory="""You are Bubbly's pronunciation coach, trained in phonetics and child speech 
            development. You understand common pronunciation mistakes children make (like confusing B with P,
            or D with T) and know how to provide encouraging feedback that helps them improve without
            discouraging them. You always celebrate attempts and guide gently.""",
            tools=[
                Tool(
                    name="analyze_pronunciation",
                    func=self._analyze_pronunciation,
                    description="Analyze pronunciation confidence and detect confusions"
                ),
                Tool(
                    name="generate_feedback",
                    func=self._generate_feedback,
                    description="Generate encouraging feedback for pronunciation"
                )
            ],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
    def _create_personalization_agent(self) -> Agent:
        """
        Create Personalization Agent for adaptive learning
        """
        return Agent(
            role='Learning Personalizer',
            goal='Maintain child state memory and adapt lessons to individual learning patterns',
            backstory="""You are Bubbly's memory keeper and personalizer. You remember the child's name,
            track their progress, note which letters they find easy or difficult, and help adapt the
            learning experience to their unique needs. You maintain a 3-turn conversation memory to
            provide contextual responses.""",
            tools=[
                Tool(
                    name="update_child_state",
                    func=self._update_child_state,
                    description="Update child's learning state and progress"
                ),
                Tool(
                    name="get_personalized_suggestion",
                    func=self._get_personalized_suggestion,
                    description="Get personalized learning suggestion"
                )
            ],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
    def _create_understanding_agent(self) -> Agent:
        """
        Create Understanding Agent for intent recognition
        """
        return Agent(
            role='Child Intent Interpreter',
            goal='Understand what the child is trying to say or ask, recognizing learning requests and questions',
            backstory="""You are Bubbly's interpreter, skilled at understanding child speech patterns
            and intentions. You can recognize when a child wants to learn a specific letter, needs help,
            wants to play a game, or is asking a question. You understand both explicit requests like
            'Teach me B' and implicit ones like making the /b/ sound.""",
            tools=[
                Tool(
                    name="classify_intent",
                    func=self._classify_intent,
                    description="Classify the child's intent from their speech"
                ),
                Tool(
                    name="extract_entities",
                    func=self._extract_entities,
                    description="Extract entities like letter names from speech"
                )
            ],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
    def _create_safety_agent(self) -> Agent:
        """
        Create Safety Agent for content moderation
        """
        return Agent(
            role='Safety Guardian',
            goal='Ensure all interactions are child-safe, prevent PII collection, and maintain privacy',
            backstory="""You are Bubbly's safety guardian, responsible for keeping all interactions
            appropriate for young children. You detect and prevent any inappropriate content, ensure
            no personal information is collected beyond the child's first name, and maintain strict
            privacy standards. You are COPPA compliant and child-safety focused.""",
            tools=[
                Tool(
                    name="check_content_safety",
                    func=self._check_content_safety,
                    description="Check if content is safe for children"
                ),
                Tool(
                    name="filter_pii",
                    func=self._filter_pii,
                    description="Filter out any personal information"
                )
            ],
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )
        
    def _create_crew(self) -> Crew:
        """
        Create the CrewAI crew with all agents
        """
        return Crew(
            agents=[
                self.understanding_agent,  # First: understand intent
                self.safety_agent,         # Second: ensure safety
                self.personalization_agent, # Third: personalize
                self.lesson_agent,         # Fourth: select content
                self.feedback_agent        # Fifth: provide feedback
            ],
            process=Process.sequential,  # Agents work in sequence
            verbose=True
        )
        
    # Tool implementations for agents
    
    def _get_lesson_content(self, letter: str) -> Dict:
        """Get lesson content for a specific letter"""
        if letter.upper() in self.curriculum.get('letters', {}):
            return self.curriculum['letters'][letter.upper()]
        return {"error": f"Letter {letter} not found in curriculum"}
        
    def _select_next_letter(self, current_progress: Dict) -> str:
        """Select next appropriate letter based on progress"""
        return self.session_memory.suggest_next_letter()
        
    def _analyze_pronunciation(self, audio_confidence: float, letter: str) -> Dict:
        """Analyze pronunciation confidence and common confusions"""
        letter_data = self.curriculum.get('letters', {}).get(letter.upper(), {})
        confusions = letter_data.get('common_confusions', [])
        
        analysis = {
            "confidence": audio_confidence,
            "letter": letter,
            "common_confusions": confusions,
            "needs_practice": audio_confidence < 0.7,
            "suggestion": None
        }
        
        if audio_confidence < 0.5 and confusions:
            analysis["suggestion"] = f"Try emphasizing the '{letter}' sound, not '{confusions[0]}'"
            
        return analysis
        
    def _generate_feedback(self, analysis: Dict) -> str:
        """Generate encouraging feedback based on pronunciation analysis"""
        confidence = analysis.get('confidence', 0)
        letter = analysis.get('letter', '')
        
        if confidence > 0.8:
            return f"Excellent! You said '{letter}' perfectly! ⭐"
        elif confidence > 0.6:
            return f"Good try! The '{letter}' sound is almost there. Let's practice once more!"
        else:
            suggestion = analysis.get('suggestion', '')
            base_feedback = f"Nice effort! Let's work on the '{letter}' sound together."
            if suggestion:
                return f"{base_feedback} {suggestion}"
            return base_feedback
            
    def _update_child_state(self, update_data: Dict) -> Dict:
        """Update child's learning state"""
        # This is handled by SessionMemory
        return {"status": "updated", "state": self.session_memory.get_derived_state_dict()}
        
    def _get_personalized_suggestion(self) -> Dict:
        """Get personalized learning suggestion"""
        state = self.session_memory.get_derived_state_dict()
        next_letter = self.session_memory.suggest_next_letter()
        
        suggestion = {
            "next_letter": next_letter,
            "reason": "",
            "encouragement": ""
        }
        
        if state['streak_count'] >= 3:
            suggestion["reason"] = "You're doing great! Ready for a new challenge?"
            suggestion["encouragement"] = "You're a letter champion! 🌟"
        elif state['last_mistake']:
            suggestion["reason"] = f"Let's practice '{state['last_mistake']}' a bit more"
            suggestion["encouragement"] = "Practice makes perfect! You've got this!"
        else:
            suggestion["reason"] = "Let's continue our alphabet journey!"
            suggestion["encouragement"] = "You're learning so well!"
            
        return suggestion
        
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent from speech"""
        input_lower = user_input.lower()
        
        # Intent patterns
        if any(phrase in input_lower for phrase in ['teach me', 'learn', 'show me', 'what is']):
            return "learn_letter"
        elif any(phrase in input_lower for phrase in ['next', 'another', 'more']):
            return "next_letter"
        elif any(phrase in input_lower for phrase in ['again', 'repeat', 'say that']):
            return "repeat"
        elif any(phrase in input_lower for phrase in ['my name is', "i'm", 'i am']):
            return "introduction"
        elif any(phrase in input_lower for phrase in ['help', 'how', 'what do']):
            return "help"
        elif any(phrase in input_lower for phrase in ['game', 'play', 'fun']):
            return "activity"
        else:
            return "general"
            
    def _extract_entities(self, user_input: str) -> Dict:
        """Extract entities from user input"""
        import re
        
        entities = {
            "letters": [],
            "objects": [],
            "name": None
        }
        
        # Extract single letters
        letter_pattern = r'\b([A-Za-z])\b'
        letters = re.findall(letter_pattern, user_input)
        entities["letters"] = [l.upper() for l in letters]
        
        # Extract name if introducing
        if "my name is" in user_input.lower():
            name = self.session_memory._extract_name(user_input)
            if name:
                entities["name"] = name
                
        return entities
        
    def _check_content_safety(self, content: str) -> bool:
        """Check if content is safe for children"""
        # Basic safety check - in production, use proper content moderation
        unsafe_patterns = ['personal information', 'address', 'phone', 'email', 
                          'password', 'credit card', 'social security']
        
        content_lower = content.lower()
        for pattern in unsafe_patterns:
            if pattern in content_lower:
                return False
        return True
        
    def _filter_pii(self, text: str) -> str:
        """Filter out personal information from text"""
        import re
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Remove potential addresses (basic)
        text = re.sub(r'\d+\s+[A-Za-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)', '[ADDRESS]', text)
        
        return text
        
    def process_interaction(self, user_input: str, audio_confidence: float = None) -> Dict:
        """
        Main method to process a child's interaction
        Returns response and updated state
        """
        try:
            # Create tasks for the crew
            tasks = [
                Task(
                    description=f"Understand the intent of: '{user_input}'",
                    agent=self.understanding_agent,
                    expected_output="Intent classification and extracted entities"
                ),
                Task(
                    description=f"Check safety of interaction: '{user_input}'",
                    agent=self.safety_agent,
                    expected_output="Safety check result"
                ),
                Task(
                    description="Get personalized learning suggestion",
                    agent=self.personalization_agent,
                    expected_output="Personalized suggestion for next steps"
                ),
                Task(
                    description="Select appropriate lesson content",
                    agent=self.lesson_agent,
                    expected_output="Selected lesson content"
                ),
                Task(
                    description=f"Provide feedback with confidence {audio_confidence}",
                    agent=self.feedback_agent,
                    expected_output="Encouraging feedback message"
                )
            ]
            
            # Execute crew tasks
            result = self.crew.kickoff(inputs={"user_input": user_input})
            
            return {
                "success": True,
                "response": result,
                "state": self.session_memory.get_derived_state_dict()
            }
            
        except Exception as e:
            logger.error(f"Crew processing error: {e}")
            # Fallback to rule-based response
            return self._fallback_response(user_input, audio_confidence)
            
    def _fallback_response(self, user_input: str, audio_confidence: float = None) -> Dict:
        """
        Fallback rule-based response when LLM is unavailable
        """
        intent = self._classify_intent(user_input)
        current_letter = self.session_memory.derived_state.current_letter
        
        responses = {
            "learn_letter": f"Let's learn the letter {current_letter}! Can you say '{current_letter}' with me?",
            "next_letter": f"Great job! Let's try the letter {self.session_memory.suggest_next_letter()}!",
            "repeat": f"Sure! The letter {current_letter} sounds like this: '{current_letter}'",
            "introduction": "Hello! I'm Bubbly, your alphabet friend! What letter would you like to learn?",
            "help": "I can teach you letters! Just say 'Teach me A' or any letter you want to learn!",
            "activity": f"Let's play a game! Can you find something that starts with '{current_letter}'?",
            "general": f"That's interesting! Would you like to practice the letter {current_letter}?"
        }
        
        return {
            "success": True,
            "response": responses.get(intent, "Let's learn letters together!"),
            "state": self.session_memory.get_derived_state_dict()
        }