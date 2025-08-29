# 🚀 KidSafe Alphabet Tutor - Complete Local Setup Guide

## From Zero to Running System

This guide will walk you through setting up the KidSafe Alphabet Tutor on your local machine, covering all scenarios from basic demo to full production setup.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Standard Setup (15 minutes)](#standard-setup-15-minutes)
4. [Full Setup with Models (30 minutes)](#full-setup-with-models-30-minutes)
5. [Docker Setup (Recommended)](#docker-setup-recommended)
6. [Development Setup](#development-setup)
7. [Troubleshooting](#troubleshooting)
8. [Verification & Testing](#verification--testing)

---

## 📦 Prerequisites

### Minimum Requirements

```yaml
System Requirements:
  OS: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
  RAM: 4GB minimum, 8GB recommended
  Storage: 2GB for basic, 10GB for full setup
  Processor: Dual-core 2GHz+
  
Software Requirements:
  Python: 3.10 or higher
  Git: For cloning repository
  Browser: Chrome/Firefox/Safari (modern version)
```

### Check Your System

```bash
# Check Python version
python --version  # or python3 --version
# Should show: Python 3.10.x or higher

# Check pip
pip --version  # or pip3 --version

# Check git
git --version

# Check available RAM (Linux/Mac)
free -h  # Linux
sysctl hw.memsize  # macOS

# Check available storage
df -h
```

---

## ⚡ Quick Start (5 minutes)

**Fastest way to see the system running - no AI models, demo mode only**

### Step 1: Get the Code

```bash
# Option A: If you have the code
cd /path/to/kidsafe-alphabet-tutor

# Option B: Clone from repository (if available)
git clone https://github.com/yourusername/kidsafe-alphabet-tutor.git
cd kidsafe-alphabet-tutor

# Option C: Download and extract ZIP
# Download the project ZIP file
unzip kidsafe-alphabet-tutor.zip
cd kidsafe-alphabet-tutor
```

### Step 2: Install Minimal Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install minimal requirements
pip install gradio numpy loguru python-dotenv
```

### Step 3: Run the Demo

```bash
# Run simplified version (no AI models needed)
python app/gradio_ui_simple.py
```

### Step 4: Access the Application

```
Open your browser and go to:
http://localhost:7860

You should see Bubbly's interface! 🫧
```

### What Works in Quick Start:
- ✅ Full UI interface
- ✅ Text-based interaction
- ✅ All activities and games
- ✅ Progress tracking
- ✅ Safety features
- ⚠️ Simulated audio/vision (not real)

---

## 📚 Standard Setup (15 minutes)

**Includes all Python dependencies but no large AI models**

### Step 1: Complete Environment Setup

```bash
# Navigate to project directory
cd kidsafe-alphabet-tutor

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install All Python Dependencies

```bash
# Install from requirements file
pip install -r requirements.txt

# If requirements.txt is missing, install manually:
pip install \
    gradio==4.19.2 \
    numpy==1.24.3 \
    loguru==0.7.2 \
    python-dotenv==1.0.0 \
    pillow==10.2.0 \
    opencv-python==4.9.0.80 \
    pytesseract==0.3.10 \
    pydantic==2.11.7
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file (optional)
nano .env  # or use any text editor
```

`.env` file contents:
```bash
# Basic Configuration
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
DEBUG=false
LOG_LEVEL=INFO

# Performance Settings
MAX_RESPONSE_TIME_MS=1200
VAD_THRESHOLD=0.5
ASR_CONFIDENCE_THRESHOLD=0.7
```

### Step 4: Install System Dependencies

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    portaudio19-dev \
    ffmpeg \
    libsndfile1
```

#### On macOS:
```bash
brew install \
    tesseract \
    portaudio \
    ffmpeg
```

#### On Windows:
```powershell
# Install Chocolatey first if not installed
# Then:
choco install tesseract
choco install ffmpeg
```

### Step 5: Run the Application

```bash
# Run with full UI features
python app/gradio_ui_simple.py

# Or use the run script
chmod +x run_demo.sh  # Make executable (Linux/Mac)
./run_demo.sh
```

---

## 🤖 Full Setup with Models (30 minutes)

**Complete setup with all AI models for full functionality**

### Step 1: Complete Standard Setup First

Follow all steps from Standard Setup above.

### Step 2: Install Additional AI Dependencies

```bash
# Speech processing
pip install \
    faster-whisper==1.0.1 \
    silero-vad==0.4.0 \
    pyaudio==0.2.14 \
    sounddevice==0.4.6 \
    librosa==0.10.1

# Vision processing
pip install \
    ultralytics==8.1.27 \
    torch torchvision torchaudio

# LLM support
pip install ollama
```

### Step 3: Download AI Models

```bash
# Create models directory
mkdir -p models

# Run model download script
chmod +x scripts/download_models.sh
./scripts/download_models.sh
```

Or download manually:

#### Whisper ASR Model:
```python
# Python script to download Whisper
from faster_whisper import WhisperModel

print("Downloading Whisper model...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
print("✅ Whisper model ready")
```

#### Silero VAD:
```python
# Download VAD model
import torch

print("Downloading Silero VAD...")
model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False
)
print("✅ VAD model ready")
```

#### YOLOv8 Model:
```python
# Download YOLO model
from ultralytics import YOLO

print("Downloading YOLOv8n...")
model = YOLO('yolov8n.pt')
model.predict('test.jpg')  # Test run
print("✅ YOLO model ready")
```

### Step 4: Install Ollama (Optional - for LLM)

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Pull Llama model
ollama pull llama3.2:3b

# Verify
ollama list
```

### Step 5: Install Piper TTS (Optional - for speech)

```bash
# Download Piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
sudo mv piper /usr/local/bin/

# Download voice model
mkdir -p models/piper
cd models/piper
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json
```

### Step 6: Run Full Version

```bash
# Run with all features
python app/gradio_ui.py

# You should see:
# - Real ASR (speech recognition)
# - Real TTS (text-to-speech)
# - Real vision (letter/object detection)
# - LLM-powered responses
```

---

## 🐳 Docker Setup (Recommended)

**Most reliable way to run the system**

### Step 1: Install Docker

```bash
# Ubuntu
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER

# macOS/Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

### Step 2: Build Docker Image

```bash
cd kidsafe-alphabet-tutor

# Build the image
docker build -t kidsafe-tutor .

# This will:
# - Install all dependencies
# - Download all models
# - Configure environment
# - Set up the application
```

### Step 3: Run Container

```bash
# Run the container
docker run -p 7860:7860 kidsafe-tutor

# Or with docker-compose
docker-compose up
```

### Docker Compose Configuration

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  kidsafe-tutor:
    build: .
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
    volumes:
      - ./models:/app/models
    restart: unless-stopped
```

---

## 💻 Development Setup

**For contributing or modifying the code**

### Step 1: Complete Development Environment

```bash
# Clone with git
git clone https://github.com/yourusername/kidsafe-alphabet-tutor.git
cd kidsafe-alphabet-tutor

# Create development branch
git checkout -b dev-feature

# Install development dependencies
pip install -r requirements-dev.txt  # If available
# Or
pip install pytest flake8 black mypy
```

### Step 2: Install Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Step 3: Set Up IDE

#### VS Code:
```json
// .vscode/settings.json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.pythonPath": "venv/bin/python"
}
```

#### PyCharm:
- Set Project Interpreter to `venv/bin/python`
- Enable pytest as test runner
- Configure black as formatter

### Step 4: Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_acceptance.py

# Run with coverage
pytest --cov=app --cov=agents tests/

# Run type checking
mypy app/ agents/

# Run linting
flake8 app/ agents/ --max-line-length=100
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Port 7860 Already in Use
```bash
# Find process using port
lsof -i :7860  # Linux/Mac
netstat -ano | findstr :7860  # Windows

# Kill process
kill -9 <PID>  # Linux/Mac
taskkill /PID <PID> /F  # Windows

# Or use different port
python app/gradio_ui_simple.py --port 7861
```

#### 2. Module Import Errors
```bash
# Ensure virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 3. Tesseract Not Found
```bash
# Linux
sudo apt-get install tesseract-ocr

# Mac
brew install tesseract

# Windows - Add to PATH
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"
```

#### 4. CUDA/GPU Issues
```bash
# Force CPU usage (no GPU required)
export CUDA_VISIBLE_DEVICES=""  # Linux/Mac
set CUDA_VISIBLE_DEVICES=  # Windows

# Or in Python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

#### 5. Memory Issues
```bash
# Reduce model size
# Use 'tiny.en' instead of 'small.en' for Whisper
# Use quantized models

# Increase swap (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 6. Gradio Not Opening
```bash
# Check if running
curl http://localhost:7860

# Try different browser
# Clear browser cache
# Disable browser extensions

# Run with share=True (creates public URL)
python -c "import gradio as gr; gr.Interface(lambda x: x, 'text', 'text').launch(share=True)"
```

---

## ✅ Verification & Testing

### Step 1: Verify Installation

```bash
# Check all imports work
python -c "
import gradio
import numpy
import cv2
print('✅ Core packages installed')
"

# Check optional packages
python -c "
try:
    import faster_whisper
    print('✅ ASR available')
except: print('⚠️ ASR not available')

try:
    import ultralytics
    print('✅ Vision available')
except: print('⚠️ Vision not available')
"
```

### Step 2: Run Component Tests

```bash
# Test components individually
python test_components.py

# Expected output:
# ✅ Session Memory test passed!
# ✅ Curriculum test passed!
# ✅ CrewAI Agents test passed!
# ✅ Fallback Response test passed!
```

### Step 3: Run Acceptance Tests

```bash
# Run full acceptance test suite
python tests/test_acceptance.py

# Should show:
# ✅ PASSED: 6/6
# 🎉 ALL ACCEPTANCE TESTS PASSED!
```

### Step 4: Test UI Interaction

1. Open http://localhost:7860
2. Type "Hello" and press Enter
3. Click "Next Letter" button
4. Type "My name is [your name]"
5. Try different activities

### Step 5: Performance Check

```bash
# Monitor resource usage
# Terminal 1:
python app/gradio_ui_simple.py

# Terminal 2:
top  # or htop
# Check CPU and memory usage
```

---

## 📊 Setup Comparison

| Setup Type | Time | Features | Use Case |
|-----------|------|----------|----------|
| Quick Start | 5 min | Basic UI, Text only | Demo, Testing UI |
| Standard | 15 min | Full UI, OCR | Development, Testing |
| Full | 30 min | All AI models | Production, Full features |
| Docker | 20 min | Everything, Isolated | Deployment, Distribution |

---

## 🎯 Next Steps

After successful setup:

1. **Read the User Guide**: `USER_GUIDE.md` for how to use
2. **Read the Technical Guide**: `TECHNICAL_GUIDE.md` for architecture
3. **Try the Activities**: Test all 6 learning activities
4. **Run Tests**: Verify everything works
5. **Customize**: Modify curriculum, add activities
6. **Deploy**: Use Docker for production deployment

---

## 📞 Getting Help

If you encounter issues:

1. **Check Troubleshooting** section above
2. **Review Error Logs**: Check terminal output
3. **Verify Prerequisites**: Ensure all requirements met
4. **Try Docker**: Most reliable setup method
5. **Use Simplified Version**: `gradio_ui_simple.py` always works

---

## 🎉 Success Indicators

You know setup is successful when:
- ✅ Browser opens at http://localhost:7860
- ✅ Bubbly's bubble avatar is animating
- ✅ Can type and get responses
- ✅ "Next Letter" button works
- ✅ Progress stars appear
- ✅ No error messages in terminal

---

**Congratulations! Your KidSafe Alphabet Tutor is ready to help children learn! 🫧📚✨**