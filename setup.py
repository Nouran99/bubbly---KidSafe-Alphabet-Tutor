#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Unified Setup Script
Handles both simple (quick start) and full (complete features) installation
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step_num, text):
    """Print formatted step"""
    print(f"\n[Step {step_num}] {text}")
    print("-" * 40)

def run_command(cmd, description="", shell=False):
    """Run a command and handle errors"""
    if description:
        print(f"  → {description}")
    
    try:
        if shell and platform.system() == "Windows":
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd.split() if isinstance(cmd, str) else cmd, 
                                  capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  ✗ Error: {result.stderr}")
            return False
        print("  ✓ Success")
        return True
    except Exception as e:
        print(f"  ✗ Failed: {str(e)}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required (current: {version.major}.{version.minor})")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment instructions"""
    print_step(1, "Virtual Environment Setup")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("  ✓ Virtual environment already exists")
    else:
        print("  Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv", "Creating venv"):
            return False
    
    # Provide activation instructions
    print("\n  📌 Activate the virtual environment:")
    if platform.system() == "Windows":
        print("     Command: venv\\Scripts\\activate")
    else:
        print("     Command: source venv/bin/activate")
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("\n  ⚠️  Virtual environment is NOT active!")
        print("  Please activate it and run this script again.")
        return False
    else:
        print("\n  ✓ Virtual environment is active")
    
    return True

def install_dependencies(mode="simple"):
    """Install Python dependencies based on mode"""
    print_step(2, f"Installing {mode.capitalize()} Dependencies")
    
    # Upgrade pip first
    print("  Upgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install core dependencies
    print("\n  Installing core dependencies...")
    core_deps = [
        "gradio==4.19.2",
        "gradio_client==0.10.1",
        "numpy==1.26.3",
        "loguru==0.7.2",
        "python-dotenv==1.0.0"
    ]
    
    for dep in core_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            print(f"  ⚠️  Failed to install {dep}, continuing...")
    
    if mode == "full":
        print("\n  Installing additional dependencies for full features...")
        
        # API and async dependencies
        api_deps = [
            "fastapi==0.109.2",
            "uvicorn[standard]==0.27.1",
            "starlette==0.36.3",
            "pydantic==2.5.3",
            "httpx==0.26.0",
            "aiofiles==23.2.1"
        ]
        
        # Computer vision and ML
        cv_deps = [
            "opencv-python==4.9.0.80",
            "Pillow==10.2.0",
            "scikit-learn==1.4.0",
            "torch>=2.0.0",
            "torchvision>=0.15.0",
            "transformers>=4.36.0"
        ]
        
        # Speech processing
        speech_deps = [
            "sounddevice==0.4.6",
            "soundfile==0.12.1",
            "librosa==0.10.1",
            "pyttsx3==2.90",
            "SpeechRecognition==3.10.1"
        ]
        
        # Multi-agent framework
        agent_deps = [
            "langchain==0.1.0",
            "langchain-community==0.0.10",
            "openai==1.8.0"
        ]
        
        all_deps = api_deps + cv_deps + speech_deps + agent_deps
        
        for dep in all_deps:
            if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
                print(f"  ⚠️  Failed to install {dep}, continuing...")
    
    print("\n  ✓ Dependencies installation completed")
    return True

def setup_environment_file():
    """Create .env file if it doesn't exist"""
    print_step(3, "Environment Configuration")
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("  ✓ .env file already exists")
    else:
        print("  Creating .env file with default settings...")
        env_content = """# KidSafe Alphabet Tutor Configuration

# Application Settings
DEBUG=False
ENVIRONMENT=development

# Model Settings (for full mode)
USE_LOCAL_MODELS=true
OLLAMA_BASE_URL=http://localhost:11434

# API Keys (optional, for full mode)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Privacy & Safety
COPPA_COMPLIANT=true
SESSION_ONLY_MEMORY=true
NO_DATA_PERSISTENCE=true
"""
        env_file.write_text(env_content)
        print("  ✓ .env file created")
    
    return True

