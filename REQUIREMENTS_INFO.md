# Requirements Information

## Overview
The KidSafe Alphabet Tutor uses a tiered requirements system to accommodate different use cases and deployment scenarios.

## Installation Levels

### 1. Minimal Installation (`requirements-minimal.txt`)
**Purpose**: Quick demo and basic functionality
**Install Time**: ~2 minutes
**Size**: ~150MB

```bash
pip install -r requirements-minimal.txt
```

**Includes**:
- `gradio` - Web UI framework
- `numpy` - Numerical operations
- `loguru` - Logging system

**Use When**:
- Testing the basic UI
- Running quick demos
- Limited system resources
- No AI features needed

### 2. Standard Installation (`requirements-standard.txt`)
**Purpose**: Full application without heavy AI dependencies
**Install Time**: ~5 minutes
**Size**: ~300MB

```bash
pip install -r requirements-standard.txt
```

**Includes everything from Minimal plus**:
- `python-dotenv` - Environment configuration
- `Pillow` - Image processing
- `better-profanity` - Content moderation
- `aiofiles` - Async file operations
- `pytest` - Testing framework

**Use When**:
- Production deployment without AI features
- Development and testing
- Educational settings with basic requirements

### 3. Full Installation (`requirements-full.txt`)
**Purpose**: Complete system with all AI capabilities
**Install Time**: ~15 minutes
**Size**: ~1GB+

```bash
pip install -r requirements-full.txt
```

**Includes everything from Standard plus**:
- `opencv-python` - Computer vision
- `pytesseract` - OCR capabilities
- `ultralytics` - Object detection (YOLO)
- `sounddevice` - Audio recording
- `scipy` - Scientific computing
- `librosa` - Audio analysis
- `webrtcvad` - Voice activity detection
- `ollama` - Local LLM support

**Use When**:
- Need speech recognition
- Need vision capabilities
- Want local LLM integration
- Full feature deployment

## Compatibility Notes

### Python Version
- **Minimum**: Python 3.10
- **Recommended**: Python 3.11
- **Maximum Tested**: Python 3.12

### NumPy Compatibility
- Requirements use `numpy>=1.24.0` for maximum compatibility
- Works with both NumPy 1.x and 2.x
- If conflicts arise, pin to `numpy==1.26.4`

### Platform Support
- **Linux**: Full support (all features)
- **macOS**: Full support (all features)
- **Windows**: Full support (may need Visual C++ redistributables for some packages)

## System Dependencies

### For Full Installation
Some features require system-level dependencies:

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr ffmpeg
```

**macOS**:
```bash
brew install tesseract ffmpeg
```

**Windows**:
- Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Install FFmpeg from: https://ffmpeg.org/download.html

## Docker Alternative
For consistent environments across all platforms:
```bash
docker build -t kidsafe-tutor .
docker run -p 7860:7860 kidsafe-tutor
```

## Troubleshooting

### Common Issues

1. **Import Error for gradio**
   - Solution: `pip install --upgrade gradio`

2. **NumPy version conflicts**
   - Solution: `pip install numpy==1.26.4`

3. **Missing system dependencies**
   - Run: `python diagnose.py` to check

4. **Slow installation**
   - Use minimal or standard installation first
   - Add AI features incrementally as needed

### Verification
After installation, verify with:
```bash
python final_test.py
```

## Package Sizes (Approximate)

| Package | Download | Installed |
|---------|----------|-----------|
| gradio | 10MB | 50MB |
| numpy | 15MB | 65MB |
| opencv-python | 30MB | 150MB |
| ultralytics | 40MB | 200MB |
| torch (CPU) | 140MB | 700MB |

## Upgrade Path

Start with minimal, upgrade as needed:
```bash
# Start minimal
pip install -r requirements-minimal.txt

# Upgrade to standard
pip install -r requirements-standard.txt

# Upgrade to full
pip install -r requirements-full.txt
```

## Production Recommendations

1. **For Cloud Deployment**: Use `requirements-standard.txt`
2. **For Edge Devices**: Use `requirements-minimal.txt`
3. **For Development**: Use `requirements-full.txt`
4. **For Docker**: All dependencies included in Dockerfile

## Security Notes

- All packages are from PyPI official repository
- No packages with known critical vulnerabilities (as of 2025)
- Regular updates recommended via `pip list --outdated`

---

For questions or issues, run `python diagnose.py` for system diagnostics.