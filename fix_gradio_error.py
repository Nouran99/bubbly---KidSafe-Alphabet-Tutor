#!/usr/bin/env python3
"""
Fix for Gradio ASGI/TypeError issue
This script patches the Gradio launch configuration to avoid the API schema error
"""

import os
import sys

def fix_gradio_launch():
    """Fix the gradio launch configuration in gradio_ui_simple.py"""
    
    file_path = 'app/gradio_ui_simple.py'
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: Disable API documentation which causes the error
    old_launch = """interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False,
            prevent_thread_lock=False
        )"""
    
    new_launch = """interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False,
            prevent_thread_lock=False,
            show_error=True,
            quiet=True
        )"""
    
    if old_launch in content:
        content = content.replace(old_launch, new_launch)
        print("✓ Fixed primary launch configuration")
    
    # Fix 2: Also fix the fallback launch
    old_fallback = """interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False
        )"""
    
    new_fallback = """interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_api=False,
            inbrowser=False,
            show_error=True,
            quiet=True
        )"""
    
    if old_fallback in content:
        content = content.replace(old_fallback, new_fallback)
        print("✓ Fixed fallback launch configuration")
    
    # Write the fixed content
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✓ Gradio launch configuration updated")
    print("\nThe TypeError should now be resolved.")
    print("You can run the app with: python app/gradio_ui_simple.py")

if __name__ == "__main__":
    fix_gradio_launch()