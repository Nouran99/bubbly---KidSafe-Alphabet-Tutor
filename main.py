#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Main Entry Point
Launches the FULL AI-powered application
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the full AI app
from app.full_ai_app import create_full_interface, tutor

if __name__ == "__main__":
    print("\n" + "="*70)
    print("KidSafe Alphabet Tutor - Starting FULL AI Mode")
    print("="*70)
    print("Features:")
    print("  ✅ Speech Recognition & Text-to-Speech")
    print("  ✅ Vision/Webcam Letter Detection")
    print("  ✅ AI-Powered Natural Language Understanding")
    print("  ✅ Phonics-Focused Learning")
    print("  ✅ Real-time Pronunciation Feedback")
    print("  ✅ Complete Assessment Tracking")
    print("="*70)
    print("\nInitializing...")
    
    try:
        app = create_full_interface()
        print("\n✅ System Ready!")
        print("Open your browser to: http://localhost:7860")
        print("="*70 + "\n")
        
        app.queue(max_size=20).launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            debug=False,
            show_api=False,
            show_error=True
        )
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        print("Thank you for using KidSafe Alphabet Tutor! 🫧")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("Please run: python setup.py to install dependencies")
        sys.exit(1)