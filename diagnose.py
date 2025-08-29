#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - System Diagnostic Tool
Helps identify and fix common setup issues
Author: Nouran Darwish
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    
    @staticmethod
    def disable():
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.BLUE = ''
        Colors.END = ''

# Disable colors on Windows by default
if platform.system() == 'Windows':
    Colors.disable()

def print_header():
    print("=" * 60)
    print("   KidSafe Alphabet Tutor - System Diagnostics")
    print("=" * 60)
    print()

def check_mark(status):
    if status:
        return f"{Colors.GREEN}✓{Colors.END}"
    return f"{Colors.RED}✗{Colors.END}"

def print_check(name, status, details=""):
    mark = check_mark(status)
    status_text = "OK" if status else "FAILED"
    print(f"{mark} {name}: {status_text}")
    if details:
        print(f"  {Colors.YELLOW}{details}{Colors.END}")

def check_python():
    """Check Python version"""
    print(f"\n{Colors.BLUE}1. Python Environment{Colors.END}")
    print("-" * 40)
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    meets_requirement = version.major >= 3 and version.minor >= 10
    print_check(
        "Python Version", 
        meets_requirement,
        f"Found: {version_str} (Required: 3.10+)"
    )
    
    # Check virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    print_check(
        "Virtual Environment",
        in_venv,
        "Recommended to use virtual environment" if not in_venv else ""
    )
    
    # Check pip
    try:
        import pip
        pip_version = pip.__version__
        print_check("pip", True, f"Version: {pip_version}")
    except ImportError:
        print_check("pip", False, "pip not found")
    
    return meets_requirement

def check_required_packages():
    """Check if required Python packages are installed"""
    print(f"\n{Colors.BLUE}2. Required Python Packages{Colors.END}")
    print("-" * 40)
    
    packages = {
        "gradio": "UI Framework",
        "numpy": "Numerical Computing",
        "loguru": "Logging",
        "python-dotenv": "Environment Variables"
    }
    
    all_installed = True
    for package, description in packages.items():
        try:
            __import__(package.replace("-", "_"))
            print_check(package, True, description)
        except ImportError:
            print_check(package, False, f"Missing - {description}")
            all_installed = False
    
    return all_installed

def check_optional_packages():
    """Check optional AI packages"""
    print(f"\n{Colors.BLUE}3. Optional AI Packages{Colors.END}")
    print("-" * 40)
    
    packages = {
        "cv2": "OpenCV (Vision)",
        "pytesseract": "OCR (Letter Detection)",
        "faster_whisper": "ASR (Speech Recognition)",
        "ultralytics": "YOLO (Object Detection)",
        "torch": "PyTorch (Deep Learning)"
    }
    
    for package, description in packages.items():
        try:
            if package == "cv2":
                import cv2
            else:
                __import__(package)
            print_check(package, True, description)
        except ImportError:
            print_check(package, False, f"Not installed - {description}")

def check_system_dependencies():
    """Check system-level dependencies"""
    print(f"\n{Colors.BLUE}4. System Dependencies{Colors.END}")
    print("-" * 40)
    
    dependencies = {
        "tesseract": "OCR Engine",
        "ffmpeg": "Audio/Video Processing",
    }
    
    for cmd, description in dependencies.items():
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["where", cmd],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ["which", cmd],
                    capture_output=True,
                    text=True
                )
            
            found = result.returncode == 0
            print_check(cmd, found, description if found else f"Not found - {description}")
        except Exception:
            print_check(cmd, False, f"Could not check - {description}")

