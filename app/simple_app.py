#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Simplified Version
This version avoids all ASGI/Pydantic compatibility issues
"""

import gradio as gr
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import SessionMemory
from agents.crew_setup_simple import AlphabetTutorAgents

# Initialize
print("Initializing KidSafe Alphabet Tutor...")
session_memory = SessionMemory()
agents = AlphabetTutorAgents(session_memory)
print("Ready!")

def chat_function(message, history):
    """Simple chat function"""
    if not message:
        return history
    
    try:
        # Process message
        result = agents.process_interaction(message)
        
        # Extract response
        if isinstance(result, dict):
            response = result.get('response', 'Let me help you learn!')
        else:
            response = str(result)
        
        # Update memory
        session_memory.add_turn(message, response)
        
        # Add to history
        history = history or []
        history.append([message, response])
        
        return history
    except Exception as e:
        print(f"Error: {e}")
        history = history or []
        history.append([message, "Let's try that again! What letter would you like to learn?"])
        return history

def clear_chat():
    """Clear chat and reset session"""
    session_memory.reset()
    return None

# Create simple interface
with gr.Blocks(title="KidSafe Alphabet Tutor") as app:
    gr.Markdown("# 🎓 KidSafe Alphabet Tutor\n### Learn the alphabet with Bubbly! 🫧")
    
    chatbot = gr.Chatbot(
        height=400,
        bubble_full_width=False
    )
    
    with gr.Row():
        msg = gr.Textbox(
            placeholder="Say hello or ask about a letter...",
            container=False,
            scale=5
        )
        submit = gr.Button("Send", scale=1)
    
    with gr.Row():
        clear = gr.Button("Clear Chat")
        
    gr.Markdown("""
    **Try saying:**
    - "Hello"
    - "Teach me the letter A"
    - "What comes after B?"
    - "Next letter"
    """)
    
    # Connect events
    msg.submit(lambda m, h: (chat_function(m, h), ""), [msg, chatbot], [chatbot, msg])
    submit.click(lambda m, h: (chat_function(m, h), ""), [msg, chatbot], [chatbot, msg])
    clear.click(clear_chat, None, chatbot)
    
    # Initial message
    app.load(
        lambda: [["", "Hi! I'm Bubbly! 🫧 Let's learn the alphabet together! Say hello or ask me about any letter!"]],
        None,
        chatbot
    )

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Starting KidSafe Alphabet Tutor (Simple Version)")
    print("="*50)
    print("\nOpen your browser to: http://localhost:7860\n")
    
    # Launch with minimal settings to avoid errors
    app.queue(max_size=10).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_api=False
    )