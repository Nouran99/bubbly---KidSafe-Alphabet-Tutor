#!/bin/bash
# Quick start script for KidSafe Alphabet Tutor Demo
# Author: Nouran Darwish

echo "🫧 Starting Bubbly - KidSafe Alphabet Tutor 🫧"
echo "============================================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "✓ Python version: $python_version"

# Install minimal required packages if not present
echo "📦 Checking dependencies..."
pip list | grep -q "gradio" || pip install gradio
pip list | grep -q "numpy" || pip install numpy

echo ""
echo "🚀 Starting application..."
echo "============================================"
echo "📱 Open your browser at: http://localhost:7860"
echo "💡 Try saying: 'Hello', 'My name is...', 'Teach me A'"
echo "🛑 Press Ctrl+C to stop the application"
echo "============================================"
echo ""

# Run the simplified demo version
python3 app/gradio_ui_simple.py