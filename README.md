# 🎓 KidSafe Alphabet Tutor - Full AI-Powered System

**Complete Speech + Vision + AI Educational System for Teaching Children the Alphabet**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![COPPA Compliant](https://img.shields.io/badge/COPPA-Compliant-success.svg)](https://www.ftc.gov/coppa)

## 🌟 Overview

A comprehensive, AI-powered alphabet learning system that teaches children aged 3-7 through:
- **Speech-to-Speech Interaction**: Children speak, AI understands and responds with voice
- **Vision Recognition**: Webcam detects letters and objects in real-time
- **Phonics Focus**: Emphasis on letter sounds and pronunciation
- **AI Intelligence**: Natural language understanding and adaptive learning
- **Complete Assessment**: Track progress, pronunciation, and learning patterns

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor.git
cd bubbly---KidSafe-Alphabet-Tutor

# 2. Run setup (installs everything)
./setup.sh

# 3. Start the application
python main.py

# 4. Open browser to http://localhost:7860
```

## ✨ Key Features

### 🎤 Speech Recognition & TTS
- Real-time speech recognition
- Child-friendly text-to-speech voices
- Pronunciation analysis and feedback
- Natural conversation flow

### 📷 Vision & Object Detection
- Webcam letter recognition
- Object detection for alphabet association
- OCR for printed text
- Real-time visual feedback

### 🧠 AI-Powered Intelligence
- Natural language understanding
- Context-aware responses
- Emotion detection
- Adaptive difficulty adjustment

### 📊 Complete Assessment System
- Pronunciation scoring
- Progress tracking
- Letter mastery evaluation
- Session analytics

### 🔒 Privacy & Safety
- 100% COPPA compliant
- No data collection or storage
- Session-only memory (3-turn buffer)
- Content filtering for child safety

## 📋 System Requirements

### Minimum Requirements
- Python 3.8+
- 4GB RAM
- Webcam (for vision features)
- Microphone (for speech features)
- Internet connection (initial setup)

### Recommended
- Python 3.10+
- 8GB RAM
- HD Webcam
- Good quality microphone
- GPU (for faster AI processing)

## 🛠️ Installation

### Automated Setup (Recommended)
```bash
./setup.sh
```
This script will:
- Install system dependencies
- Create virtual environment
- Install all Python packages
- Setup AI models (optional)
- Configure environment

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama (for local AI)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# Create .env file
cp .env.example .env
```

## 🎯 Usage

### Starting the Application
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
python main.py
```

### Using the Interface

1. **Speech Input** 🎤
   - Click microphone button
   - Speak clearly
   - Say letters or words
   - Get instant feedback

2. **Vision Input** 📷
   - Allow webcam access
   - Show letters or objects
   - Get visual recognition
   - Learn through sight

3. **Text Input** ⌨️
   - Type messages
   - Ask questions
   - Request specific letters
   - Natural conversation

### Example Interactions

```
Child: "Hi, my name is Sarah and I'm 5 years old"
AI: "Hi Sarah! It's wonderful to meet you! I'm Bubbly, and I'm here to help you learn the alphabet! You're 5? That's the perfect age for learning letters! Should we start with the letter A?"

Child: [Shows letter B to camera]
AI: "Great job! I can see the letter B! B makes the 'buh' sound, like in Ball and Bear. Can you say 'B' for me?"

Child: "Bee"
AI: "Excellent pronunciation, Sarah! You said 'B' perfectly! ⭐ Let's try a word with B - can you say 'Ball'?"
```

## 🔧 Configuration

### Environment Variables (.env)
```env
# AI Configuration
USE_OLLAMA=true              # Use local AI (recommended)
OLLAMA_MODEL=llama2          # AI model choice
# OPENAI_API_KEY=sk-...      # Optional: Use OpenAI instead

# Features
TTS_ENABLED=true             # Text-to-speech
ASR_ENABLED=true             # Speech recognition
VISION_ENABLED=true          # Webcam/vision
WEBCAM_ENABLED=true          # Enable webcam

# Privacy
COPPA_COMPLIANT=true         # Child privacy protection
SESSION_ONLY_MEMORY=true     # No data persistence
NO_DATA_PERSISTENCE=true     # Zero storage
```

## 📁 Project Structure

```
kidsafe-alphabet-tutor/
├── main.py                  # Main entry point
├── setup.sh                 # Installation script
├── requirements.txt         # Python dependencies
├── .env                     # Configuration (create from .env.example)
├── app/
│   ├── full_ai_app.py      # Complete AI application
│   ├── state.py            # Session memory management
│   └── curriculum.json     # Alphabet curriculum data
├── agents/
│   └── crew_ai_powered.py  # AI agent system
├── docs/
│   ├── USER_GUIDE.md       # For parents/teachers
│   ├── TECHNICAL_GUIDE.md  # For developers
│   └── AI_GUIDE.md         # AI configuration
└── README.md               # This file
```

## 🧪 Testing

### System Check
```bash
# Test all components
python -c "from app.full_ai_app import FullAIAlphabetTutor; print('✅ System OK')"

# Check individual components
python -m pytest tests/  # If tests are available
```

### Component Status
Run the app and check the status panel:
- ✅ AI: Active/Fallback
- ✅ Speech: Ready/Unavailable
- ✅ Vision: Ready/Unavailable
- ✅ TTS: Active/Unavailable

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **No microphone detected** | Check browser permissions, allow microphone access |
| **Webcam not working** | Allow camera access in browser settings |
| **AI not responding** | Ensure Ollama is running: `ollama serve` |
| **Slow responses** | Use smaller AI model: `ollama pull phi` |
| **Installation fails** | Run `./setup.sh` with sudo for system packages |

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
export LOG_LEVEL=DEBUG
python main.py
```

## 📊 Assessment Metrics

The system tracks:
- **Pronunciation Accuracy**: 0-100% score
- **Letter Recognition**: Visual and auditory
- **Progress Tracking**: Letters mastered
- **Interaction Quality**: Engagement level
- **Learning Pace**: Adaptive difficulty

## 🤝 Contributing

We welcome contributions! Areas of interest:
- Additional language support
- More curriculum content
- Enhanced vision models
- Voice variety
- Educational games

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 👥 Credits

**Author**: Nouran Darwish  
**Role**: Generative AI Engineer  
**Project**: CNTXT.AI Assessment  

## 🔗 Links

- [Repository](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor)
- [Issues](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor/issues)
- [Documentation](docs/)

## ✅ Status

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2025-08-31  

---

*Built with ❤️ for children's education and safety*