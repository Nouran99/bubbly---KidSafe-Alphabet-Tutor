#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Safe Gradio UI
A simplified version that avoids Gradio API schema issues
"""

import gradio as gr
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import SessionMemory
from agents.crew_setup_simple import AlphabetTutorAgents

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize components
logger.info("Initializing KidSafe Alphabet Tutor (Safe Mode)...")
session_memory = SessionMemory()
agents = AlphabetTutorAgents(session_memory)
logger.info("System initialized successfully!")

def process_message(message, history):
    """Process user message and return response"""
    try:
        # Process through agent system
        result = agents.process_interaction(message)
        
        # Extract response
        if isinstance(result, dict):
            response = result.get('response', 'Let me help you learn the alphabet!')
        else:
            response = str(result)
        
        # Update memory
        session_memory.add_turn(message, response)
        
        return response
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Let's try again! What letter would you like to learn?"

def reset_session():
    """Reset the session"""
    session_memory.reset()
    return "Hi! I'm Bubbly! 🫧 Let's learn the alphabet together!", []

def create_simple_interface():
    """Create a simplified Gradio interface"""
    
    with gr.Blocks(title="KidSafe Alphabet Tutor", theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🎓 KidSafe Alphabet Tutor
        ### Hi! I'm Bubbly! Let's learn the alphabet together! 🫧
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    value=[],
                    height=400,
                    bubble_full_width=False,
                    avatar_images=(None, "🫧")
                )
                
                msg = gr.Textbox(
                    label="Your message",
                    placeholder="Type 'hello' or 'teach me A' or press Enter...",
                    lines=1
                )
                
                with gr.Row():
                    submit = gr.Button("Send", variant="primary")
                    clear = gr.Button("New Session")
            
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 📚 Quick Commands
                - Say "hello" to start
                - "Teach me [letter]"
                - "Next letter"
                - "What's after [letter]?"
                
                ### 🌟 Features
                - Complete A-Z curriculum
                - Safe for children
                - No data saved
                - Fun learning!
                """)
        
        # Event handlers
        def respond(message, chat_history):
            response = process_message(message, chat_history)
            chat_history.append((message, response))
            return "", chat_history
        
        def clear_chat():
            reset_response, _ = reset_session()
            return [(None, reset_response)]
        
        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(clear_chat, None, chatbot)
        
        # Initial greeting
        interface.load(
            lambda: [(None, "Hi! I'm Bubbly! 🫧 Let's learn the alphabet together! Type 'hello' or ask me about any letter!")],
            None,
            chatbot
        )
    
    return interface

if __name__ == "__main__":
    try:
        interface = create_simple_interface()
        
        print("="*60)
        print("🎓 KidSafe Alphabet Tutor (Safe Mode)")
        print("="*60)
        print("\nStarting application...")
        print("Access at: http://localhost:7860")
        print("\nPress Ctrl+C to stop")
        print("-"*60)
        
        # Launch with minimal configuration to avoid errors
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=False,
            show_api=False,  # Disable API to avoid schema errors
            show_error=False,  # Don't show detailed errors
            quiet=True  # Reduce output
        )
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTry running: python fix_gradio_error.py")
        print("Or use: fix_asgi_error.bat (Windows) / fix_asgi_error.sh (Linux/Mac)")
        sys.exit(1)