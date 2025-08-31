#!/bin/bash

echo "=========================================="
echo "KidSafe Alphabet Tutor - AI Setup"
echo "=========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install base requirements
echo "Installing base requirements..."
pip install -r requirements.txt

# Ask user about AI features
echo ""
echo "=========================================="
echo "AI Model Selection"
echo "=========================================="
echo "Choose your AI backend:"
echo "1) OpenAI (requires API key)"
echo "2) Ollama (local, free)"
echo "3) Both"
echo "4) Skip AI setup"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "Installing OpenAI dependencies..."
        pip install openai langchain langchain-community tiktoken
        echo ""
        read -p "Enter your OpenAI API key (or press Enter to set later): " api_key
        if [ ! -z "$api_key" ]; then
            echo "OPENAI_API_KEY=$api_key" >> .env
            echo "API key saved to .env file"
        else
            echo "# Add your OpenAI API key here:" >> .env
            echo "# OPENAI_API_KEY=your_key_here" >> .env
        fi
        echo "AI_MODEL=openai" >> .env
        ;;
    2)
        echo "Installing Ollama dependencies..."
        pip install langchain langchain-community
        
        # Check if Ollama is installed
        if command_exists ollama; then
            echo "Ollama detected!"
            echo "Pulling recommended model (llama2)..."
            ollama pull llama2
        else
            echo ""
            echo "⚠️  Ollama not installed!"
            echo "Please install Ollama from: https://ollama.ai"
            echo "Then run: ollama pull llama2"
        fi
        echo "AI_MODEL=ollama" >> .env
        ;;
    3)
        echo "Installing all AI dependencies..."
        pip install -r requirements-ai.txt
        
        # Check for Ollama
        if command_exists ollama; then
            echo "Pulling Ollama model..."
            ollama pull llama2
        fi
        
        read -p "Enter OpenAI API key (optional): " api_key
        if [ ! -z "$api_key" ]; then
            echo "OPENAI_API_KEY=$api_key" >> .env
        fi
        echo "AI_MODEL=ollama" >> .env  # Default to free option
        ;;
    4)
        echo "Skipping AI setup. Using rule-based mode."
        echo "AI_MODEL=fallback" >> .env
        ;;
esac

echo ""
echo "=========================================="
echo "Testing Installation"
echo "=========================================="

# Test the installation
python3 -c "
import sys
sys.path.insert(0, '.')

print('Testing imports...')
try:
    import gradio
    print('✓ Gradio installed')
except:
    print('✗ Gradio not found')

try:
    from agents.crew_setup_ai import AlphabetTutorAI
    print('✓ AI agents available')
except:
    print('✗ AI agents not available (will use rule-based)')

try:
    import openai
    print('✓ OpenAI library installed')
except:
    print('  OpenAI not installed')

try:
    import langchain
    print('✓ LangChain installed')
except:
    print('  LangChain not installed')

print('\nSetup complete!')
"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the AI-enhanced version:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Run: python app/simple_app_ai.py"
echo ""
echo "The app will automatically use AI if available,"
echo "or fall back to rule-based mode if not."
echo ""