def check_project_files():
    """Check if all required project files exist"""
    print(f"\n{Colors.BLUE}5. Project Files{Colors.END}")
    print("-" * 40)
    
    required_files = [
        "app/gradio_ui_simple.py",
        "app/state.py",
        "app/curriculum.json",
        "agents/crew_setup_simple.py",
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        print_check(file, exists)
        if not exists:
            all_exist = False
    
    return all_exist

def check_network():
    """Check network connectivity"""
    print(f"\n{Colors.BLUE}6. Network & Ports{Colors.END}")
    print("-" * 40)
    
    # Check if port 7860 is available
    import socket
    
    port_available = True
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 7860))
        sock.close()
        
        if result == 0:
            port_available = False
            print_check("Port 7860", False, "Already in use")
        else:
            print_check("Port 7860", True, "Available")
    except:
        print_check("Port 7860", True, "Check failed but likely available")
    
    # Check localhost resolution
    try:
        socket.gethostbyname('localhost')
        print_check("Localhost", True, "Resolves correctly")
    except:
        print_check("Localhost", False, "Cannot resolve localhost")
    
    return port_available

def check_environment():
    """Check environment configuration"""
    print(f"\n{Colors.BLUE}7. Environment Configuration{Colors.END}")
    print("-" * 40)
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print_check(".env file", True, "Found")
        
        # Check key variables
        try:
            from dotenv import dotenv_values
            config = dotenv_values(".env")
            
            important_vars = ["GRADIO_SERVER_PORT", "GRADIO_SERVER_NAME"]
            for var in important_vars:
                if var in config:
                    print(f"  • {var}: {config[var]}")
        except:
            pass
    else:
        print_check(".env file", False, "Not found")
        if env_example.exists():
            print(f"  {Colors.YELLOW}Tip: Copy .env.example to .env{Colors.END}")

def suggest_fixes():
    """Suggest fixes for common issues"""
    print(f"\n{Colors.BLUE}Suggested Fixes{Colors.END}")
    print("-" * 40)
    
    suggestions = []
    
    # Check if we're in the right directory
    if not Path("app/gradio_ui_simple.py").exists():
        suggestions.append(
            "You might be in the wrong directory. Navigate to the project root:\n"
            "  cd kidsafe-alphabet-tutor"
        )
    
    # Check virtual environment
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        suggestions.append(
            "Create and activate a virtual environment:\n"
            "  python3 -m venv venv\n"
            "  source venv/bin/activate  # Linux/Mac\n"
            "  venv\\Scripts\\activate.bat  # Windows"
        )
    
    # Check if gradio is installed
    try:
        import gradio
    except ImportError:
        suggestions.append(
            "Install minimal requirements:\n"
            "  pip install gradio numpy loguru python-dotenv"
        )
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion}")
    else:
        print(f"{Colors.GREEN}No critical issues found!{Colors.END}")

def test_import():
    """Try to import the main application"""
    print(f"\n{Colors.BLUE}8. Application Import Test{Colors.END}")
    print("-" * 40)
    
    try:
        sys.path.insert(0, os.getcwd())
        from app import state
        print_check("app.state", True, "Session memory module")
    except Exception as e:
        print_check("app.state", False, str(e))
    
    try:
        from agents import crew_setup_simple
        print_check("agents.crew_setup_simple", True, "Agent system module")
    except Exception as e:
        print_check("agents.crew_setup_simple", False, str(e))

def main():
    print_header()
    
    # Run all checks
    python_ok = check_python()
    packages_ok = check_required_packages()
    check_optional_packages()
    check_system_dependencies()
    files_ok = check_project_files()
    network_ok = check_network()
    check_environment()
    test_import()
    
    # Overall status
    print(f"\n{Colors.BLUE}Overall Status{Colors.END}")
    print("-" * 40)
    
    can_run_basic = python_ok and packages_ok and files_ok and network_ok
    
    if can_run_basic:
        print(f"{Colors.GREEN}✓ System is ready to run the basic version!{Colors.END}")
        print("\nTo start the application:")
        print("  python app/gradio_ui_simple.py")
    else:
        print(f"{Colors.RED}✗ Some issues need to be fixed before running.{Colors.END}")
        suggest_fixes()
    
    print("\n" + "=" * 60)
    print("Diagnostics complete!")
    
    return 0 if can_run_basic else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDiagnostics interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Diagnostic tool error: {e}{Colors.END}")
        sys.exit(1)