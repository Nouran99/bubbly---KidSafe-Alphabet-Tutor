#!/bin/bash

# KidSafe Alphabet Tutor - Complete Setup Script
# Installs ALL components for the FULL AI-powered application

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     KidSafe Alphabet Tutor - FULL AI Setup                  ║"
echo "║     Speech + Vision + AI + Phonics                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo "📍 Detected OS: $OS"
echo ""

# Function to install system dependencies
install_system_deps() {
    echo "📦 Installing system dependencies..."
    
    if [[ "$OS" == "linux" ]]; then
        echo "→ Updating package list..."
        sudo apt-get update
        
        echo "→ Installing audio libraries..."
        sudo apt-get install -y portaudio19-dev python3-pyaudio
        sudo apt-get install -y espeak ffmpeg libespeak1
        
        echo "→ Installing Tesseract OCR..."
        sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
        
        echo "→ Installing webcam support..."
        sudo apt-get install -y v4l-utils
        
    elif [[ "$OS" == "mac" ]]; then
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew not found. Installing..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        
        echo "→ Installing audio libraries..."
        brew install portaudio
        
        echo "→ Installing Tesseract OCR..."
        brew install tesseract
        
        echo "→ Installing FFmpeg..."
        brew install ffmpeg
    fi
}

# Function to create virtual environment
setup_venv() {
    echo "🐍 Setting up Python virtual environment..."
    
    if [ -d "venv" ]; then
        echo "→ Virtual environment already exists"
    else
        echo "→ Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "→ Activating virtual environment..."
    source venv/bin/activate
    
    echo "→ Upgrading pip..."
    pip install --upgrade pip wheel setuptools
}

# Function to install Python dependencies
install_python_deps() {
    echo "📚 Installing Python dependencies..."
    
    # Core dependencies
    echo "→ Installing core dependencies..."
    pip install gradio==4.19.2
    pip install numpy==1.26.3
    pip install python-dotenv==1.0.0
    pip install loguru==0.7.2
    
    # Web framework dependencies
    echo "→ Installing web framework..."
    pip install fastapi==0.109.2
    pip install pydantic==2.5.3
    pip install uvicorn==0.27.1
    pip install httpx==0.26.0
    pip install aiofiles==23.2.1
    
    # AI/LLM dependencies
    echo "→ Installing AI components..."
    pip install langchain==0.1.0
    pip install langchain-community==0.0.10
    pip install openai==1.8.0
    pip install tiktoken==0.5.2
    pip install chromadb==0.4.22
    
    # Speech components
    echo "→ Installing speech recognition and TTS..."
    pip install SpeechRecognition==3.10.1
    pip install pyttsx3==2.90
    
    # Try to install PyAudio (may fail on some systems)
    pip install pyaudio || echo "⚠️  PyAudio installation failed (optional)"
    pip install sounddevice==0.4.6
    pip install soundfile==0.12.1
    
    # Vision components
    echo "→ Installing vision and OCR..."
    pip install opencv-python==4.9.0.80
    pip install pytesseract==0.3.10
    pip install Pillow==10.2.0
    
    # Machine Learning (optional - large)
    echo ""
    read -p "Install ML models for advanced vision (2GB+)? [y/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "→ Installing PyTorch and Transformers..."
        pip install torch torchvision transformers
    fi
}

# Function to setup Ollama
setup_ollama() {
    echo "🤖 Setting up Ollama for local AI..."
    
    read -p "Install Ollama for local AI models? [y/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OS" == "linux" ]]; then
            echo "→ Installing Ollama..."
            curl -fsSL https://ollama.ai/install.sh | sh
        elif [[ "$OS" == "mac" ]]; then
            echo "→ Installing Ollama via Homebrew..."
            brew install ollama
        else
            echo "⚠️  Please install Ollama manually from: https://ollama.ai/download"
            return
        fi
        
        echo "→ Starting Ollama service..."
        ollama serve > /dev/null 2>&1 &
        sleep 5
        
        echo "→ Pulling AI models..."
        ollama pull llama2 || echo "⚠️  Failed to pull llama2"
        ollama pull mistral || echo "⚠️  Failed to pull mistral"
        
        echo "✅ Ollama setup complete"
    fi
}

