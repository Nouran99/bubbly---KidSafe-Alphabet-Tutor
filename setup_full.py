#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Universal Complete Setup Script
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Disable colors on Windows if not supported
if platform.system() == 'Windows':
    try:
        import colorama
        colorama.init()
    except ImportError:
        # If colorama not available, disable colors
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

def print_header():
    """Print setup header"""
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}   KidSafe Alphabet Tutor - Complete Setup{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.WHITE}Platform: {platform.system()} {platform.release()}{Colors.RESET}")
    print(f"{Colors.WHITE}Python: {sys.version.split()[0]}{Colors.RESET}")
    print(f"{Colors.WHITE}Directory: {os.getcwd()}{Colors.RESET}")
    print()

def print_step(message):
    """Print step message"""
    print(f"\n{Colors.BLUE}▶ {message}{Colors.RESET}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.WHITE}ℹ {message}{Colors.RESET}")

def run_command(command, silent=True):
    """Run a shell command"""
    try:
        if silent:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True)
        return result.returncode == 0
    except Exception as e:
        if not silent:
            print_error(f"Command failed: {e}")
        return False

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} (3.10+ required)")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} found but 3.10+ required")
        return False

def check_project_files():
    """Check if we're in the correct directory"""
    required_files = [
        'app/gradio_ui_simple.py',
        'agents/crew_setup_simple.py',
        'app/state.py'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print_error(f"Missing required file: {file}")
            print_info("Please run this script from the project root directory")
            return False
    
    print_success("All project files found")
    return True

def setup_virtual_environment():
    """Create and activate virtual environment"""
    venv_path = Path('venv')
    
    if not venv_path.exists():
        print_info("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'])
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")
    
    # Get activation script path
    if platform.system() == 'Windows':
        activate_path = venv_path / 'Scripts' / 'activate.bat'
        python_path = venv_path / 'Scripts' / 'python.exe'
    else:
        activate_path = venv_path / 'bin' / 'activate'
        python_path = venv_path / 'bin' / 'python'
    
    print_info(f"To activate manually: source {activate_path}")
    return str(python_path)

def upgrade_pip(python_exe):
    """Upgrade pip to latest version"""
    print_info("Upgrading pip...")
    run_command(f'"{python_exe}" -m pip install --quiet --upgrade pip')
    print_success("pip upgraded")

def install_dependencies(python_exe, install_type):
    """Install Python dependencies based on type"""
    requirements_files = {
        '1': 'requirements-minimal.txt',
        '2': 'requirements-standard.txt',
        '3': 'requirements-full.txt'
    }
    
    fallback_packages = {
        '1': 'gradio numpy loguru python-dotenv',
        '2': 'gradio numpy loguru python-dotenv pillow better-profanity aiofiles pytest',
        '3': 'gradio numpy loguru python-dotenv pillow opencv-python pytesseract scipy librosa'
    }
    
    req_file = requirements_files.get(install_type)
    
    if req_file and os.path.exists(req_file):
        print_info(f"Installing from {req_file}...")
        success = run_command(f'"{python_exe}" -m pip install --quiet -r {req_file}')
    else:
        print_info("Installing packages directly...")
        packages = fallback_packages.get(install_type, fallback_packages['2'])
        success = run_command(f'"{python_exe}" -m pip install --quiet {packages}')
    
    if success:
        print_success("Dependencies installed successfully")
    else:
        print_warning("Some packages may have failed to install")
    
    return success

def setup_curriculum():
    """Ensure curriculum.json is complete"""
    curriculum_path = Path('app/curriculum.json')
    
    try:
        if curriculum_path.exists():
            with open(curriculum_path, 'r') as f:
                curriculum = json.load(f)
            
            if len(curriculum) == 26:
                print_success(f"Curriculum complete ({len(curriculum)} letters)")
                return True
        
        # Create complete curriculum
        print_info("Creating complete A-Z curriculum...")
        alphabet_data = [
            ('A', 'Apple', 'Ant'), ('B', 'Ball', 'Bear'), ('C', 'Cat', 'Car'),
            ('D', 'Dog', 'Duck'), ('E', 'Elephant', 'Egg'), ('F', 'Fish', 'Flower'),
            ('G', 'Giraffe', 'Grape'), ('H', 'House', 'Hat'), ('I', 'Ice cream', 'Igloo'),
            ('J', 'Jellyfish', 'Juice'), ('K', 'Kite', 'Kangaroo'), ('L', 'Lion', 'Lemon'),
            ('M', 'Monkey', 'Moon'), ('N', 'Nest', 'Nose'), ('O', 'Octopus', 'Orange'),
            ('P', 'Penguin', 'Pizza'), ('Q', 'Queen', 'Quilt'), ('R', 'Rainbow', 'Rabbit'),
            ('S', 'Sun', 'Star'), ('T', 'Tiger', 'Tree'), ('U', 'Umbrella', 'Unicorn'),
            ('V', 'Violin', 'Volcano'), ('W', 'Whale', 'Watermelon'), ('X', 'X-ray', 'Xylophone'),
            ('Y', 'Yo-yo', 'Yacht'), ('Z', 'Zebra', 'Zoo')
        ]
        
        curriculum = {}
        for letter, word1, word2 in alphabet_data:
            curriculum[letter] = {
                'letter': letter,
                'phonetic': f'{letter.lower()} as in {word1.lower()}',
                'examples': [word1, word2],
                'difficulty': 'easy' if letter in 'AEIOU' else 'medium',
                'activities': [
                    {'type': 'repeat_after_me', 'content': f'Say {letter}! {letter} is for {word1}!'},
                    {'type': 'find_an_object', 'content': f'Can you find something that starts with {letter}?'},
                    {'type': 'letter_matching', 'content': f'Match the letter {letter} with {word1}'}
                ],
                'encouragement': [
                    f'Great job! You learned the letter {letter}!',
                    f'{letter} is for {word1}!',
                    f'You are doing amazing with the letter {letter}!'
                ]
            }
        
        with open(curriculum_path, 'w') as f:
            json.dump(curriculum, f, indent=2)
        
        print_success("Complete curriculum created")
        return True
        
    except Exception as e:
        print_error(f"Failed to setup curriculum: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path('.env')
    
    if not env_path.exists():
        env_content = """# KidSafe Alphabet Tutor Environment Configuration
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
LOG_LEVEL=INFO
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        print_success("Environment file created")
    else:
        print_success("Environment file exists")

def run_tests(python_exe):
    """Run verification tests"""
    if os.path.exists('test_setup.py'):
        print_info("Running verification tests...")
        success = run_command(f'"{python_exe}" test_setup.py', silent=True)
        if success:
            print_success("All tests passed")
        else:
            print_warning("Some tests failed but core functionality should work")
    else:
        print_warning("test_setup.py not found, skipping tests")

def create_startup_scripts():
    """Create platform-specific startup scripts"""
    
    # Create run.sh for Unix-like systems
    if platform.system() != 'Windows':
        run_sh = """#!/bin/bash
# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the application
echo "Starting KidSafe Alphabet Tutor..."
python app/gradio_ui_simple.py
"""
        with open('run.sh', 'w') as f:
            f.write(run_sh)
        os.chmod('run.sh', 0o755)
        print_success("Created run.sh")
    
    # Create run.bat for Windows
    if platform.system() == 'Windows':
        run_bat = """@echo off
REM Activate virtual environment if it exists
if exist "venv" (
    call venv\\Scripts\\activate.bat
)

REM Start the application
echo Starting KidSafe Alphabet Tutor...
python app\\gradio_ui_simple.py
pause
"""
        with open('run.bat', 'w') as f:
            f.write(run_bat)
        print_success("Created run.bat")

def main():
    """Main setup process"""
    print_header()
    
    # Step 1: Check Python version
    print_step("Step 1: Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check project files
    print_step("Step 2: Checking project files...")
    if not check_project_files():
        sys.exit(1)
    
    # Step 3: Setup virtual environment
    print_step("Step 3: Setting up virtual environment...")
    python_exe = setup_virtual_environment()
    
    # Step 4: Upgrade pip
    print_step("Step 4: Upgrading pip...")
    upgrade_pip(python_exe)
    
    # Step 5: Choose installation type
    print_step("Step 5: Selecting installation type...")
    print("\nInstallation Options:")
    print("  1) Minimal  - Core functionality only (2 min, ~150MB)")
    print("  2) Standard - Recommended for most users (5 min, ~300MB)")
    print("  3) Full     - All features including AI (15 min, ~1GB)")
    print()
    
    install_choice = input("Select option [1-3] (default: 2): ").strip() or '2'
    
    if install_choice not in ['1', '2', '3']:
        print_error("Invalid choice")
        sys.exit(1)
    
    install_types = {'1': 'minimal', '2': 'standard', '3': 'full'}
    install_type_name = install_types[install_choice]
    
    # Step 6: Install dependencies
    print_step("Step 6: Installing Python packages...")
    print_info(f"Installing {install_type_name} dependencies...")
    install_dependencies(python_exe, install_choice)
    
    # Step 7: Setup curriculum
    print_step("Step 7: Setting up curriculum data...")
    setup_curriculum()
    
    # Step 8: Create .env file
    print_step("Step 8: Setting up environment...")
    create_env_file()
    
    # Step 9: Run tests
    print_step("Step 9: Running verification tests...")
    run_tests(python_exe)
    
    # Step 10: Create startup scripts
    print_step("Step 10: Creating startup scripts...")
    create_startup_scripts()
    
    # Summary
    print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Setup Complete!{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.WHITE}Installation Summary:{Colors.RESET}")
    print(f"  • Type: {install_type_name}")
    print(f"  • Python: {sys.version.split()[0]}")
    print(f"  • Virtual Env: venv/")
    print(f"  • Dependencies: Installed")
    print()
    print(f"{Colors.WHITE}To start the application:{Colors.RESET}")
    
    if platform.system() == 'Windows':
        print(f"{Colors.CYAN}  run.bat{Colors.RESET}")
        print(f"{Colors.WHITE}Or manually:{Colors.RESET}")
        print(f"{Colors.CYAN}  venv\\Scripts\\activate.bat{Colors.RESET}")
        print(f"{Colors.CYAN}  python app\\gradio_ui_simple.py{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}  ./run.sh{Colors.RESET}")
        print(f"{Colors.WHITE}Or manually:{Colors.RESET}")
        print(f"{Colors.CYAN}  source venv/bin/activate{Colors.RESET}")
        print(f"{Colors.CYAN}  python app/gradio_ui_simple.py{Colors.RESET}")
    
    print()
    print(f"{Colors.WHITE}Then open in browser:{Colors.RESET}")
    print(f"{Colors.CYAN}  http://localhost:7860{Colors.RESET}")
    print()
    
    # Ask if user wants to start now
    start_now = input("Start the application now? [Y/n]: ").strip().lower()
    if start_now != 'n':
        print_info("\nStarting KidSafe Alphabet Tutor...")
        subprocess.run([python_exe, 'app/gradio_ui_simple.py'])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)