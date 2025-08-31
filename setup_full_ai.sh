#!/bin/bash

# Full AI-Powered Setup Script
# Installs everything needed for Speech, Vision, and AI

echo "=========================================="
echo "KidSafe Alphabet Tutor - FULL AI Setup"
echo "Installing Speech, Vision, and AI components"
echo "=========================================="

# Update pip
echo "→ Updating pip..."
pip install --upgrade pip

# Install core dependencies
echo "→ Installing core dependencies..."
pip install -r requirements.txt

# Install AI/LLM components
echo "→ Installing AI components..."
pip install langchain==0.1.0 langchain-community==0.0.10 openai==1.8.0

# Install speech components
echo "→ Installing speech recognition and TTS..."
pip install SpeechRecognition==3.10.1 pyttsx3==2.90

# For Linux/Mac - install audio dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "→ Installing Linux audio dependencies..."
    sudo apt-get update
    sudo apt-get install -y portaudio19-dev python3-pyaudio
    sudo apt-get install -y espeak ffmpeg libespeak1
    sudo apt-get install -y tesseract-ocr
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "→ Installing Mac audio dependencies..."
    brew install portaudio
    brew install tesseract
fi

pip install pyaudio sounddevice soundfile

# Install vision components
echo "→ Installing vision and OCR..."
pip install opencv-python==4.9.0.80 pytesseract==0.3.10 Pillow==10.2.0

# Install ML models (optional - large downloads)
read -p "Install ML models for vision (large download, ~2GB)? (y/n): " install_ml
if [[ $install_ml == "y" ]]; then
    echo "→ Installing PyTorch and transformers..."
    pip install torch torchvision transformers
fi

# Setup Ollama for local AI
read -p "Install Ollama for local AI models? (y/n): " install_ollama
if [[ $install_ollama == "y" ]]; then
    echo "→ Installing Ollama..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ollama
    fi
    
    echo "→ Starting Ollama service..."
    ollama serve &
    sleep 5
    
    echo "→ Pulling AI models..."
    ollama pull llama2
    ollama pull mistral
fi

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "→ Creating .env file..."
    cat > .env << EOF
# AI Configuration
USE_OLLAMA=true
OLLAMA_MODEL=llama2

# Optional OpenAI
# OPENAI_API_KEY=your_key_here

# Speech Settings
TTS_ENABLED=true
ASR_ENABLED=true
TTS_VOICE=child_friendly
SPEECH_RATE=150

# Vision Settings
VISION_ENABLED=true
WEBCAM_ENABLED=true
OCR_ENABLED=true

# Privacy Settings
COPPA_COMPLIANT=true
SESSION_ONLY_MEMORY=true
NO_DATA_PERSISTENCE=true
EOF
fi

# Test installations
echo ""
echo "=========================================="
echo "Testing installations..."
echo "=========================================="

python -c "import gradio; print('✓ Gradio installed')" 2>/dev/null || echo "✗ Gradio missing"
python -c "import langchain; print('✓ LangChain installed')" 2>/dev/null || echo "✗ LangChain missing"
python -c "import speech_recognition; print('✓ Speech Recognition installed')" 2>/dev/null || echo "✗ Speech Recognition missing"
python -c "import pyttsx3; print('✓ TTS installed')" 2>/dev/null || echo "✗ TTS missing"
python -c "import cv2; print('✓ OpenCV installed')" 2>/dev/null || echo "✗ OpenCV missing"
python -c "import pytesseract; print('✓ Tesseract installed')" 2>/dev/null || echo "✗ Tesseract missing"

# Check Ollama
ollama list 2>/dev/null && echo "✓ Ollama running" || echo "✗ Ollama not running"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the FULL AI-powered app:"
echo "  python app/full_ai_app.py"
echo ""
echo "Features available:"
echo "  • Speech Recognition (Microphone input)"
echo "  • Text-to-Speech (Voice responses)"
echo "  • Vision/Webcam (Letter & object detection)"
echo "  • AI Intelligence (Natural language understanding)"
echo "  • Phonics Focus (Pronunciation feedback)"
echo ""
echo "Open your browser to: http://localhost:7860"
echo "=========================================="