"""
Ollama LLM Client for Local Language Model Integration
Uses Llama 3.2 3B (quantized) for efficient inference
Author: Nouran Darwish
"""

import requests
import json
import logging
from typing import Dict, List, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """
    Client for interacting with Ollama local LLM
    Provides child-friendly responses for alphabet tutoring
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        """
        Initialize Ollama client
        Args:
            base_url: Ollama server URL
            model: Model to use (quantized version recommended)
        """
        self.base_url = base_url
        self.model = model
        self.timeout = 10  # seconds
        
        # Check if Ollama is available
        self.available = self._check_availability()
        
        if self.available:
            logger.info(f"Ollama client initialized with model: {model}")
        else:
            logger.warning("Ollama not available, using fallback responses")
            
    def _check_availability(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
            
    def generate(self, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 150) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
        """
        if not self.available:
            return self._fallback_response(prompt)
            
        try:
            # Prepare request
            data = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            if system_prompt:
                data["system"] = system_prompt
                
            # Make request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama error: {response.status_code}")
                return self._fallback_response(prompt)
                
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return self._fallback_response(prompt)
            
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Chat with conversation history
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            
        Returns:
            Generated response
        """
        if not self.available:
            return self._fallback_response(messages[-1]['content'] if messages else "")
            
        try:
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "").strip()
            else:
                return self._fallback_response(messages[-1]['content'] if messages else "")
                
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return self._fallback_response(messages[-1]['content'] if messages else "")
            
    def _fallback_response(self, prompt: str) -> str:
        """
        Fallback responses when Ollama is unavailable
        """
        prompt_lower = prompt.lower()
        
        # Pattern-based responses for alphabet tutoring
        if 'letter' in prompt_lower:
            if any(letter in prompt_lower for letter in 'abcdefghijklmnopqrstuvwxyz'):
                # Extract letter
                for letter in 'abcdefghijklmnopqrstuvwxyz':
                    if letter in prompt_lower:
                        return f"The letter {letter.upper()} is wonderful! Can you say it with me?"
            return "Let's learn letters together! Which letter would you like to practice?"
            
        elif 'hello' in prompt_lower or 'hi' in prompt_lower:
            return "Hello! I'm Bubbly, your alphabet friend! Ready to learn some letters?"
            
        elif 'help' in prompt_lower:
            return "I can help you learn the alphabet! Just say a letter or show me one!"
            
        elif 'name' in prompt_lower:
            return "Nice to meet you! What letter would you like to learn today?"
            
        elif any(word in prompt_lower for word in ['good', 'great', 'excellent', 'perfect']):
            return "You're doing amazing! Keep up the great work! ⭐"
            
        elif any(word in prompt_lower for word in ['again', 'repeat', 'once more']):
            return "Sure! Let's try that again. You're doing great!"
            
        else:
            return "That's interesting! Would you like to practice a letter?"
            
    def create_child_friendly_prompt(self, context: Dict) -> str:
        """
        Create a child-friendly system prompt
        """
        age_range = context.get('age_range', '3-5')
        current_letter = context.get('current_letter', 'A')
        child_name = context.get('child_name', 'friend')
        
        prompt = f"""You are Bubbly, a friendly and patient alphabet tutor for children aged {age_range}.
        You're currently teaching the letter {current_letter} to {child_name}.
        
        Guidelines:
        - Use simple, clear language appropriate for young children
        - Be encouraging and positive, celebrate all attempts
        - Keep responses short (1-2 sentences)
        - Use playful and engaging tone
        - Never use complex words or concepts
        - Always be patient and supportive
        - Include emoji occasionally for engagement
        - Focus on letter sounds and simple examples
        
        Remember: You're helping a young child learn, so be warm, fun, and encouraging!"""
        
        return prompt
        
    def analyze_pronunciation(self, letter: str, confidence: float) -> str:
        """
        Generate pronunciation feedback using LLM
        """
        if not self.available:
            if confidence > 0.8:
                return f"Excellent! You said '{letter}' perfectly!"
            elif confidence > 0.6:
                return f"Good try! The '{letter}' sound is getting better!"
            else:
                return f"Let's practice '{letter}' together one more time!"
                
        prompt = f"""A child is learning the letter '{letter}' and pronounced it with {confidence:.0%} confidence.
        Generate a brief, encouraging response (max 2 sentences) that:
        1. Acknowledges their effort
        2. Provides gentle guidance if confidence is low
        3. Celebrates if confidence is high
        Keep it simple and child-friendly."""
        
        return self.generate(prompt, temperature=0.7, max_tokens=50)
        
    def suggest_activity(self, letter: str, activity_type: str) -> str:
        """
        Generate activity suggestion for letter learning
        """
        if not self.available:
            activities = {
                'repeat-after-me': f"Let's say '{letter}' together! Ready? '{letter}'!",
                'find-an-object': f"Can you find something that starts with '{letter}'?",
                'show-the-letter': f"Can you show me the letter '{letter}'?",
                'choose-the-sound': f"Which sound is '{letter}'? Listen carefully!"
            }
            return activities.get(activity_type, f"Let's practice the letter '{letter}'!")
            
        prompt = f"""Create a fun activity for teaching the letter '{letter}'.
        Activity type: {activity_type}
        Make it engaging for a young child (1-2 sentences, simple language)."""
        
        return self.generate(prompt, temperature=0.8, max_tokens=50)