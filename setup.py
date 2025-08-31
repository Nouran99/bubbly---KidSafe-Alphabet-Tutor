#!/usr/bin/env python3
"""
KidSafe Alphabet Tutor - Complete Setup Script
Installs ALL components for the FULL AI-powered application
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path


class KidSafeSetup:
    def __init__(self):
        self.os_type = self.detect_os()
        self.venv_path = Path("venv")
        
    def detect_os(self):
        """Detect the operating system"""
        system = platform.system().lower()
        if system == "linux":
            return "linux"
        elif system == "darwin":
            return "mac"
        elif system == "windows":
            return "windows"
        else:
            return "unknown"
    
    def print_header(self):
        """Print the setup header"""
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║     KidSafe Alphabet Tutor - FULL AI Setup                  ║")
        print("║     Speech + Vision + AI + Phonics                          ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print(f"📍 Detected OS: {self.os_type}")
        print()
    
    def run_command(self, command, shell=True, check=True):
        """Run a system command safely"""
        try:
            result = subprocess.run(command, shell=shell, check=check, 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e}")
            return False
    
    def install_system_deps(self):
        """Install system-level dependencies"""
        print("📦 Installing system dependencies...")
        
        if self.os_type == "linux":
            print("→ Updating package list...")
            self.run_command("sudo apt-get update")
            
            print("→ Installing audio libraries...")
            self.run_command("sudo apt-get install -y portaudio19-dev python3-pyaudio")
            self.run_command("sudo apt-get install -y espeak ffmpeg libespeak1")
            
            print("→ Installing Tesseract OCR...")
            self.run_command("sudo apt-get install -y tesseract-ocr tesseract-ocr-eng")
            
            print("→ Installing webcam support...")
            self.run_command("sudo apt-get install -y v4l-utils")
            
        elif self.os_type == "mac":
            # Check if Homebrew is installed
            if not shutil.which("brew"):
                print("❌ Homebrew not found. Installing...")
                install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                self.run_command(install_cmd)
            
            print("→ Installing audio libraries...")
            self.run_command("brew install portaudio")
            
            print("→ Installing Tesseract OCR...")
            self.run_command("brew install tesseract")
            
            print("→ Installing FFmpeg...")
            self.run_command("brew install ffmpeg")
            
        elif self.os_type == "windows":
            print("⚠️  Windows system dependencies require manual installation:")
            print("   1. Install Visual Studio Build Tools")
            print("   2. Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("   3. Install FFmpeg from: https://ffmpeg.org/download.html")
    
    def setup_venv(self):
        """Setup Python virtual environment"""
        print("🐍 Setting up Python virtual environment...")
        
        if self.venv_path.exists():
            print("→ Virtual environment already exists")
        else:
            print("→ Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        print("→ Virtual environment created")
        
        # Get pip path
        if self.os_type == "windows":
            pip_path = self.venv_path / "Scripts" / "pip"
            python_path = self.venv_path / "Scripts" / "python"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"
        
        print("→ Upgrading pip...")
        subprocess.run([str(python_path), "-m", "pip", "install", "--upgrade", 
                       "pip", "wheel", "setuptools"], check=True)
        
        return pip_path, python_path
    
    def install_python_deps(self, pip_path):
        """Install Python dependencies"""
        print("📚 Installing Python dependencies...")
        
        # Core dependencies
        print("→ Installing core dependencies...")
        core_deps = [
            "gradio==4.16.0",
            "numpy==1.26.3",
            "python-dotenv==1.0.0",
            "loguru==0.7.2",
            "audioop-lts==0.2.2"
        ]
        
        for dep in core_deps:
            subprocess.run([str(pip_path), "install", dep], check=True)
        
        # Web framework dependencies
        print("→ Installing web framework...")
        web_deps = [
            "fastapi==0.109.2",
            "pydantic==2.5.3",        # if you have issues with Pydantic, try running: fix_windows.bat, and comment this line
            "httpx==0.26.0",
            "aiofiles==23.2.1"
        ]
        
        for dep in web_deps:
            subprocess.run([str(pip_path), "install", dep], check=True)
        
        # AI/LLM dependencies
        print("→ Installing AI components...")
        ai_deps = [
            "langchain==0.1.0",
            "langchain-community==0.0.10",
            "openai==1.8.0",
            "tiktoken==0.11.0",
            "chromadb==0.4.22"
        ]
        
        for dep in ai_deps:
            subprocess.run([str(pip_path), "install", dep], check=True)
        
        # Speech components
        print("→ Installing speech recognition and TTS...")
        speech_deps = [
            "SpeechRecognition==3.10.1",
            "pyttsx3==2.90",
            "sounddevice==0.4.6",
            "soundfile==0.12.1"
        ]
        
        for dep in speech_deps:
            subprocess.run([str(pip_path), "install", dep], check=True)
        
        # Try to install PyAudio (may fail on some systems)
        try:
            subprocess.run([str(pip_path), "install", "pyaudio"], check=True)
            print("✅ PyAudio installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  PyAudio installation failed (optional)")
        
        # Vision components
        print("→ Installing vision and OCR...")
        vision_deps = [
            "opencv-python==4.9.0.80",
            "pytesseract==0.3.10",
            "Pillow==10.4.0"
        ]
        
        for dep in vision_deps:
            subprocess.run([str(pip_path), "install", dep], check=True)
        
        # Machine Learning (optional - large)
        print()
        install_ml = input("Install ML models for advanced vision (2GB+)? [y/N]: ").strip().lower()
        if install_ml in ['y', 'yes']:
            print("→ Installing PyTorch and Transformers...")
            ml_deps = ["torch", "torchvision", "transformers"]
            for dep in ml_deps:
                subprocess.run([str(pip_path), "install", dep], check=True)
    
    def setup_ollama(self):
        """Setup Ollama for local AI"""
        print("🤖 Setting up Ollama for local AI...")
        
        install_ollama = input("Install Ollama for local AI models? [y/N]: ").strip().lower()
        if install_ollama not in ['y', 'yes']:
            return
        
        if self.os_type == "linux":
            print("→ Installing Ollama...")
            install_cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
            self.run_command(install_cmd)
            
        elif self.os_type == "mac":
            print("→ Installing Ollama via Homebrew...")
            self.run_command("brew install ollama")
            
        else:
            print("⚠️  Please install Ollama manually from: https://ollama.ai/download")
            return
        
        print("→ Starting Ollama service...")
        # Start Ollama in background
        try:
            subprocess.Popen(["ollama", "serve"], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            import time
            time.sleep(5)
        except FileNotFoundError:
            print("⚠️  Ollama not found in PATH")
            return
        
        print("→ Pulling AI models...")
        models = ["llama2", "mistral"]
        for model in models:
            try:
                subprocess.run(["ollama", "pull", model], check=True)
                print(f"✅ {model} model downloaded")
            except subprocess.CalledProcessError:
                print(f"⚠️  Failed to pull {model}")
        
        print("✅ Ollama setup complete")
    
    def create_env_file(self):
        """Create environment configuration file"""
        print("⚙️  Creating configuration file...")
        
        env_path = Path(".env")
        if env_path.exists():
            print("→ .env file already exists, skipping...")
            return
        
        env_content = """# KidSafe Alphabet Tutor Configuration

