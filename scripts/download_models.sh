#!/bin/bash
# Model Download Script for KidSafe Alphabet Tutor
# Downloads all required models for offline operation
# Author: Nouran Darwish

set -e

echo "📦 KidSafe Alphabet Tutor - Model Downloader"
echo "============================================"

# Create models directory
mkdir -p models

# Download Whisper model
echo "📥 Downloading Whisper ASR model..."
python3 -c "
from faster_whisper import WhisperModel
import os
os.makedirs('models/whisper', exist_ok=True)
model = WhisperModel('small.en', device='cpu', compute_type='int8', download_root='models/whisper')
print('✅ Whisper model downloaded')
" || echo "⚠️ Whisper download failed (continuing...)"

# Download Silero VAD
echo "📥 Downloading Silero VAD model..."
python3 -c "
import torch
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
print('✅ Silero VAD downloaded')
" || echo "⚠️ Silero VAD download failed (continuing...)"

# Download YOLOv8n
echo "📥 Downloading YOLOv8n model..."
python3 -c "
from ultralytics import YOLO
import shutil
model = YOLO('yolov8n.pt')
# Copy to models directory
shutil.copy('yolov8n.pt', 'models/yolov8n.pt') if os.path.exists('yolov8n.pt') else None
print('✅ YOLOv8n model downloaded')
" || echo "⚠️ YOLOv8n download failed (continuing...)"

# Download Piper TTS models (if available)
echo "📥 Checking Piper TTS..."
if command -v piper &> /dev/null; then
    echo "✅ Piper TTS is installed"
    # Download voice model
    mkdir -p models/piper
    # Note: Actual voice download would require specific URLs
    echo "ℹ️ Please download Piper voice models manually from:"
    echo "   https://github.com/rhasspy/piper/releases"
else
    echo "⚠️ Piper TTS not installed. Install with: pip install piper-tts"
fi

# Setup Ollama
echo "📥 Setting up Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    echo "📥 Pulling Llama 3.2 3B model..."
    ollama pull llama3.2:3b || echo "⚠️ Ollama model pull failed"
else
    echo "⚠️ Ollama not installed. Please install from: https://ollama.ai"
fi

echo ""
echo "============================================"
echo "✅ Model download complete!"
echo "ℹ️ Some models may need manual installation"
echo "============================================"