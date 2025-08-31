#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Bubbly 🫧
Simplified Gradio UI Application (No external model dependencies)
Author: Nouran Darwish
"""

import gradio as gr
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
from agents.crew_setup_simple import AlphabetTutorAgents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BubblyTutorSimple:
    """Simplified application class for KidSafe Alphabet Tutor"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing Bubbly Tutor (Simplified Version)...")
        
        # Core components
        self.session_memory = SessionMemory()
        self.agents = AlphabetTutorAgents(self.session_memory)
        
        # Load curriculum
        with open('app/curriculum.json', 'r') as f:
            self.curriculum = json.load(f)
            
        # Settings
        self.parental_gate_active = False
        self.camera_enabled = False
        self.speech_rate = 0.8
        
        logger.info("Bubbly Tutor initialized successfully!")
        
    def process_text_input(self, text_input: str, state: str) -> Tuple[str, str]:
        """
        Process text input from child (fallback for audio)
        """
        try:
            if not text_input:
                return "Please type something or use the microphone!", state
                
            # Simulate confidence based on input quality
            confidence = 0.8 if len(text_input) > 1 else 0.6
            
            # Process with agents
            response = self.agents.process_interaction(text_input, confidence)
            
            # Update session memory
            assistant_response = response.get('response', "Let's learn letters together!")
            self.session_memory.add_turn(text_input, assistant_response, confidence=confidence)
            
            # Update state display
            state = self.session_memory.get_formatted_memory()
            
            return assistant_response, state
            
        except Exception as e:
            logger.error(f"Text processing error: {e}")
            return "Let me help you with letters!", state
            
    def process_audio_simple(self, audio_input, state):
        """
        Simplified audio processing (without actual ASR)
        """
        try:
            if audio_input is None:
                return "Please speak into the microphone!", state
                
            # Simulate transcription for demo
            # In production, this would use the ASR module
            simulated_transcripts = [
                "Teach me B",
                "My name is Alice",
                "What's next?",
                "B",
                "Show me A"
            ]
            
            import random
            transcription = random.choice(simulated_transcripts)
            confidence = random.uniform(0.6, 0.9)
            
            logger.info(f"Simulated transcription: '{transcription}' (confidence: {confidence:.2f})")
            
            # Process with agents
            response = self.agents.process_interaction(transcription, confidence)
            
            # Update session memory
            assistant_response = response.get('response', "Let's learn letters together!")
            self.session_memory.add_turn(transcription, assistant_response, confidence=confidence)
            
            # Update state display
            state = self.session_memory.get_formatted_memory()
            
            return assistant_response, state
            
        except Exception as e:
            logger.error(f"Audio processing error: {e}")
            return "Let me help you with letters!", state
            
    def process_image_simple(self, image_input, state):
        """Simplified image processing (without actual vision models)"""
        try:
            if image_input is None:
                return "Please show me a letter or object!", state
                
            # Simulate detection for demo
            import random
            detected_letters = ['A', 'B', 'C', 'D', 'E']
            detected_objects = ['Apple', 'Ball', 'Cat', 'Dog', 'Elephant']
            
            letter = random.choice(detected_letters)
            obj = random.choice(detected_objects)
            confidence = random.uniform(0.7, 0.95)
            
            response = f"I see the letter {letter}! (confidence: {confidence:.2f})\n"
            response += f"I also see a {obj}! '{obj}' starts with the letter {letter[0]}!"
            
            # Update memory
            self.session_memory.add_turn(
                f"[Showed image with {letter}]",
                response
            )
            
            state = self.session_memory.get_formatted_memory()
            
            return response, state
            
        except Exception as e:
            logger.error(f"Image processing error: {e}")
            return "I couldn't see that clearly. Can you try again?", state
            
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
            
            return response, state
        
        return "Great job! You're doing amazing!", state
        
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
        self.speech_rate = speech_rate
        
        return f"Settings updated! Age range: {age_range}, Camera: {'On' if camera_enabled else 'Off'}, Speech rate: {speech_rate}x"
        
    def reset_session(self):
        """Reset the session"""
        self.session_memory.reset()
        self.parental_gate_active = False
        return "Session reset! Let's start fresh!", ""