# AI Configuration
USE_OLLAMA=true
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434

# Optional: OpenAI Configuration
# OPENAI_API_KEY=your_api_key_here
# USE_OLLAMA=false  # Set to false to use OpenAI

# Speech Configuration
TTS_ENABLED=true
ASR_ENABLED=true
TTS_VOICE=child_friendly
SPEECH_RATE=150
AUDIO_QUALITY=high

# Vision Configuration
VISION_ENABLED=true
WEBCAM_ENABLED=true
OCR_ENABLED=true
OBJECT_DETECTION=true

# Privacy & Safety (COPPA Compliance)
COPPA_COMPLIANT=true
SESSION_ONLY_MEMORY=true
NO_DATA_PERSISTENCE=true
CONTENT_FILTER=strict
MAX_SESSION_DURATION=30

# Assessment Settings
TRACK_PRONUNCIATION=true
TRACK_PROGRESS=true
SHOW_ASSESSMENT=true

# Debug Settings
DEBUG=false
LOG_LEVEL=INFO
"""
        
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ Configuration file created")
    
    def test_installation(self, python_path):
        """Test the installation"""
        print("🧪 Testing installation...")
        print()
        
        # Test Python imports
        test_script = '''
import sys
print(f"Python version: {sys.version}")

modules_to_test = [
    ("gradio", "Gradio"),
    ("langchain", "LangChain"), 
    ("speech_recognition", "Speech Recognition"),
    ("pyttsx3", "Text-to-Speech"),
    ("cv2", "OpenCV"),
    ("pytesseract", "Tesseract OCR")
]

for module, name in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {name}: Installed")
    except ImportError:
        print(f"❌ {name}: Not installed")
'''
        
        subprocess.run([str(python_path), "-c", test_script])
        
        # Test Ollama
        if shutil.which("ollama"):
            print("✅ Ollama: Installed")
            try:
                subprocess.run(["ollama", "list"], check=True, 
                             capture_output=True)
                print("✅ Ollama: Running")
            except subprocess.CalledProcessError:
                print("⚠️  Ollama not running")
        else:
            print("⚠️  Ollama: Not installed (optional)")
        
        # Test Tesseract
        if shutil.which("tesseract"):
            print("✅ Tesseract CLI: Installed")
        else:
            print("⚠️  Tesseract CLI: Not installed")
    
    def print_completion_message(self):
        """Print completion message with next steps"""
        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    Setup Complete! 🎉                       ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        print("📝 Next Steps:")
        print()
        
        if self.os_type == "windows":
            print("1. Activate virtual environment:")
            print("   venv\\Scripts\\activate")
        else:
            print("1. Activate virtual environment:")
            print("   source venv/bin/activate")
        
        print()
        print("2. Start the application:")
        print("   python main.py")
        print()
        print("3. Open your browser to:")
        print("   http://localhost:7860")
        print()
        print("📋 Available Features:")
        print("  • 🎤 Speech Recognition (Microphone input)")
        print("  • 🔊 Text-to-Speech (Voice responses)")
        print("  • 📷 Vision/Webcam (Letter detection)")
        print("  • 🤖 AI Intelligence (Natural language)")
        print("  • 📊 Assessment Tracking")
        print("  • 🔤 Phonics Focus")
        print()
        print("For help, see README.md or docs/USER_GUIDE.md")
        print()
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        version_info = sys.version_info
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
            print(f"❌ Python 3.8+ required (found {version_info.major}.{version_info.minor})")
            sys.exit(1)
        
        print(f"✅ Python {version_info.major}.{version_info.minor}.{version_info.micro} detected")
        print()
    
    def run_setup(self):
        """Main setup process"""
        try:
            self.print_header()
            
            # Check Python version
            self.check_python_version()
            
            # Install system dependencies
            self.install_system_deps()
            
            # Setup virtual environment
            pip_path, python_path = self.setup_venv()
            
            # Install Python dependencies
            self.install_python_deps(pip_path)
            
            # Setup Ollama
            self.setup_ollama()
            
            # Create environment file
            self.create_env_file()
            
            # Test installation
            print()
            self.test_installation(python_path)
            
            # Print completion message
            self.print_completion_message()
            
        except KeyboardInterrupt:
            print("\n❌ Setup interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    setup = KidSafeSetup()
    setup.run_setup()


if __name__ == "__main__":
    main()