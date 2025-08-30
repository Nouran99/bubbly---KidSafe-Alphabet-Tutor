# Setup Instructions - KidSafe Alphabet Tutor

## 🚀 Quick Start (Fastest - 1 minute)

### One-Command Setup & Run
```bash
# Linux/Mac
chmod +x run_app.sh && ./run_app.sh

# Or directly with Python
pip install gradio numpy loguru python-dotenv && python app/gradio_ui_simple.py
```

## 📦 Installation Options

### Option 1: Automatic Full Setup (Recommended)

Choose the setup script for your platform:

#### **Linux/Mac:**
```bash
chmod +x setup_full.sh
./setup_full.sh
```

#### **Windows:**
```cmd
setup_full.bat
```

#### **Universal (All Platforms):**
```bash
python setup_full.py
```

The setup script will:
1. Check Python version (3.10+ required)
2. Create virtual environment
3. Install all dependencies
4. Setup curriculum data
5. Configure environment
6. Run tests
7. Create startup scripts
8. Optionally start the app

### Option 2: Quick Manual Setup

```bash
# 1. Install minimal requirements
pip install gradio numpy loguru python-dotenv

# 2. Run the app
python app/gradio_ui_simple.py
```

### Option 3: Standard Setup with Virtual Environment

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-standard.txt

# 4. Run the app
python app/gradio_ui_simple.py
```

## 📋 Setup Scripts Overview

| Script | Platform | Features | Time |
|--------|----------|----------|------|
| `run_app.sh` | Linux/Mac | Minimal, auto-install & run | 1 min |
| `quick_setup.sh` | Linux/Mac | Basic setup with prompts | 2 min |
| `setup_full.sh` | Linux/Mac | Complete setup, all options | 5-15 min |
| `setup_full.bat` | Windows | Complete setup, all options | 5-15 min |
| `setup_full.py` | All | Universal, works everywhere | 5-15 min |

## 🎯 Installation Levels

### Minimal (Core Only)
```bash
pip install -r requirements-minimal.txt
# Or: pip install gradio numpy loguru python-dotenv
```
- Size: ~150MB
- Time: 1-2 minutes
- Features: Basic UI and agent system

### Standard (Recommended)
```bash
pip install -r requirements-standard.txt
```
- Size: ~300MB
- Time: 3-5 minutes
- Features: Full app with content moderation

### Full (All Features)
```bash
pip install -r requirements-full.txt
```
- Size: ~1GB
- Time: 10-15 minutes
- Features: AI capabilities (vision, speech)

## 🔧 System Requirements

### Required:
- Python 3.10 or higher
- 2GB RAM minimum
- 500MB disk space (minimal) to 2GB (full)

### Optional (for AI features):
- **Linux/Mac**: `ffmpeg`, `tesseract-ocr`
- **Windows**: FFmpeg, Tesseract OCR

Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg tesseract-ocr

# macOS
brew install ffmpeg tesseract

# Windows
# Download from official websites
```

## ✅ Verify Installation

After setup, verify everything works:

```bash
# Run the test script
python test_setup.py

# Or manually check
python -c "import gradio, numpy, loguru; print('✓ Ready!')"
```

## 🚀 Starting the Application

After setup, you can start the app using:

### Using Created Scripts:
```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

### Direct Python:
```bash
python app/gradio_ui_simple.py
```

### With Virtual Environment:
```bash
# Activate venv first
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Then run
python app/gradio_ui_simple.py
```

## 🌐 Accessing the Application

Once started, open your browser to:
- **Local**: http://localhost:7860
- **Network**: http://[your-ip]:7860

## 🆘 Troubleshooting

### Common Issues:

1. **"Python not found"**
   - Install Python 3.10+: https://www.python.org/downloads/

2. **"Module not found"**
   - Run: `pip install -r requirements-minimal.txt`

3. **"Port already in use"**
   - Change port in `.env` file or kill process using port 7860

4. **"Curriculum error"**
   - Run: `python test_setup.py` to recreate curriculum

### Get Help:
- Check `TROUBLESHOOTING.md` for detailed solutions
- Run `python diagnose.py` for system diagnosis
- Test with `python test_setup.py`

## 📊 Setup Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| `run_app.sh` | Fastest, simple | No venv, basic only | Quick demos |
| `quick_setup.sh` | Fast, automated | Linux/Mac only | Quick setup |
| `setup_full.py` | Universal, complete | Takes longer | Production |
| Manual | Full control | More steps | Developers |

## 🎉 Success!

When setup is complete, you'll see:
```
✅ Setup Complete!
Starting KidSafe Alphabet Tutor...
Running on local URL: http://localhost:7860
```

The app is ready when you can access http://localhost:7860 in your browser!

## 💡 Tips

- Use virtual environment for clean installation
- Start with minimal, upgrade if needed
- Check `test_setup.py` after installation
- Keep `.env` file for configuration
- Use `run.sh` or `run.bat` for easy startup

---

For additional help, see:
- `README.md` - Project overview
- `TROUBLESHOOTING.md` - Problem solutions
- `REQUIREMENTS_INFO.md` - Dependency details