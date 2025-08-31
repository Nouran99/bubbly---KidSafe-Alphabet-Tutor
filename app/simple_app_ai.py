#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - AI-Enhanced Version
Uses actual AI models when available, falls back to rules when not
"""

import gradio as gr
import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import SessionMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import AI version, fall back to rule-based
try:
    from agents.crew_setup_ai import AlphabetTutorAI
    AI_MODE = True
    logger.info("AI mode available - using intelligent conversation")
except ImportError:
    from agents.crew_setup_simple import AlphabetTutorAgents
    AI_MODE = False
    logger.info("AI libraries not installed - using rule-based mode")

# Initialize
print("Initializing KidSafe Alphabet Tutor...")
print(f"Mode: {'AI-Powered' if AI_MODE else 'Rule-Based'}")

session_memory = SessionMemory()

if AI_MODE:
    # Try different AI backends
    model_type = os.getenv("AI_MODEL", "ollama")  # ollama, openai, or fallback
    api_key = os.getenv("OPENAI_API_KEY")
    
    agents = AlphabetTutorAI(session_memory, model_type=model_type, api_key=api_key)
    print(f"Using AI backend: {model_type}")
else:
    agents = AlphabetTutorAgents(session_memory)
    print("Using rule-based responses")

print("Ready!")

def chat_function(message, history):
    """Enhanced chat function with AI capabilities"""
    if not message:
        return history
    
    try:
        # Process message with AI or rules
        result = agents.process_interaction(message)
        
        # Extract response
        if isinstance(result, dict):
            response = result.get('response', 'Let me help you learn!')
            
            # Show extracted data if in AI mode
            if AI_MODE and result.get('extracted_data'):
                extracted = result['extracted_data']
                logger.info(f"AI extracted: {extracted}")
                
                # Add understanding indicator to response
                if extracted.get('intent') != 'chat':
                    response = f"[Understood: {extracted.get('intent', 'chat')}] " + response
        else:
            response = str(result)
        
        # Update memory
        session_memory.add_turn(message, response)
        
        # Add to history
        history = history or []
        history.append([message, response])
        
        return history
    except Exception as e:
        logger.error(f"Error: {e}")
        history = history or []
        history.append([message, "Let's try that again! What letter would you like to learn?"])
        return history

def clear_chat():
    """Clear chat and reset session"""
    session_memory.reset()
    return None

def get_system_info():
    """Get current system status"""
    mode = "AI-Powered" if AI_MODE else "Rule-Based"
    state = session_memory.get_derived_state_dict()
    
    info = f"""
    **System Mode**: {mode}
    **Current Letter**: {state.get('current_letter', 'A')}
    **Letters Learned**: {', '.join(state.get('letters_completed', [])[:5]) or 'None yet'}
    **Session Duration**: {state.get('session_duration', '0:00')}
    """
    
    if AI_MODE:
        info += f"\n**AI Backend**: {getattr(agents, 'model_type', 'unknown')}"
    
    return info

# Create enhanced interface
with gr.Blocks(title="KidSafe Alphabet Tutor - AI Enhanced", theme=gr.themes.Soft()) as app:
    gr.Markdown(f"""
    # 🎓 KidSafe Alphabet Tutor {'(AI-Powered)' if AI_MODE else '(Rule-Based)'}
    ### Learn the alphabet with Bubbly! 🫧
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=400,
                bubble_full_width=False,
                avatar_images=(None, "🫧")
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Say hello or ask about a letter...",
                    container=False,
                    scale=5,
                    label="Your message"
                )
                submit = gr.Button("Send", scale=1, variant="primary")
            
            with gr.Row():
                clear = gr.Button("Clear Chat", scale=1)
                
                # Example buttons for quick actions
                example_btns = [
                    gr.Button("Teach me A", scale=1),
                    gr.Button("Next letter", scale=1),
                    gr.Button("Play a game", scale=1)
                ]
        
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Session Info")
            info_display = gr.Markdown(get_system_info())
            refresh_btn = gr.Button("Refresh Info", size="sm")
            
            gr.Markdown("""
            ### 💡 Try saying:
            - "Hello, my name is [Name]"
            - "Teach me the letter B"
            - "What comes after C?"
            - "Can we play a game?"
            - "Show me words with D"
            - "I don't understand"
            """)
            
            if AI_MODE:
                gr.Markdown("""
                ### 🤖 AI Features:
                - Natural conversation
                - Context understanding
                - Emotion detection
                - Smart responses
                """)
    
    # Connect events
    msg.submit(lambda m, h: (chat_function(m, h), ""), [msg, chatbot], [chatbot, msg])
    submit.click(lambda m, h: (chat_function(m, h), ""), [msg, chatbot], [chatbot, msg])
    clear.click(clear_chat, None, chatbot)
    refresh_btn.click(get_system_info, None, info_display)
    
    # Example button actions
    example_btns[0].click(
        lambda h: chat_function("Teach me the letter A", h),
        [chatbot], [chatbot]
    )
    example_btns[1].click(
        lambda h: chat_function("Next letter please", h),
        [chatbot], [chatbot]
    )
    example_btns[2].click(
        lambda h: chat_function("Let's play a game", h),
        [chatbot], [chatbot]
    )
    
    # Initial message
    app.load(
        lambda: [["", f"Hi! I'm Bubbly! 🫧 I'm running in {'AI mode' if AI_MODE else 'simple mode'}. Let's learn the alphabet together! What's your name?"]],
        None,
        chatbot
    )
    app.load(get_system_info, None, info_display)

if __name__ == "__main__":
    print("\n" + "="*50)
    print(f"Starting KidSafe Alphabet Tutor ({'AI-Enhanced' if AI_MODE else 'Rule-Based'})")
    print("="*50)
    
    if not AI_MODE:
        print("\n💡 To enable AI features, install:")
        print("   pip install openai langchain")
        print("   Then set OPENAI_API_KEY or run Ollama locally")
    
    print("\nOpen your browser to: http://localhost:7860\n")
    
    # Launch with enhanced settings
    app.queue(max_size=10).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_api=False
    )