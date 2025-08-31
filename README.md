# 🎓 KidSafe Alphabet Tutor - "Bubbly" 🫧

An AI-powered educational system that teaches the alphabet to children aged 3-7 with complete COPPA compliance, zero data retention, and engaging interactive learning.

## 🌟 Key Features

### Safety & Privacy First
- ✅ **100% COPPA Compliant** - No personal data collection
- ✅ **Session-Only Memory** - Zero data persistence
- ✅ **No Login Required** - Completely anonymous usage
- ✅ **Content Filtering** - Child-safe responses only

### Educational Features
- 🔤 **Complete Alphabet Coverage** - All 26 letters with phonetics
- 🎯 **Adaptive Learning** - Adjusts difficulty based on performance
- 🎮 **Interactive Activities** - Games, matching, and exercises
- 🗣️ **Voice Support** - Speech recognition and text-to-speech
- 🏆 **Progress Tracking** - Session-based achievement system

### Technical Highlights
- 🤖 **Multi-Agent System** - Specialized AI agents for different tasks
- 🚀 **Simple & Full Modes** - Choose between quick start or full features
- 💻 **Cross-Platform** - Works on Windows, Mac, and Linux
- 🔧 **Easy Setup** - One-command installation

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum
- Internet connection for initial setup

### Quick Start (Simple Mode)
```bash
# 1. Clone the repository
git clone https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor.git
cd bubbly---KidSafe-Alphabet-Tutor

# 2. Run setup (simple mode - default)
python setup.py --simple

# 3. Start the application
python app/simple_app.py

# 4. Open browser to http://localhost:7860
```

### Full Installation (All Features)
```bash
# Run setup with full features
python setup.py --full

# Start with full features (if available)
python app/main.py
```

### Windows Users - Special Fix
If you encounter ASGI or Pydantic errors on Windows:
```bash
python setup.py --fix-windows
```

## 🚀 Usage

### Starting the Application
1. **Activate virtual environment** (if created):
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

2. **Run the application**:
   ```bash
   python app/simple_app.py
   ```

3. **Open your browser** to: `http://localhost:7860`

### Interacting with Bubbly
- Say "Hello" to start
- Ask "Teach me the letter A"
- Say "Next letter" to progress
- Ask "What comes after B?"
- Request activities: "Let's play a game"

## 📁 Project Structure

```
kidsafe-alphabet-tutor/
├── app/                      # Main application code
│   ├── simple_app.py        # Simple mode entry point
│   ├── state.py             # Session memory management
│   └── curriculum.json      # Letter curriculum data
├── agents/                   # Multi-agent system
│   └── crew_setup_simple.py # Agent orchestration
├── docs/                     # Documentation
├── requirements.txt          # Python dependencies
├── setup.py                  # Unified setup script
└── README.md                # This file
```

## 🧪 Testing & Verification

### Check Compatibility
```bash
python check_compatibility.py
```

### Run Tests
```bash
python diagnose.py          # System diagnostics
python final_test.py        # Acceptance tests
```

## 🔧 Configuration

### Environment Variables (.env)
The setup script creates a `.env` file with default settings:
```env
DEBUG=False
ENVIRONMENT=development
COPPA_COMPLIANT=true
SESSION_ONLY_MEMORY=true
NO_DATA_PERSISTENCE=true
```

### Customization Options
- **Age Range**: 3-5 (younger) or 6-8 (older)
- **Difficulty**: Easy, Medium, Hard
- **Features**: Vision, TTS, ASR can be toggled

## 🛠️ Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   fuser -k 7860/tcp  # Linux/Mac
   # Or change port in simple_app.py
   ```

2. **Import Errors**
   ```bash
   python setup.py --simple  # Reinstall dependencies
   ```

3. **Windows ASGI Error**
   ```bash
   python setup.py --fix-windows
   ```

4. **Gradio Not Loading**
   - Clear browser cache
   - Try different browser
   - Check firewall settings

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md) - For parents and teachers
- [Technical Guide](docs/TECHNICAL_GUIDE.md) - For developers
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues
- [Compatibility Report](docs/COMPATIBILITY_REPORT.md) - System compatibility

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is part of an educational initiative. All rights reserved.

## 👥 Team

- **Author**: Nouran Darwish
- **Role**: Generative AI Engineer
- **Organization**: CNTXT.AI Assessment Project

## 🔗 Links

- **GitHub**: [https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor)
- **Issues**: [Report bugs or request features](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor/issues)

## ✅ Project Status

- **Development**: ✅ Complete
- **Testing**: ✅ All tests passing
- **Documentation**: ✅ Complete
- **Deployment**: ✅ Ready
- **Windows Compatibility**: ✅ Fixed

---

*Last Updated: 2025-08-31*