#!/usr/bin/env python3
"""
Test script to verify the KidSafe Alphabet Tutor setup
"""

import sys
import os
sys.path.insert(0, '.')

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    errors = []
    
    # Core imports
    try:
        import gradio
        print("  ✓ gradio")
    except ImportError as e:
        errors.append(f"  ✗ gradio: {e}")
    
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        errors.append(f"  ✗ numpy: {e}")
    
    try:
        import loguru
        print("  ✓ loguru")
    except ImportError as e:
        errors.append(f"  ✗ loguru: {e}")
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError as e:
        errors.append(f"  ✗ python-dotenv: {e}")
    
    # App modules
    try:
        from app.state import SessionMemory
        print("  ✓ app.state")
    except ImportError as e:
        errors.append(f"  ✗ app.state: {e}")
    
    try:
        from agents.crew_setup_simple import AlphabetTutorAgents
        print("  ✓ agents.crew_setup_simple")
    except ImportError as e:
        errors.append(f"  ✗ agents.crew_setup_simple: {e}")
    
    try:
        from app.progress import ProgressTracker
        print("  ✓ app.progress")
    except ImportError as e:
        errors.append(f"  ✗ app.progress: {e}")
    
    try:
        from app.activities import AlphabetActivities
        print("  ✓ app.activities")
    except ImportError as e:
        errors.append(f"  ✗ app.activities: {e}")
    
    return errors

def test_files():
    """Test required files exist"""
    print("\nTesting files...")
    errors = []
    
    required_files = [
        'app/gradio_ui_simple.py',
        'app/state.py',
        'app/progress.py',
        'app/activities.py',
        'app/curriculum.json',
        'agents/crew_setup_simple.py',
        '.env',
        'requirements-minimal.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            errors.append(f"  ✗ {file} not found")
    
    return errors

def test_curriculum():
    """Test curriculum data"""
    print("\nTesting curriculum...")
    errors = []
    
    try:
        import json
        with open('app/curriculum.json', 'r') as f:
            curriculum = json.load(f)
        
        if len(curriculum) == 26:
            print(f"  ✓ Complete A-Z curriculum ({len(curriculum)} letters)")
        else:
            errors.append(f"  ✗ Incomplete curriculum (only {len(curriculum)} letters)")
        
        # Check a sample letter
        if 'A' in curriculum:
            a_data = curriculum['A']
            if all(key in a_data for key in ['letter', 'phonetic', 'examples', 'activities']):
                print("  ✓ Curriculum structure correct")
            else:
                errors.append("  ✗ Curriculum structure incomplete")
    except Exception as e:
        errors.append(f"  ✗ Curriculum error: {e}")
    
    return errors

def test_basic_functionality():
    """Test basic app functionality"""
    print("\nTesting basic functionality...")
    errors = []
    
    try:
        from app.state import SessionMemory
        from agents.crew_setup_simple import AlphabetTutorAgents
        
        memory = SessionMemory()
        agents = AlphabetTutorAgents(memory)
        
        result = agents.process_interaction("Hello")
        if result and 'response' in result:
            print("  ✓ Agent system working")
        else:
            errors.append("  ✗ Agent system not responding correctly")
    except Exception as e:
        errors.append(f"  ✗ Functionality test failed: {e}")
    
    return errors

def main():
    print("="*60)
    print("KidSafe Alphabet Tutor - Setup Test")
    print("="*60)
    
    all_errors = []
    
    # Run tests
    all_errors.extend(test_imports())
    all_errors.extend(test_files())
    all_errors.extend(test_curriculum())
    all_errors.extend(test_basic_functionality())
    
    # Summary
    print("\n" + "="*60)
    if all_errors:
        print("❌ Setup has issues:")
        for error in all_errors:
            print(error)
        print("\nTo fix:")
        print("1. Run: pip install -r requirements-minimal.txt")
        print("2. Check missing files")
        print("3. Run this test again")
        return 1
    else:
        print("✅ Setup is complete and working!")
        print("\nYou can now run:")
        print("  python app/gradio_ui_simple.py")
        print("\nThen open: http://localhost:7860")
        return 0

if __name__ == "__main__":
    sys.exit(main())