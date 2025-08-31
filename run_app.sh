#!/bin/bash
# KidSafe Alphabet Tutor - Quick Run Script

# Check and install dependencies if needed
python3 -c "import gradio" 2>/dev/null || pip install -r requirements-minimal.txt

# Run the app
python3 app/gradio_ui_simple.py