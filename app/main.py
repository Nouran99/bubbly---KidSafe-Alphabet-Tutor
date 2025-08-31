#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Full Mode Entry Point
This runs the application with all features enabled
Author: Nouran Darwish
"""

import sys
import os
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging for full mode
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for full mode"""
    try:
        # Import the full UI application
        from app.gradio_ui_simple import create_interface
        
        logger.info("=" * 60)
        logger.info("Starting KidSafe Alphabet Tutor - FULL MODE")
        logger.info("=" * 60)
        logger.info("This mode includes all features:")
        logger.info("- Complete curriculum with all 26 letters")
        logger.info("- Advanced activities and games")
        logger.info("- Progress tracking")
        logger.info("- Adaptive difficulty")
        logger.info("- Full multi-agent system")
        logger.info("- Audio input support")
        logger.info("- Image recognition (if enabled)")
        logger.info("=" * 60)
        
        # Create the Gradio interface with full features
        interface = create_interface()
        
        # Launch with full features
        logger.info("\nLaunching application with full features...")
        logger.info("Open your browser to: http://localhost:7860\n")
        
        interface.queue(max_size=20).launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=False,  # Set to True for development
            show_api=False,  # Prevent ASGI errors
            show_error=True,
            quiet=False
        )
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Some dependencies may be missing. Run: python setup.py --full")
        logger.error("\nFalling back to simple mode...")
        
        # Fallback to simple mode if full mode fails
        try:
            logger.info("Attempting to start simple mode instead...")
            from app.simple_app import app
            app.queue(max_size=10).launch(
                server_name="0.0.0.0",
                server_port=7860,
                share=False,
                debug=False,
                show_api=False
            )
        except Exception as fallback_error:
            logger.error(f"Failed to start even simple mode: {fallback_error}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        logger.error("Please check the logs and try again.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("KidSafe Alphabet Tutor - Full Mode")
    print("="*60)
    print("\nInitializing full feature set...")
    print("This may take a moment...\n")
    
    # Check if running in virtual environment (recommended)
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: Not running in a virtual environment!")
        print("   Recommended: python -m venv venv && source venv/bin/activate\n")
    
    # Check for full mode dependencies
    print("Checking dependencies...")
    try:
        import gradio
        import numpy
        print("✓ Core dependencies found")
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("  Run: python setup.py --full")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        print("Thank you for using Bubbly! 🫧")
        sys.exit(0)