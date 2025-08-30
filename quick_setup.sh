#!/bin/bash
# KidSafe Alphabet Tutor - Quick One-Command Setup Script

echo "========================================"
echo "KidSafe Alphabet Tutor - Quick Setup"
echo "========================================"
echo ""

# Check Python version
python3 --version >/dev/null 2>&1 || { echo "Error: Python 3 not found. Please install Python 3.10+"; exit 1; }

# Install dependencies
echo "Installing dependencies..."
pip install --quiet --user gradio numpy loguru python-dotenv || pip3 install --quiet --user gradio numpy loguru python-dotenv

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "import gradio, numpy, loguru; print('✓ Core packages installed')" 2>/dev/null || { echo "✗ Package installation failed"; exit 1; }

# Create complete curriculum if needed
python3 -c "
import json
import os

curriculum_path = 'app/curriculum.json'
if os.path.exists(curriculum_path):
    with open(curriculum_path, 'r') as f:
        curriculum = json.load(f)
    if len(curriculum) < 26:
        print('Updating curriculum...')
    else:
        print('✓ Curriculum complete')
else:
    print('Creating curriculum...')

# Ensure complete curriculum
alphabet_data = [
    ('A', 'Apple'), ('B', 'Ball'), ('C', 'Cat'), ('D', 'Dog'),
    ('E', 'Elephant'), ('F', 'Fish'), ('G', 'Giraffe'), ('H', 'House'),
    ('I', 'Ice cream'), ('J', 'Jellyfish'), ('K', 'Kite'), ('L', 'Lion'),
    ('M', 'Monkey'), ('N', 'Nest'), ('O', 'Octopus'), ('P', 'Penguin'),
    ('Q', 'Queen'), ('R', 'Rainbow'), ('S', 'Sun'), ('T', 'Tiger'),
    ('U', 'Umbrella'), ('V', 'Violin'), ('W', 'Whale'), ('X', 'X-ray'),
    ('Y', 'Yo-yo'), ('Z', 'Zebra')
]

curriculum = {}
for letter, word in alphabet_data:
    curriculum[letter] = {
        'letter': letter,
        'phonetic': f'{letter.lower()} as in {word.lower()}',
        'examples': [word],
        'difficulty': 'easy' if letter in 'AEIOU' else 'medium',
        'activities': [{'type': 'learn', 'content': f'{letter} is for {word}'}]
    }

with open(curriculum_path, 'w') as f:
    json.dump(curriculum, f, indent=2)
print('✓ Curriculum ready')
" 2>/dev/null

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "GRADIO_SERVER_PORT=7860" > .env
    echo "GRADIO_SERVER_NAME=0.0.0.0" >> .env
    echo "✓ Environment configured"
else
    echo "✓ Environment ready"
fi

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "To start the application:"
echo "  python3 app/gradio_ui_simple.py"
echo ""
echo "Then open: http://localhost:7860"
echo ""

# Ask to start
read -p "Start now? [Y/n]: " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    python3 app/gradio_ui_simple.py
fi