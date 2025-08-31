#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - AI-Powered Version
Fully AI-driven tutoring without hard-coded responses
Author: Nouran Darwish
"""

import gradio as gr
import sys
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.state import SessionMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import AI-powered agents
try:
    from agents.crew_ai_powered import AIAlphabetTutorAgents
    AI_AVAILABLE = True
    logger.info("AI-powered agents loaded successfully")
except ImportError as e:
    logger.warning(f"AI agents not available: {e}")
    logger.info("Falling back to rule-based agents")
    from agents.crew_setup_simple import AlphabetTutorAgents
    AI_AVAILABLE = False

# Initialize
print("=" * 60)
print("Initializing KidSafe Alphabet Tutor - AI-Powered Version")
print("=" * 60)

# Initialize session memory
session_memory = SessionMemory()

# Initialize AI agents
if AI_AVAILABLE:
    # Check for API keys or model configuration
    openai_key = os.getenv("OPENAI_API_KEY")
    use_ollama = os.getenv("USE_OLLAMA", "true").lower() == "true"
    
    if use_ollama:
        print("Using Ollama for local AI processing (no API key needed)")
        print("Make sure Ollama is running: ollama serve")
        agents = AIAlphabetTutorAgents(
            session_memory,
            model_type="ollama"
        )
    elif openai_key:
        print("Using OpenAI GPT models")
        agents = AIAlphabetTutorAgents(
            session_memory,
            model_type="openai",
            api_key=openai_key
        )
    else:
        print("No AI configuration found. Using intelligent fallback mode.")
        agents = AIAlphabetTutorAgents(
            session_memory,
            model_type="mock"
        )
else:
    print("Using rule-based agents (AI libraries not installed)")
    agents = AlphabetTutorAgents(session_memory)

print("Ready for AI-powered alphabet learning!")
print("=" * 60)

def chat_function(message, history):
    """AI-powered chat function with intelligent data extraction"""
    if not message:
        return history
    
    try:
        # Process with AI agents
        result = agents.process_interaction(message)
        
        # Extract response and metadata
        if isinstance(result, dict):
            response = result.get('response', 'Let me help you learn!')
            
            # Show extracted data in response (for demonstration)
            if AI_AVAILABLE and result.get('extracted_data'):
                extracted = result['extracted_data']
                
                # Add extracted information to response if relevant
                if extracted.get('name'):
                    logger.info(f"Extracted name: {extracted['name']}")
                if extracted.get('letter'):
                    logger.info(f"Extracted letter: {extracted['letter']}")
                if extracted.get('intent'):
                    logger.info(f"Detected intent: {extracted['intent']}")
                if extracted.get('emotion'):
                    logger.info(f"Detected emotion: {extracted['emotion']}")
                
                # Add confidence indicator if AI is being used
                confidence = extracted.get('confidence', 0)
                if confidence > 0:
                    logger.info(f"AI Confidence: {confidence:.2%}")
        else:
            response = str(result)
        
        # Update memory with AI-enhanced turn
        session_memory.add_turn(message, response)
        
        # Add to history
        history = history or []
        history.append([message, response])
        
        return history
        
    except Exception as e:
        logger.error(f"Error in AI processing: {e}")
        history = history or []
        history.append([message, "I'm here to help you learn! What letter would you like to explore?"])
        return history

def show_extracted_data():
    """Show what data the AI has extracted from the conversation"""
    state = session_memory.get_derived_state_dict()
    
    extracted_info = f"""
    📊 **AI-Extracted Information:**
    
    **Child's Profile:**
    - Name: {state.get('child_name') or 'Not detected'}
    - Age Range: {state.get('age_range', 'Not detected')}
    - Current Letter: {state.get('current_letter', 'A')}
    
    **Learning Progress:**
    - Difficulty Level: {state.get('difficulty_level', 'easy')}
    - Streak Count: {state.get('streak_count', 0)}
    - Letters Completed: {', '.join(state.get('letters_completed', [])) or 'None yet'}
    - Letters Needing Practice: {', '.join(state.get('letters_struggled', [])) or 'None'}
    
    **Session Stats:**
    - Total Interactions: {state.get('total_interactions', 0)}
    - Session Duration: {state.get('session_duration', 'Just started')}
    
    **AI Model Status:**
    - AI Powered: {'✅ Yes' if AI_AVAILABLE else '❌ No (Using fallback)'}
    - Model Type: {getattr(agents, 'model_type', 'rule-based') if AI_AVAILABLE else 'rule-based'}
    """
    
    return extracted_info

def clear_chat():
    """Clear chat and reset session"""
    session_memory.reset()
    return None, "Session reset. Ready to start fresh!"

def get_ai_status():
    """Get current AI status"""
    if AI_AVAILABLE:
        model_type = getattr(agents, 'model_type', 'unknown')
        status = f"""
        🤖 **AI Status: Active**
        - Model: {model_type}
        - Data Extraction: Enabled
        - Intent Detection: Enabled
        - Personalization: Enabled
        """
    else:
        status = """
        🤖 **AI Status: Fallback Mode**
        - Using rule-based patterns
        - Basic data extraction
        - Limited personalization
        
        To enable full AI:
        1. Install AI dependencies: pip install langchain langchain-community openai
        2. Set up Ollama or OpenAI API key
        """
    return status

# Create AI-powered interface
with gr.Blocks(title="KidSafe Alphabet Tutor - AI Powered", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🎓 KidSafe Alphabet Tutor - AI-Powered Edition
    ### Learn the alphabet with Bubbly's intelligent AI! 🫧🤖
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                height=500,
                bubble_full_width=False,
                label="Chat with AI-Powered Bubbly"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Talk naturally! AI will understand: 'My name is Sarah and I'm 5 years old' or 'Show me the letter B'",
                    container=False,
                    scale=5,
                    label="Your message"
                )
                submit = gr.Button("Send", scale=1, variant="primary")
            
            with gr.Row():
                clear = gr.Button("🔄 Clear Chat", scale=1)
                
        with gr.Column(scale=1):
            gr.Markdown("### 📊 AI Intelligence Panel")
            
            ai_status = gr.Markdown(get_ai_status())
            
            extracted_data = gr.Markdown(
                show_extracted_data(),
                label="Extracted Data"
            )
            
            refresh_btn = gr.Button("🔄 Refresh Data", size="sm")
    
    gr.Markdown("""
    ---
    ### 💡 AI Capabilities:
    - **Natural Language Understanding**: Talk naturally, AI understands context
    - **Intent Detection**: Automatically detects what you want to do
    - **Entity Extraction**: Extracts names, ages, letters, emotions
    - **Adaptive Learning**: Personalizes based on performance
    - **Safety Filtering**: AI-powered content moderation
    
    ### 🗣️ Try saying:
    - "Hi, my name is Alex and I'm 4 years old"
    - "I want to learn about the letter D"
    - "That's too hard, can we try something easier?"
    - "I don't understand, can you explain again?"
    - "Next letter please"
    """)
    
    # Connect events
    msg.submit(
        lambda m, h: (chat_function(m, h), "", show_extracted_data()),
        [msg, chatbot],
        [chatbot, msg, extracted_data]
    )
    submit.click(
        lambda m, h: (chat_function(m, h), "", show_extracted_data()),
        [msg, chatbot],
        [chatbot, msg, extracted_data]
    )
    clear.click(
        clear_chat,
        None,
        [chatbot, extracted_data]
    )
    refresh_btn.click(
        lambda: show_extracted_data(),
        None,
        extracted_data
    )
    
    # Initial AI-powered greeting
    app.load(
        lambda: ([["", "Hi! I'm Bubbly, your AI-powered alphabet tutor! 🫧🤖 Tell me your name and age, and let's start learning! I can understand everything you say!"]], show_extracted_data()),
        None,
        [chatbot, extracted_data]
    )

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting KidSafe Alphabet Tutor - AI-Powered Version")
    print("="*60)
    
    if AI_AVAILABLE:
        print("✅ AI Models: Active")
        print("✅ Data Extraction: Enabled")
        print("✅ Natural Language: Enabled")
    else:
        print("⚠️  AI Models: Not available (install dependencies)")
        print("⚠️  Using rule-based fallback")
    
    print("\nOpen your browser to: http://localhost:7860")
    print("="*60 + "\n")
    
    # Launch with AI-optimized settings
    app.queue(max_size=20).launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_api=False,
        show_error=True
    )