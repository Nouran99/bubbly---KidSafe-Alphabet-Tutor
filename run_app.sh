#!/bin/bash
# KidSafe Alphabet Tutor - One-Command Setup & Run

# Quick dependency check and install
python3 -c "import gradio" 2>/dev/null || pip install --quiet --user gradio numpy loguru python-dotenv

# Run the app
python3 app/gradio_ui_simple.py