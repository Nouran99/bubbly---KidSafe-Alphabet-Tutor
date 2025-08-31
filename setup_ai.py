#!/usr/bin/env python3
"""
AI-Powered Setup for KidSafe Alphabet Tutor
Installs and configures AI/LLM dependencies
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    if description:
        print(f"→ {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✗ Error: {result.stderr}")
            return False
        print("✓ Success")
        return True
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return False

def setup_ai_mode():
    """Setup AI-powered mode with all LLM dependencies"""
    
    print_header("KidSafe Alphabet Tutor - AI-Powered Setup")
    
    print("This will install AI/LLM components for intelligent tutoring:")
    print("- LangChain for AI orchestration")
    print("- OpenAI SDK for GPT models (optional)")
    print("- Ollama for local models (recommended)")
    print("- Vector databases for memory")
    print()
    
    # Step 1: Install core AI dependencies
    print_header("Step 1: Installing AI Dependencies")
    
    ai_packages = [
        "langchain==0.1.0",
        "langchain-community==0.0.10",
        "openai==1.8.0",
        "tiktoken==0.5.2",
        "chromadb==0.4.22",
        "sentence-transformers==2.2.2"
    ]
    
    for package in ai_packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"Warning: Failed to install {package}")
    
    # Step 2: Setup Ollama (optional but recommended)
    print_header("Step 2: Ollama Setup (Local AI Models)")
    
    print("Ollama allows you to run AI models locally without API keys.")
    print("It's private, free, and works offline after initial download.\n")
    
    if platform.system() != "Windows":
        install_ollama = input("Install Ollama for local AI? (y/n): ").lower()
        if install_ollama == 'y':
            print("\nInstalling Ollama...")
            if platform.system() == "Darwin":  # macOS
                run_command("brew install ollama", "Installing Ollama via Homebrew")
            else:  # Linux
                run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama")
            
            print("\nStarting Ollama service...")
            run_command("ollama serve &", "Starting Ollama server")
            
            print("\nPulling recommended models...")
            run_command("ollama pull llama2", "Downloading Llama 2 model (4GB)")
            run_command("ollama pull mistral", "Downloading Mistral model (4GB)")
    else:
        print("For Windows, please install Ollama manually from: https://ollama.ai/download")
        print("Then run: ollama pull llama2")
    
    # Step 3: Configure environment
    print_header("Step 3: Environment Configuration")
    
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print("Creating .env file...")
        with open(env_file, 'w') as f:
            f.write("# AI Configuration\n")
            f.write("USE_OLLAMA=true  # Use local Ollama models\n")
            f.write("OLLAMA_MODEL=llama2  # or mistral, phi, etc.\n")
            f.write("\n")
            f.write("# Optional: OpenAI Configuration\n")
            f.write("# OPENAI_API_KEY=your_key_here\n")
            f.write("# USE_OLLAMA=false  # Set to false to use OpenAI\n")
            f.write("\n")
            f.write("# Privacy Settings\n")
            f.write("COPPA_COMPLIANT=true\n")
            f.write("SESSION_ONLY_MEMORY=true\n")
            f.write("NO_DATA_PERSISTENCE=true\n")
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")
    
    # Step 4: Verify installation
    print_header("Step 4: Verification")
    
    print("Testing AI imports...")
    try:
        import langchain
        print("✓ LangChain installed")
    except ImportError:
        print("✗ LangChain not found")
    
    try:
        import openai
        print("✓ OpenAI SDK installed")
    except ImportError:
        print("✗ OpenAI SDK not found")
    
    try:
        import chromadb
        print("✓ ChromaDB installed")
    except ImportError:
        print("✗ ChromaDB not found")
    
    # Test Ollama
    ollama_test = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
    if ollama_test.returncode == 0:
        print("✓ Ollama is running")
        print("Available models:")
        print(ollama_test.stdout)
    else:
        print("⚠ Ollama not running (optional)")
    
    # Step 5: Next steps
    print_header("Setup Complete!")
    
    print("🎉 AI-Powered mode is ready!\n")
    print("To start the AI-powered tutor:")
    print("  python app/ai_app.py\n")
    print("The AI will:")
    print("  • Understand natural language")
    print("  • Extract names, ages, and context")
    print("  • Provide personalized responses")
    print("  • Adapt to each child's needs\n")
    
    if not os.getenv("OPENAI_API_KEY") and ollama_test.returncode != 0:
        print("⚠️  Note: No AI backend detected!")
        print("  Either:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Or add OpenAI API key to .env file")

if __name__ == "__main__":
    setup_ai_mode()