# 🚀 KidSafe Alphabet Tutor - Quick Start Guide

## Get Running in 2 Minutes!

### Option 1: Fastest Setup (Linux/Mac)
```bash
# 1. Navigate to project
cd kidsafe-alphabet-tutor

# 2. Run automated installer
./install.sh
# Choose option 1 (Quick) when prompted

# 3. Start the application
./start.sh
```

### Option 2: Fastest Setup (Windows)
```batch
# 1. Navigate to project
cd kidsafe-alphabet-tutor

# 2. Run automated installer
install.bat
REM Choose option 1 (Quick) when prompted

# 3. Start the application
start.bat
```

### Option 3: Manual Quick Setup (All Platforms)
```bash
# 1. Navigate to project
cd kidsafe-alphabet-tutor

# 2. Install minimal dependencies
pip install gradio numpy loguru python-dotenv

# 3. Run the application
python app/gradio_ui_simple.py

# 4. Open browser at http://localhost:7860
```

---

## 🔍 Having Issues?

### Run Diagnostics
```bash
python diagnose.py
```

This will check:
- ✅ Python version
- ✅ Required packages
- ✅ Project files
- ✅ Available ports
- ✅ System dependencies

### Common Fixes

#### "Module not found" Error
```bash
pip install gradio numpy loguru python-dotenv
```

#### "Port 7860 already in use"
```bash
# Linux/Mac
lsof -i :7860
kill -9 <PID>

# Windows
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

#### "Python not found"
- Install Python 3.10+ from https://python.org
- Make sure to check "Add Python to PATH" during installation

---

## 📖 Next Steps

1. **Try the Demo**
   - Type "Hello" in the text box
   - Click "Next Letter" to start learning
   - Type "My name is [your name]"

2. **Read the Guides**
   - `USER_GUIDE.md` - For parents and teachers
   - `TECHNICAL_GUIDE.md` - For developers
   - `SETUP_GUIDE.md` - For complete setup options

3. **Explore Features**
   - Try all 6 activities
   - Check progress tracking
   - Test parental controls (Math: 3+4=7)

---

## 🎯 What's Working Now?

| Feature | Status | Notes |
|---------|--------|-------|
| UI Interface | ✅ Working | Full Gradio interface |
| Text Interaction | ✅ Working | Type and get responses |
| Activities/Games | ✅ Working | All 6 activities functional |
| Progress Tracking | ✅ Working | Stars and badges |
| Safety Features | ✅ Working | Content filtering active |
| Audio (Demo) | ⚠️ Simulated | Real ASR/TTS need models |
| Vision (Demo) | ⚠️ Simulated | Real detection needs models |

---

## 💡 Tips

- **For Developers**: Use `diagnose.py` to check your setup
- **For Parents**: Start with USER_GUIDE.md
- **For Quick Demo**: Just run `python app/gradio_ui_simple.py`
- **For Full Features**: Follow SETUP_GUIDE.md for model installation

---

**Ready to teach the alphabet with Bubbly! 🫧📚✨**