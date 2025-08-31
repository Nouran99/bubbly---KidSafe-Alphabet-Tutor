# Installation Guide

## Quick Start (2 minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor.git
cd bubbly---KidSafe-Alphabet-Tutor
```

### 2. Install Dependencies
```bash
pip install -r requirements-minimal.txt
```

### 3. Run the Application
```bash
python app/gradio_ui_simple.py
```

Open your browser to: http://localhost:7860

## Installation Options

### Option A: Minimal (Recommended for Quick Start)
```bash
pip install -r requirements-minimal.txt
```
- Size: ~150MB
- Includes: Core functionality only

### Option B: Standard (Recommended for Full Features)
```bash
pip install -r requirements-standard.txt
```
- Size: ~300MB
- Includes: All app features

### Option C: Full (For AI Features)
```bash
pip install -r requirements-full.txt
```
- Size: ~1GB
- Includes: Vision and speech capabilities

## Using Virtual Environment (Recommended)

### Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements-minimal.txt
python app\gradio_ui_simple.py
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-minimal.txt
python app/gradio_ui_simple.py
```

## Alternative Start Methods

### Using the Startup Script:
```bash
python start_app.py
```

### Using the Run Script (Linux/Mac):
```bash
chmod +x run_app.sh
./run_app.sh
```

### Using the Setup Script:
```bash
python setup_full.py  # Interactive setup with options
```

## System Requirements

- Python 3.10 or higher
- 2GB RAM minimum
- 500MB disk space

## Troubleshooting

### Port Already in Use
Change the port in `.env` file:
```
GRADIO_SERVER_PORT=7861
```

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements-minimal.txt
```

### Python Version Error
Ensure you have Python 3.10+:
```bash
python --version
```

## Testing the Installation

Run the test script:
```bash
python test_setup.py
```

Or test manually:
```bash
python -c "import gradio, numpy, loguru; print('✓ Dependencies OK')"
```

## Success!

When the app starts successfully, you'll see:
```
Running on local URL: http://0.0.0.0:7860
```

Open http://localhost:7860 in your browser to use the application.