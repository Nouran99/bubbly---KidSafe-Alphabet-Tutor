#!/usr/bin/env python3
"""
Simple startup script for KidSafe Alphabet Tutor
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def main():
    try:
        print("="*60)
        print("🎓 KidSafe Alphabet Tutor")
        print("="*60)
        print("\nStarting application...")
        
        # Run the main UI directly
        from app import gradio_ui_simple
        
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        print("Thank you for using KidSafe Alphabet Tutor!")
    except ImportError as e:
        print(f"\n❌ Missing dependencies: {e}")
        print("\nPlease run: pip install -r requirements-minimal.txt")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())