#!/bin/bash
# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the application
echo "Starting KidSafe Alphabet Tutor..."
python app/gradio_ui_simple.py
