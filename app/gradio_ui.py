"""
KidSafe Alphabet Tutor - Bubbly 🫧
Main Gradio UI Application
Author: Nouran Darwish
"""

import gradio as gr
import asyncio
import json
import numpy as np
from typing import Dict, Optional, Tuple, List
from datetime import datetime
import logging
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import SessionMemory
from agents.crew_setup import AlphabetTutorCrew
from speech.asr import ASRProcessor
from speech.tts import TTSProcessor
from vision.letter_detector import LetterDetector
from vision.object_detector import ObjectDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BubblyTutor:
    """Main application class for KidSafe Alphabet Tutor"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing Bubbly Tutor...")
        
        # Core components
        self.session_memory = SessionMemory()
        self.crew = AlphabetTutorCrew(self.session_memory)
        
        # Speech components
        self.asr = ASRProcessor()
        self.tts = TTSProcessor()
        
        # Vision components
        self.letter_detector = LetterDetector()
        self.object_detector = ObjectDetector()
        
        # Load curriculum
        with open('app/curriculum.json', 'r') as f:
            self.curriculum = json.load(f)
            
        # Settings
        self.parental_gate_active = False
        self.camera_enabled = False
        
        logger.info("Bubbly Tutor initialized successfully!")
        
    def process_audio(self, audio_input, state):
        """
        Process audio input from child
        Target: <1.2s response time
        """
        try:
            if audio_input is None:
                return "Please speak into the microphone!", state, None
                
            # Step 1: ASR (300-500ms)
            transcription, confidence = self.asr.transcribe(audio_input)
            logger.info(f"Transcription: '{transcription}' (confidence: {confidence:.2f})")
            
            if not transcription:
                return "I couldn't hear that. Can you try again?", state, None
                
            # Step 2: Process with CrewAI agents (200-300ms)
            response = self.crew.process_interaction(transcription, confidence)
            
            # Step 3: Update session memory
            assistant_response = response.get('response', "Let's learn letters together!")
            self.session_memory.add_turn(transcription, assistant_response, confidence=confidence)
            
            # Step 4: Generate TTS (streaming, 150-250ms first chunk)
            audio_response = self.tts.synthesize(assistant_response, streaming=True)
            
            # Update state display
            state = self.session_memory.get_formatted_memory()
            
            return assistant_response, state, audio_response
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return "Let me help you with letters!", state, None
            
    def process_image(self, image_input, state):
        """Process image input for letter/object detection"""
        try:
            if image_input is None:
                return "Please show me a letter or object!", state, None
                
            # Detect letters
            letter_results = self.letter_detector.detect(image_input)
            
            # Detect objects
            object_results = self.object_detector.detect(image_input)
            
            response = self._generate_vision_response(letter_results, object_results)
            
            # Update memory
            self.session_memory.add_turn(
                f"[Showed image with {letter_results.get('letter', 'unknown')}]",
                response
            )
            
            state = self.session_memory.get_formatted_memory()
            
            return response, state, None
            
        except Exception as e:
            logger.error(f"Image processing error: {e}")
            return "I couldn't see that clearly. Can you try again?", state, None
            
    def _generate_vision_response(self, letter_results: Dict, object_results: Dict) -> str:
        """Generate response based on vision detection results"""
        response_parts = []
        
        if letter_results.get('detected'):
            letter = letter_results['letter']
            confidence = letter_results['confidence']
            response_parts.append(f"I see the letter {letter}! (confidence: {confidence:.2f})")
            
            # Get letter info from curriculum
            if letter in self.curriculum['letters']:
                letter_info = self.curriculum['letters'][letter]
                response_parts.append(f"'{letter}' sounds like {letter_info['sound_description']}!")
                
        if object_results.get('detected'):
            objects = object_results['objects']
            for obj in objects[:3]:  # Limit to top 3 objects
                response_parts.append(f"I also see a {obj['label']}!")
                
                # Check if object maps to a letter
                for letter, info in self.curriculum['letters'].items():
                    if obj['label'].lower() in info['mapped_object'].lower():
                        response_parts.append(f"'{obj['label']}' starts with the letter {letter}!")
                        break
                        
        if not response_parts:
            return "Can you show me a letter or an object? Hold it closer to the camera!"
            
        return " ".join(response_parts)
        
    def select_next_letter(self, state):
        """Select next letter based on progress"""
        next_letter = self.session_memory.suggest_next_letter()
        
        if next_letter in self.curriculum['letters']:
            letter_info = self.curriculum['letters'][next_letter]
            response = f"Let's learn the letter {next_letter}! "
            response += f"'{next_letter}' sounds like {letter_info['sound_description']}. "
            response += f"Like in {letter_info['example_words'][0]}!"
            
            # Update memory
            self.session_memory.add_turn("What's next?", response)
            self.session_memory.derived_state.current_letter = next_letter
            
            state = self.session_memory.get_formatted_memory()
            
            # Generate audio
            audio = self.tts.synthesize(response)
            
            return response, state, audio
        
        return "Great job! You're doing amazing!", state, None
        
    def check_parental_gate(self, answer: str) -> Tuple[bool, str]:
        """Simple math puzzle for parental gate"""
        try:
            # Simple math: 3 + 4 = ?
            if answer.strip() == "7":
                self.parental_gate_active = True
                return True, "Access granted! You can now change settings."
            else:
                return False, "Incorrect answer. Please try again."
        except:
            return False, "Please enter a number."
            
    def update_settings(self, age_range: str, camera_enabled: bool, speech_rate: float):
        """Update application settings"""
        if not self.parental_gate_active:
            return "Please complete the parental gate first."
            
        self.session_memory.update_settings(age_range=age_range, vision=camera_enabled)
        self.camera_enabled = camera_enabled
        self.tts.set_speech_rate(speech_rate)
        
        return f"Settings updated! Age range: {age_range}, Camera: {'On' if camera_enabled else 'Off'}, Speech rate: {speech_rate}x"
        
    def reset_session(self):
        """Reset the session"""
        self.session_memory.reset()
        self.parental_gate_active = False
        return "Session reset! Let's start fresh!", "", None

def create_interface():
    """Create the Gradio interface"""
    
    tutor = BubblyTutor()
    
    # Custom CSS for child-friendly design
    custom_css = """
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Comic Sans MS', cursive;
    }
    .bubble-avatar {
        background: radial-gradient(circle, #87CEEB, #4682B4);
        border-radius: 50%;
        width: 100px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    .star-badge {
        color: gold;
        font-size: 24px;
    }
    """
    
    with gr.Blocks(title="Bubbly - KidSafe Alphabet Tutor", css=custom_css) as interface:
        
        gr.HTML("""
        <div style='text-align: center; padding: 20px;'>
            <div class='bubble-avatar'>🫧</div>
            <h1 style='color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                Bubbly's Alphabet Adventure! 🌟
            </h1>
            <p style='color: white;'>Let's learn letters together!</p>
        </div>
        """)
        
        with gr.Row():
            # Left Panel - Interaction
            with gr.Column(scale=2):
                # Audio Input Section
                gr.Markdown("### 🎤 Talk to Bubbly!")
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="numpy",
                    label="Push to Talk",
                    streaming=False
                )
                
                # Camera Input Section
                gr.Markdown("### 📷 Show me a letter!")
                camera_input = gr.Image(
                    sources=["webcam"],
                    type="numpy",
                    label="Camera",
                    visible=True
                )
                recognize_btn = gr.Button("🔍 Recognize", variant="primary")
                
                # Response Section
                gr.Markdown("### 💬 Bubbly says:")
                response_text = gr.Textbox(
                    label="",
                    lines=3,
                    interactive=False
                )
                audio_output = gr.Audio(label="Listen", type="numpy", autoplay=True)
                
                # Next Letter Button
                next_btn = gr.Button("➡️ Next Letter!", variant="secondary")
                
            # Right Panel - State and Settings
            with gr.Column(scale=1):
                # Progress Display
                gr.Markdown("### 🌟 Your Progress")
                progress_display = gr.HTML(
                    value="<div class='star-badge'>⭐ × 0</div>"
                )
                
                # Memory Display
                gr.Markdown("### 🧠 Memory")
                memory_display = gr.Textbox(
                    label="Session Memory",
                    lines=10,
                    interactive=False,
                    value="Session just started!"
                )
                
                # Settings (with parental gate)
                with gr.Accordion("⚙️ Settings (Parents Only)", open=False):
                    gr.Markdown("**Parental Gate:** What is 3 + 4?")
                    gate_answer = gr.Textbox(label="Answer", type="text")
                    gate_btn = gr.Button("Unlock Settings")
                    gate_result = gr.Textbox(label="", interactive=False)
                    
                    with gr.Group(visible=False) as settings_group:
                        age_range = gr.Radio(
                            choices=["3-5", "6-8"],
                            value="3-5",
                            label="Age Range"
                        )
                        camera_toggle = gr.Checkbox(
                            label="Enable Camera",
                            value=True
                        )
                        speech_rate = gr.Slider(
                            minimum=0.5,
                            maximum=1.5,
                            value=0.8,
                            step=0.1,
                            label="Speech Rate"
                        )
                        apply_settings_btn = gr.Button("Apply Settings")
                        settings_result = gr.Textbox(label="", interactive=False)
                    
                # Reset Button
                reset_btn = gr.Button("🔄 New Session", variant="stop")
        
        # Event Handlers
        
        def handle_audio(audio, memory):
            return tutor.process_audio(audio, memory)
            
        def handle_image(image, memory):
            return tutor.process_image(image, memory)
            
        def handle_next(memory):
            return tutor.select_next_letter(memory)
            
        def handle_gate(answer):
            success, message = tutor.check_parental_gate(answer)
            return message, gr.update(visible=success)
            
        def handle_settings(age, camera, rate):
            return tutor.update_settings(age, camera, rate)
            
        def handle_reset():
            return tutor.reset_session()
        
        # Connect events
        audio_input.stop_recording(
            handle_audio,
            inputs=[audio_input, memory_display],
            outputs=[response_text, memory_display, audio_output]
        )
        
        recognize_btn.click(
            handle_image,
            inputs=[camera_input, memory_display],
            outputs=[response_text, memory_display, audio_output]
        )
        
        next_btn.click(
            handle_next,
            inputs=[memory_display],
            outputs=[response_text, memory_display, audio_output]
        )
        
        gate_btn.click(
            handle_gate,
            inputs=[gate_answer],
            outputs=[gate_result, settings_group]
        )
        
        apply_settings_btn.click(
            handle_settings,
            inputs=[age_range, camera_toggle, speech_rate],
            outputs=[settings_result]
        )
        
        reset_btn.click(
            handle_reset,
            inputs=[],
            outputs=[response_text, memory_display, audio_output]
        )
        
        # Launch message
        interface.load(
            lambda: ("Hi! I'm Bubbly! 🫧 Let's learn the alphabet together! Say hello or press 'Next Letter' to start!", 
                     "Session just started!",
                     None),
            outputs=[response_text, memory_display, audio_output]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_api=False
    )