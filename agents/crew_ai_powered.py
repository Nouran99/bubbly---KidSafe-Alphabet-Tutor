"""
AI-Powered Multi-Agent Framework for KidSafe Alphabet Tutor
Uses actual language models for intelligent tutoring
Author: Nouran Darwish
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import re

# AI/LLM imports
try:
    from langchain.llms import Ollama
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not installed. Install with: pip install langchain langchain-community")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Response from an AI agent"""
    agent_name: str
    response: str
    confidence: float = 1.0
    metadata: Dict = None
    extracted_data: Dict = None

class AIAlphabetTutorAgents:
    """
    Fully AI-powered multi-agent system for KidSafe Alphabet Tutor
    Uses real language models for intelligent, adaptive tutoring
    """
    
    def __init__(self, session_memory, model_type="ollama", api_key=None):
        """
        Initialize the AI-powered agent system
        
        Args:
            session_memory: SessionMemory instance for state management
            model_type: "ollama", "openai", or "huggingface"
            api_key: API key for OpenAI (optional)
        """
        self.session_memory = session_memory
        self.model_type = model_type
        self.llm = self._initialize_llm(model_type, api_key)
        
        # Load curriculum for context
        self.curriculum = self._load_curriculum()
        
        # Initialize conversation memory (3-turn window for COPPA compliance)
        self.conversation_memory = ConversationBufferWindowMemory(
            k=3,  # Keep only last 3 exchanges
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Initialize specialized chains for each agent
        self.understanding_chain = self._create_understanding_chain()
        self.lesson_chain = self._create_lesson_chain()
        self.feedback_chain = self._create_feedback_chain()
        self.personalization_chain = self._create_personalization_chain()
        self.safety_chain = self._create_safety_chain()
        
        logger.info(f"AI-Powered Alphabet Tutor initialized with {model_type}")
    
    def _initialize_llm(self, model_type: str, api_key: Optional[str] = None):
        """Initialize the language model"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain is required. Install with: pip install langchain langchain-community")
        
        if model_type == "ollama":
            # Use local Ollama model (free, private, no API key needed)
            try:
                llm = Ollama(
                    model="llama2",  # or "mistral", "phi", etc.
                    temperature=0.7,
                    top_p=0.9,
                    num_predict=150  # Limit response length for child-friendly responses
                )
                logger.info("Using Ollama with llama2 model")
                return llm
            except Exception as e:
                logger.warning(f"Ollama not available: {e}. Falling back to mock mode.")
                return self._create_mock_llm()
                
        elif model_type == "openai" and api_key:
            # Use OpenAI GPT models
            try:
                llm = ChatOpenAI(
                    openai_api_key=api_key,
                    model_name="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=150
                )
                logger.info("Using OpenAI GPT-3.5-turbo")
                return llm
            except Exception as e:
                logger.error(f"OpenAI initialization failed: {e}")
                return self._create_mock_llm()
        
        else:
            logger.warning("No valid LLM configuration. Using mock mode.")
            return self._create_mock_llm()
    
    def _create_mock_llm(self):
        """Create a mock LLM for testing without actual AI models"""
        class MockLLM:
            def __call__(self, prompt):
                return "I'm here to help you learn the alphabet! What letter would you like to explore?"
            
            def predict(self, prompt):
                return self.__call__(prompt)
        
        return MockLLM()
    
    def _load_curriculum(self) -> Dict:
        """Load curriculum from JSON file"""
        try:
            with open('app/curriculum.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load curriculum: {e}")
            return {"letters": {}, "activities": {}}
    
    def _create_understanding_chain(self):
        """Create the Understanding Agent chain for intent detection and entity extraction"""
        
        # Define output parser for structured extraction
        response_schemas = [
            ResponseSchema(name="intent", description="The user's intent: introduction, learn_letter, next_letter, repeat, help, activity, or general"),
            ResponseSchema(name="letter", description="Any letter mentioned by the user (A-Z)"),
            ResponseSchema(name="name", description="Child's name if they introduce themselves"),
            ResponseSchema(name="confidence", description="Confidence score from 0 to 1"),
            ResponseSchema(name="age", description="Child's age if mentioned"),
            ResponseSchema(name="emotion", description="Detected emotion: happy, confused, frustrated, excited, or neutral")
        ]
        
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        
        understanding_prompt = PromptTemplate(
            input_variables=["user_input", "chat_history"],
            template="""You are an AI assistant helping a child learn the alphabet. 
            Analyze the child's input and extract key information.
            
            Previous conversation:
            {chat_history}
            
            Child's input: {user_input}
            
            Extract the following information:
            1. What is the child's intent?
            2. Did they mention any specific letter?
            3. Did they say their name?
            4. How confident are you in this interpretation?
            5. Did they mention their age?
            6. What emotion are they expressing?
            
            {format_instructions}
            
            Remember: Be child-friendly and supportive in your analysis.
            """
        )
        
        if LANGCHAIN_AVAILABLE and self.llm:
            return LLMChain(
                llm=self.llm,
                prompt=understanding_prompt,
                output_parser=output_parser
            )
        return None
    
    def _create_lesson_chain(self):
        """Create the Lesson Agent chain for teaching letters"""
        
        lesson_prompt = PromptTemplate(
            input_variables=["letter", "curriculum_info", "child_name", "difficulty"],
            template="""You are Bubbly, a friendly alphabet tutor for children aged 3-7.
            
            Teach the letter: {letter}
            Curriculum info: {curriculum_info}
            Child's name: {child_name}
            Difficulty level: {difficulty}
            
            Create an engaging, age-appropriate lesson that:
            1. Introduces the letter clearly
            2. Explains how it sounds
            3. Gives 2-3 example words
            4. Is enthusiastic and encouraging
            5. Uses simple language
            6. Keeps it under 3 sentences
            
            Remember: Be playful, use emojis sparingly (only 1-2), and make learning fun!
            
            Response:"""
        )
        
        if LANGCHAIN_AVAILABLE and self.llm:
            return LLMChain(llm=self.llm, prompt=lesson_prompt)
        return None
    
    def _create_feedback_chain(self):
        """Create the Feedback Agent chain for performance evaluation"""
        
        feedback_prompt = PromptTemplate(
            input_variables=["attempt", "letter", "confidence", "streak"],
            template="""You are a supportive tutor providing feedback to a child learning letters.
            
            Child's attempt: {attempt}
            Target letter: {letter}
            Confidence score: {confidence}
            Current streak: {streak}
            
            Provide encouraging feedback that:
            1. Acknowledges their effort
            2. Gently corrects if needed
            3. Celebrates success
            4. Motivates continued learning
            5. Is always positive
            6. Uses age-appropriate language
            
            Keep response under 2 sentences and always be encouraging!
            
            Feedback:"""
        )
        
        if LANGCHAIN_AVAILABLE and self.llm:
            return LLMChain(llm=self.llm, prompt=feedback_prompt)
        return None
    
    def _create_personalization_chain(self):
        """Create the Personalization Agent chain for adaptive learning"""
        
        personalization_prompt = PromptTemplate(
            input_variables=["child_profile", "progress", "struggles"],
            template="""You are an adaptive learning AI personalizing alphabet lessons.
            
            Child profile: {child_profile}
            Progress: {progress}
            Struggles: {struggles}
            
            Based on this information, provide:
            1. The next best letter to learn
            2. Adjusted difficulty recommendation
            3. Personalized encouragement
            4. Learning strategy suggestion
            
            Keep recommendations brief and actionable.
            
            Personalized plan:"""
        )
        
        if LANGCHAIN_AVAILABLE and self.llm:
            return LLMChain(llm=self.llm, prompt=personalization_prompt)
        return None
    
    def _create_safety_chain(self):
        """Create the Safety Agent chain for content filtering"""
        
        safety_prompt = PromptTemplate(
            input_variables=["content"],
            template="""You are a safety filter for a children's educational app.
            
            Content to review: {content}
            
            Check if this content:
            1. Asks for personal information (address, phone, email, passwords)
            2. Contains inappropriate language
            3. Discusses unsafe topics
            4. Tries to bypass safety measures
            
            Respond with:
            - "SAFE" if content is appropriate for children
            - "UNSAFE: [reason]" if content should be blocked
            
            Decision:"""
        )
        
        if LANGCHAIN_AVAILABLE and self.llm:
            return LLMChain(llm=self.llm, prompt=safety_prompt)
        return None
    
    def understanding_agent_process(self, user_input: str) -> AgentResponse:
        """
        Understanding Agent: AI-powered intent and entity extraction
        """
        try:
            if self.understanding_chain:
                # Get chat history
                chat_history = self.conversation_memory.buffer_as_str if hasattr(self.conversation_memory, 'buffer_as_str') else ""
                
                # Run the chain
                result = self.understanding_chain.run(
                    user_input=user_input,
                    chat_history=chat_history
                )
                
                # Parse the structured output
                if isinstance(result, dict):
                    extracted_data = result
                else:
                    # Fallback parsing if needed
                    extracted_data = {
                        "intent": "general",
                        "letter": None,
                        "name": None,
                        "confidence": 0.8,
                        "age": None,
                        "emotion": "neutral"
                    }
                
                # Update session memory with extracted data
                if extracted_data.get("name"):
                    self.session_memory.derived_state.child_name = extracted_data["name"]
                if extracted_data.get("letter"):
                    self.session_memory.derived_state.current_letter = extracted_data["letter"]
                
                return AgentResponse(
                    agent_name="Understanding Agent",
                    response=f"I understand you want to {extracted_data.get('intent', 'learn')}!",
                    confidence=float(extracted_data.get("confidence", 0.8)),
                    extracted_data=extracted_data
                )
            else:
                # Fallback without AI
                return self._fallback_understanding(user_input)
                
        except Exception as e:
            logger.error(f"Understanding agent error: {e}")
            return self._fallback_understanding(user_input)
    
    def _fallback_understanding(self, user_input: str) -> AgentResponse:
        """Fallback understanding without AI"""
        # Simple pattern matching as backup
        intent = "general"
        letter = None
        name = None
        
        input_lower = user_input.lower()
        
        # Detect intent
        if any(word in input_lower for word in ["teach", "learn", "show"]):
            intent = "learn_letter"
        elif any(word in input_lower for word in ["next", "another"]):
            intent = "next_letter"
        elif any(word in input_lower for word in ["my name is", "i'm", "i am"]):
            intent = "introduction"
            # Extract name
            for marker in ["my name is", "i'm", "i am"]:
                if marker in input_lower:
                    parts = input_lower.split(marker)
                    if len(parts) > 1:
                        name = parts[1].strip().split()[0] if parts[1].strip() else None
                        break
        
        # Extract letter
        letter_match = re.search(r'\b([A-Za-z])\b', user_input)
        if letter_match:
            letter = letter_match.group(1).upper()
        
        return AgentResponse(
            agent_name="Understanding Agent",
            response="I'm here to help you learn!",
            confidence=0.6,
            extracted_data={
                "intent": intent,
                "letter": letter,
                "name": name,
                "confidence": 0.6
            }
        )
    
    def lesson_agent_process(self, context: Dict) -> AgentResponse:
        """
        Lesson Agent: AI-powered lesson generation
        """
        try:
            letter = context.get("current_letter", "A")
            child_name = self.session_memory.derived_state.child_name or "friend"
            difficulty = self.session_memory.derived_state.difficulty_level.value
            
            # Get curriculum info for the letter
            letter_info = self.curriculum.get("letters", {}).get(letter, {})
            curriculum_str = json.dumps(letter_info, indent=2)
            
            if self.lesson_chain:
                # Generate AI lesson
                response = self.lesson_chain.run(
                    letter=letter,
                    curriculum_info=curriculum_str,
                    child_name=child_name,
                    difficulty=difficulty
                )
                
                return AgentResponse(
                    agent_name="Lesson Agent",
                    response=response.strip(),
                    metadata={"letter": letter, "lesson": letter_info}
                )
            else:
                # Fallback lesson
                return self._fallback_lesson(letter, letter_info, child_name)
                
        except Exception as e:
            logger.error(f"Lesson agent error: {e}")
            return self._fallback_lesson(
                context.get("current_letter", "A"),
                {},
                "friend"
            )
    
    def _fallback_lesson(self, letter: str, letter_info: Dict, child_name: str) -> AgentResponse:
        """Fallback lesson without AI"""
        response = f"Let's learn the letter {letter}, {child_name}! "
        if letter_info:
            response += f"It sounds like {letter_info.get('sound_description', 'a special sound')}. "
            examples = letter_info.get('example_words', [])
            if examples:
                response += f"Like in {examples[0]}!"
        return AgentResponse(
            agent_name="Lesson Agent",
            response=response,
            metadata={"letter": letter}
        )
    
    def feedback_agent_process(self, context: Dict) -> AgentResponse:
        """
        Feedback Agent: AI-powered performance feedback
        """
        try:
            attempt = context.get("user_input", "")
            letter = context.get("current_letter", "A")
            confidence = context.get("confidence", 0.7)
            streak = self.session_memory.derived_state.streak_count
            
            if self.feedback_chain:
                # Generate AI feedback
                response = self.feedback_chain.run(
                    attempt=attempt,
                    letter=letter,
                    confidence=confidence,
                    streak=streak
                )
                
                # Update streak based on confidence
                if confidence > 0.8:
                    self.session_memory.derived_state.streak_count += 1
                elif confidence < 0.5:
                    self.session_memory.derived_state.streak_count = 0
                
                return AgentResponse(
                    agent_name="Feedback Agent",
                    response=response.strip(),
                    confidence=confidence,
                    metadata={"streak": self.session_memory.derived_state.streak_count}
                )
            else:
                return self._fallback_feedback(letter, confidence, streak)
                
        except Exception as e:
            logger.error(f"Feedback agent error: {e}")
            return self._fallback_feedback("A", 0.7, 0)
    
    def _fallback_feedback(self, letter: str, confidence: float, streak: int) -> AgentResponse:
        """Fallback feedback without AI"""
        if confidence > 0.8:
            response = f"Excellent! You're doing great with {letter}! ⭐"
        elif confidence > 0.6:
            response = f"Good try! You're getting closer with {letter}!"
        else:
            response = f"Keep practicing! You're learning {letter} well!"
        
        return AgentResponse(
            agent_name="Feedback Agent",
            response=response,
            confidence=confidence
        )
    
    def personalization_agent_process(self, context: Dict) -> AgentResponse:
        """
        Personalization Agent: AI-powered adaptive learning
        """
        try:
            # Build child profile
            state = self.session_memory.get_derived_state_dict()
            child_profile = {
                "name": state.get("child_name", "unknown"),
                "age_range": state.get("age_range", "3-5"),
                "current_letter": state.get("current_letter", "A"),
                "difficulty": state.get("difficulty_level", "easy")
            }
            
            progress = {
                "completed": state.get("letters_completed", []),
                "streak": state.get("streak_count", 0),
                "total_interactions": state.get("total_interactions", 0)
            }
            
            struggles = state.get("letters_struggled", [])
            
            if self.personalization_chain:
                # Generate AI personalization
                response = self.personalization_chain.run(
                    child_profile=json.dumps(child_profile),
                    progress=json.dumps(progress),
                    struggles=json.dumps(struggles)
                )
                
                # Parse recommendations
                next_letter = self._extract_next_letter(response)
                if next_letter:
                    self.session_memory.derived_state.current_letter = next_letter
                
                return AgentResponse(
                    agent_name="Personalization Agent",
                    response=response.strip(),
                    metadata={"next_letter": next_letter, "profile": child_profile}
                )
            else:
                return self._fallback_personalization(child_profile, progress, struggles)
                
        except Exception as e:
            logger.error(f"Personalization agent error: {e}")
            return self._fallback_personalization({}, {}, [])
    
    def _extract_next_letter(self, response: str) -> Optional[str]:
        """Extract next letter recommendation from AI response"""
        # Look for letter patterns in response
        match = re.search(r'letter ([A-Z])', response, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    
    def _fallback_personalization(self, profile: Dict, progress: Dict, struggles: List) -> AgentResponse:
        """Fallback personalization without AI"""
        next_letter = self.session_memory.suggest_next_letter()
        name = profile.get("name", "friend")
        
        response = f"Great job, {name}! "
        if struggles:
            response += f"Let's practice {struggles[0]} again. "
        else:
            response += f"Ready for {next_letter}? "
        
        return AgentResponse(
            agent_name="Personalization Agent",
            response=response,
            metadata={"next_letter": next_letter}
        )
    
    def safety_agent_process(self, content: str) -> AgentResponse:
        """
        Safety Agent: AI-powered content filtering
        """
        try:
            if self.safety_chain:
                # Check content with AI
                result = self.safety_chain.run(content=content)
                
                is_safe = "SAFE" in result.upper()
                
                if not is_safe:
                    return AgentResponse(
                        agent_name="Safety Agent",
                        response="Let's talk about letters instead! What letter would you like to learn?",
                        confidence=0.0,
                        metadata={"safe": False, "reason": result}
                    )
                
                return AgentResponse(
                    agent_name="Safety Agent",
                    response="",
                    confidence=1.0,
                    metadata={"safe": True}
                )
            else:
                return self._fallback_safety(content)
                
        except Exception as e:
            logger.error(f"Safety agent error: {e}")
            return self._fallback_safety(content)
    
    def _fallback_safety(self, content: str) -> AgentResponse:
        """Fallback safety check without AI"""
        unsafe_patterns = [
            "address", "phone", "email", "password",
            "credit card", "social security", "school name"
        ]
        
        content_lower = content.lower()
        is_safe = not any(pattern in content_lower for pattern in unsafe_patterns)
        
        if not is_safe:
            return AgentResponse(
                agent_name="Safety Agent",
                response="Let's focus on learning letters!",
                confidence=0.0,
                metadata={"safe": False}
            )
        
        return AgentResponse(
            agent_name="Safety Agent",
            response="",
            confidence=1.0,
            metadata={"safe": True}
        )
    
    def process_interaction(self, user_input: str) -> Dict:
        """
        Main method to process interaction using all AI agents
        """
        try:
            # Step 1: Safety check first
            safety_result = self.safety_agent_process(user_input)
            if not safety_result.metadata.get("safe", True):
                return {
                    "success": True,
                    "response": safety_result.response,
                    "state": self.session_memory.get_derived_state_dict()
                }
            
            # Step 2: Understand user input with AI
            understanding_result = self.understanding_agent_process(user_input)
            extracted_data = understanding_result.extracted_data or {}
            
            # Build context for other agents
            context = {
                "user_input": user_input,
                "current_letter": self.session_memory.derived_state.current_letter,
                "intent": extracted_data.get("intent", "general"),
                "extracted_letter": extracted_data.get("letter"),
                "confidence": extracted_data.get("confidence", 0.7)
            }
            
            # Step 3: Generate appropriate response based on intent
            responses = []
            
            if extracted_data.get("intent") == "learn_letter":
                # Use lesson agent for teaching
                if extracted_data.get("letter"):
                    self.session_memory.derived_state.current_letter = extracted_data["letter"]
                lesson_result = self.lesson_agent_process(context)
                responses.append(lesson_result.response)
                
            elif extracted_data.get("intent") == "next_letter":
                # Get personalized next letter
                personal_result = self.personalization_agent_process(context)
                responses.append(personal_result.response)
                
            elif extracted_data.get("intent") == "introduction":
                # Welcome with personalization
                name = extracted_data.get("name", "friend")
                responses.append(f"Hi {name}! I'm Bubbly! Let's learn the alphabet together! 🫧")
                
            else:
                # General response with current letter context
                lesson_result = self.lesson_agent_process(context)
                responses.append(lesson_result.response)
            
            # Step 4: Add feedback if appropriate
            if extracted_data.get("letter") or "letter" in user_input.lower():
                feedback_result = self.feedback_agent_process(context)
                responses.append(feedback_result.response)
            
            # Combine responses
            final_response = " ".join(responses)
            
            # Update conversation memory
            self.conversation_memory.save_context(
                {"input": user_input},
                {"output": final_response}
            )
            
            # Update session memory
            self.session_memory.add_turn(
                user_input,
                final_response,
                extracted_data.get("intent"),
                extracted_data.get("confidence", 0.7)
            )
            
            return {
                "success": True,
                "response": final_response,
                "state": self.session_memory.get_derived_state_dict(),
                "extracted_data": extracted_data,
                "metadata": {
                    "ai_powered": True,
                    "model_type": self.model_type,
                    "agents_used": ["Understanding", "Safety", "Lesson", "Feedback", "Personalization"]
                }
            }
            
        except Exception as e:
            logger.error(f"AI processing error: {e}")
            # Fallback to simple response
            return {
                "success": False,
                "response": "Let's learn the alphabet together! What letter interests you?",
                "state": self.session_memory.get_derived_state_dict(),
                "error": str(e)
            }