def verify_installation(mode="simple"):
    """Verify the installation by importing key modules"""
    print_step(4, "Verifying Installation")
    
    # Test core imports
    core_modules = ["gradio", "numpy", "loguru", "dotenv"]
    
    if mode == "full":
        core_modules.extend(["fastapi", "cv2", "torch", "langchain"])
    
    failed_modules = []
    
    for module in core_modules:
        try:
            if module == "cv2":
                __import__("cv2")
            elif module == "dotenv":
                __import__("dotenv")
            else:
                __import__(module)
            print(f"  ✓ {module} imported successfully")
        except ImportError as e:
            print(f"  ✗ {module} import failed: {str(e)}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n  ⚠️  Some modules failed to import: {', '.join(failed_modules)}")
        return False
    
    print("\n  ✓ All modules imported successfully")
    return True

def fix_windows_compatibility():
    """Apply Windows-specific fixes"""
    print_step("Windows Fix", "Applying Windows Compatibility Fixes")
    
    # Uninstall potentially incompatible versions
    print("  Removing potentially incompatible packages...")
    packages_to_remove = [
        "gradio", "gradio-client", "fastapi", 
        "uvicorn", "starlette", "pydantic"
    ]
    
    for pkg in packages_to_remove:
        run_command(f"{sys.executable} -m pip uninstall -y {pkg}", f"Removing {pkg}")
    
    # Reinstall with compatible versions
    print("\n  Installing Windows-compatible versions...")
    compatible_packages = [
        "gradio==4.19.2",
        "gradio_client==0.10.1",
        "fastapi==0.109.2",
        "uvicorn[standard]==0.27.1",
        "starlette==0.36.3",
        "pydantic==2.5.3"
    ]
    
    for pkg in compatible_packages:
        run_command(f"{sys.executable} -m pip install {pkg}", f"Installing {pkg}")
    
    print("\n  ✓ Windows compatibility fixes applied")
    return True

def print_next_steps(mode="simple"):
    """Print next steps for the user"""
    print_header("Setup Complete! Next Steps:")
    
    print("1. Make sure your virtual environment is activated:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print(f"\n2. Start the application ({mode} mode):")
    if mode == "simple":
        print("   python app/simple_app.py  # Basic chat interface")
    else:
        print("   python app/main.py       # Full UI with audio/image support")
    
    print("\n3. Open your browser and go to:")
    print("   http://localhost:7860")
    
    if mode == "full":
        print("\n4. (Optional) For Ollama support, ensure Ollama is running:")
        print("   ollama serve")
        print("   ollama pull llama2")
    
    print("\n📚 For more information, check README.md")
    print("🐛 If you encounter issues, run: python diagnose.py")

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="KidSafe Alphabet Tutor Setup")
    parser.add_argument(
        "--mode",
        choices=["simple", "full"],
        default="simple",
        help="Installation mode: simple (quick start) or full (all features)"
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Shortcut for --mode simple"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Shortcut for --mode full"
    )
    parser.add_argument(
        "--fix-windows",
        action="store_true",
        help="Apply Windows compatibility fixes"
    )
    parser.add_argument(
        "--skip-venv",
        action="store_true",
        help="Skip virtual environment setup (not recommended)"
    )
    
    args = parser.parse_args()
    
    # Determine mode
    if args.simple:
        mode = "simple"
    elif args.full:
        mode = "full"
    else:
        mode = args.mode
    
    # Print banner
    print_header(f"KidSafe Alphabet Tutor - {mode.capitalize()} Setup")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Check Python version
    if not check_python_version():
        print("\n✗ Setup failed: Python 3.8+ required")
        sys.exit(1)
    
    # Apply Windows fixes if requested or if on Windows with issues
    if args.fix_windows or (platform.system() == "Windows" and "--fix-windows" in sys.argv):
        fix_windows_compatibility()
    
    # Setup virtual environment (unless skipped)
    if not args.skip_venv:
        if not setup_virtual_environment():
            print("\n⚠️  Please activate the virtual environment and run again:")
            print(f"   python setup.py --{mode}")
            sys.exit(1)
    
    # Install dependencies
    if not install_dependencies(mode):
        print("\n✗ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Setup environment file
    if not setup_environment_file():
        print("\n⚠️  Warning: Could not create .env file")
    
    # Verify installation
    if not verify_installation(mode):
        print("\n⚠️  Warning: Some modules failed to import")
        if platform.system() == "Windows":
            print("   Try running: python setup.py --fix-windows")
    
    # Print next steps
    print_next_steps(mode)
    
    print("\n✅ Setup completed successfully!")

if __name__ == "__main__":
    main()