# Function to create environment file
create_env_file() {
    echo "⚙️  Creating configuration file..."
    
    if [ -f ".env" ]; then
        echo "→ .env file already exists, skipping..."
    else
        cat > .env << 'EOF'
# KidSafe Alphabet Tutor Configuration

# AI Configuration
USE_OLLAMA=true
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# Optional: OpenAI Configuration
# OPENAI_API_KEY=your_api_key_here
# USE_OLLAMA=false  # Set to false to use OpenAI

# Speech Configuration
TTS_ENABLED=true
ASR_ENABLED=true
TTS_VOICE=child_friendly
SPEECH_RATE=150
AUDIO_QUALITY=high

# Vision Configuration
VISION_ENABLED=true
WEBCAM_ENABLED=true
OCR_ENABLED=true
OBJECT_DETECTION=true

# Privacy & Safety (COPPA Compliance)
COPPA_COMPLIANT=true
SESSION_ONLY_MEMORY=true
NO_DATA_PERSISTENCE=true
CONTENT_FILTER=strict
MAX_SESSION_DURATION=30

# Assessment Settings
TRACK_PRONUNCIATION=true
TRACK_PROGRESS=true
SHOW_ASSESSMENT=true

# Debug Settings
DEBUG=false
LOG_LEVEL=INFO
EOF
        echo "✅ Configuration file created"
    fi
}

# Function to test installation
test_installation() {
    echo "🧪 Testing installation..."
    echo ""
    
    # Test Python imports
    python3 << EOF
import sys
print("Python version:", sys.version)

try:
    import gradio
    print("✅ Gradio: Installed")
except ImportError:
    print("❌ Gradio: Not installed")

try:
    import langchain
    print("✅ LangChain: Installed")
except ImportError:
    print("❌ LangChain: Not installed")

try:
    import speech_recognition
    print("✅ Speech Recognition: Installed")
except ImportError:
    print("❌ Speech Recognition: Not installed")

try:
    import pyttsx3
    print("✅ Text-to-Speech: Installed")
except ImportError:
    print("❌ Text-to-Speech: Not installed")

try:
    import cv2
    print("✅ OpenCV: Installed")
except ImportError:
    print("❌ OpenCV: Not installed")

try:
    import pytesseract
    print("✅ Tesseract OCR: Installed")
except ImportError:
    print("❌ Tesseract OCR: Not installed")
EOF
    
    # Test Ollama
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama: Installed"
        ollama list 2>/dev/null || echo "⚠️  Ollama not running"
    else
        echo "⚠️  Ollama: Not installed (optional)"
    fi
    
    # Test Tesseract
    if command -v tesseract &> /dev/null; then
        echo "✅ Tesseract CLI: Installed"
    else
        echo "⚠️  Tesseract CLI: Not installed"
    fi
}

# Main installation flow
main() {
    echo "Starting installation..."
    echo ""
    
    # Check Python version
    python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    if (( $(echo "$python_version < 3.8" | bc -l) )); then
        echo "❌ Python 3.8+ required (found $python_version)"
        exit 1
    fi
    echo "✅ Python $python_version detected"
    echo ""
    
    # Install system dependencies
    install_system_deps
    
    # Setup virtual environment
    setup_venv
    
    # Install Python dependencies
    install_python_deps
    
    # Setup Ollama
    setup_ollama
    
    # Create environment file
    create_env_file
    
    # Test installation
    echo ""
    test_installation
    
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Setup Complete! 🎉                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📝 Next Steps:"
    echo ""
    echo "1. Activate virtual environment (if not activated):"
    echo "   source venv/bin/activate"
    echo ""
    echo "2. Start the application:"
    echo "   python main.py"
    echo ""
    echo "3. Open your browser to:"
    echo "   http://localhost:7860"
    echo ""
    echo "📋 Available Features:"
    echo "  • 🎤 Speech Recognition (Microphone input)"
    echo "  • 🔊 Text-to-Speech (Voice responses)"
    echo "  • 📷 Vision/Webcam (Letter detection)"
    echo "  • 🤖 AI Intelligence (Natural language)"
    echo "  • 📊 Assessment Tracking"
    echo "  • 🔤 Phonics Focus"
    echo ""
    echo "For help, see README.md or docs/USER_GUIDE.md"
    echo ""
}

# Run main installation
main