def create_interface():
    """Create the Gradio interface"""
    
    tutor = BubblyTutorSimple()
    
    # Custom CSS for child-friendly design
    custom_css = """
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Comic Sans MS', cursive, sans-serif;
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
        margin: 0 auto;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    .star-badge {
        color: gold;
        font-size: 24px;
        text-align: center;
    }
    """
    
    with gr.Blocks(title="Bubbly - KidSafe Alphabet Tutor", css=custom_css, theme=gr.themes.Soft()) as interface:
        
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
                # Text Input Section (Primary for simplified version)
                gr.Markdown("### 💬 Talk to Bubbly!")
                text_input = gr.Textbox(
                    label="Type your message",
                    placeholder="Type 'Hello', 'Teach me A', or 'My name is...'",
                    lines=1
                )
                submit_btn = gr.Button("Send", variant="primary")
                
                # Audio Input Section (Simulated)
                gr.Markdown("### 🎤 Or use your voice! (Demo Mode)")
                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="numpy",
                    label="Push to Talk (Simulated)",
                )
                
                # Camera Input Section (Simulated)
                gr.Markdown("### 📷 Show me a letter! (Demo Mode)")
                camera_input = gr.Image(
                    sources=["webcam"],
                    type="numpy",
                    label="Camera (Simulated)",
                )
                recognize_btn = gr.Button("🔍 Recognize", variant="primary")
                
                # Response Section
                gr.Markdown("### 💬 Bubbly says:")
                response_text = gr.Textbox(
                    label="",
                    lines=3,
                    interactive=False
                )
                
                # Next Letter Button
                next_btn = gr.Button("➡️ Next Letter!", variant="secondary")
                
            # Right Panel - State and Settings
            with gr.Column(scale=1):
                # Progress Display
                gr.Markdown("### 🌟 Your Progress")
                progress_html = gr.HTML(
                    value="<div class='star-badge'>⭐ Keep learning! ⭐</div>"
                )
                
                # Memory Display
                gr.Markdown("### 🧠 Memory")
                memory_display = gr.Textbox(
                    label="Session Memory",
                    lines=12,
                    interactive=False,
                    value="Session just started!\n\nSay hello or click 'Next Letter' to begin!"
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
                            label="Enable Camera (Demo)",
                            value=False
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
        
        # Instructions
        with gr.Row():
            gr.Markdown("""
            ### 📚 How to Use:
            1. **Type or speak** to Bubbly (e.g., "Hello", "Teach me B", "My name is Alex")
            2. **Click 'Next Letter'** to progress through the alphabet
            3. **Show letters or objects** to the camera (demo will simulate recognition)
            4. **Parents:** Complete the math puzzle to access settings
            
            ### 🎯 Try These:
            - "My name is [your name]"
            - "Teach me the letter A"
            - "What's next?"
            - "Help me learn"
            - "Let's play a game"
            
            **Note:** This is a simplified demo version. Audio and vision features are simulated.
            """)
        
        # Event Handlers
        def handle_text(text, memory):
            return tutor.process_text_input(text, memory)
            
        def handle_audio(audio, memory):
            return tutor.process_audio_simple(audio, memory)
            
        def handle_image(image, memory):
            return tutor.process_image_simple(image, memory)
            
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
        submit_btn.click(
            handle_text,
            inputs=[text_input, memory_display],
            outputs=[response_text, memory_display]
        ).then(
            lambda: "",
            outputs=[text_input]  # Clear input after submission
        )
        
        text_input.submit(
            handle_text,
            inputs=[text_input, memory_display],
            outputs=[response_text, memory_display]
        ).then(
            lambda: "",
            outputs=[text_input]  # Clear input after submission
        )
        
        audio_input.stop_recording(
            handle_audio,
            inputs=[audio_input, memory_display],
            outputs=[response_text, memory_display]
        )
        
        recognize_btn.click(
            handle_image,
            inputs=[camera_input, memory_display],
            outputs=[response_text, memory_display]
        )
        
        next_btn.click(
            handle_next,
            inputs=[memory_display],
            outputs=[response_text, memory_display]
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
            outputs=[response_text, memory_display]
        )
        
        # Launch message
        interface.load(
            lambda: ("Hi! I'm Bubbly! 🫧 Let's learn the alphabet together! Type hello, tell me your name, or press 'Next Letter' to start!", 
                     "Session just started!\n\nWaiting for you to say hello..."),
            outputs=[response_text, memory_display]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    try:
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False,
            prevent_thread_lock=False,
            show_error=True,
            quiet=True
        )
    except ValueError:
        # Fallback if localhost not accessible
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False,
            show_error=True,
            quiet=True
        )