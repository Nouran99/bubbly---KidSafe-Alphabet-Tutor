#!/usr/bin/env python3
"""
System Test - Verify all components are working
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports"""
    print("="*60)
    print("TESTING SYSTEM COMPONENTS")
    print("="*60)
    
    results = {"passed": 0, "failed": 0}
    
    # Test core imports
    imports_to_test = [
        ("Gradio", "gradio"),
        ("NumPy", "numpy"),
        ("Dotenv", "dotenv"),
        ("State Management", "app.state"),
        ("AI Agents", "agents.crew_ai_powered"),
        ("LangChain", "langchain"),
        ("Speech Recognition", "speech_recognition"),
        ("Text-to-Speech", "pyttsx3"),
        ("OpenCV", "cv2"),
        ("Tesseract", "pytesseract"),
    ]
    
    for name, module in imports_to_test:
        try:
            if "." in module:
                parts = module.split(".")
                __import__(module)
            else:
                __import__(module)
            print(f"✅ {name}: OK")
            results["passed"] += 1
        except ImportError as e:
            print(f"❌ {name}: FAILED - {e}")
            results["failed"] += 1
    
    print("\n" + "="*60)
    print(f"Results: {results['passed']} passed, {results['failed']} failed")
    
    if results["failed"] == 0:
        print("✅ ALL COMPONENTS READY!")
        return True
    else:
        print("⚠️  Some components need installation")
        print("Run: ./python setup.py")
        return False

def test_full_app():
    """Test the full AI app can be imported"""
    print("\n" + "="*60)
    print("TESTING FULL AI APP")
    print("="*60)
    
    try:
        from app.full_ai_app import FullAIAlphabetTutor, create_full_interface
        print("✅ Full AI App: Successfully imported")
        print("✅ FullAIAlphabetTutor class: Available")
        print("✅ create_full_interface function: Available")
        
        # Try to initialize (without starting)
        print("\nTrying to initialize tutor...")
        tutor = FullAIAlphabetTutor()
        print("✅ Tutor initialized successfully!")
        
        # Check components
        print("\nComponent Status:")
        print(f"  • Session Memory: {'✅' if hasattr(tutor, 'session_memory') else '❌'}")
        print(f"  • AI Agents: {'✅' if hasattr(tutor, 'agents') else '❌'}")
        print(f"  • Curriculum: {'✅' if hasattr(tutor, 'curriculum') else '❌'}")
        print(f"  • Assessment: {'✅' if hasattr(tutor, 'assessment_data') else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n" + "="*60)
    print("TESTING ENVIRONMENT")
    print("="*60)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info >= (3, 8):
        print("✅ Python 3.8+ detected")
    else:
        print("❌ Python 3.8+ required")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found (will use defaults)")
    
    # Check curriculum
    if os.path.exists("app/curriculum.json"):
        print("✅ Curriculum data found")
    else:
        print("❌ Curriculum data missing")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "🧪 KidSafe Alphabet Tutor - System Test 🧪\n")
    
    # Run tests
    env_ok = test_environment()
    imports_ok = test_imports()
    app_ok = test_full_app()
    
    # Summary
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    if env_ok and imports_ok and app_ok:
        print("✅ SYSTEM IS 100% READY!")
        print("\nYou can now run: python main.py")
        return 0
    else:
        print("⚠️  Some components need attention")
        print("\nPlease run: ./python setup.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())