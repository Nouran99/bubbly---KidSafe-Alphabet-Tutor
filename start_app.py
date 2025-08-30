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
        # Import required modules
        from app.gradio_ui_simple import create_interface
        
        print("="*60)
        print("🎓 KidSafe Alphabet Tutor")
        print("="*60)
        print("\nStarting application...")
        print("This may take a few seconds...\n")
        
        # Create and launch interface
        interface = create_interface()
        
        print("✅ Application ready!")
        print("\nAccess the app at:")
        print("  • Local: http://localhost:7860")
        print("  • Network: http://0.0.0.0:7860")
        print("\nPress Ctrl+C to stop the server\n")
        print("-"*60)
        
        # Launch the interface
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_api=False,
            quiet=True
        )
        
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        print("Thank you for using KidSafe Alphabet Tutor!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("\nTroubleshooting steps:")
        print("1. Run: pip install -r requirements-minimal.txt")
        print("2. Run: python test_setup.py")
        print("3. Check port 7860 is not in use")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())