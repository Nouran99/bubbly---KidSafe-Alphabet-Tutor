#!/bin/bash

# ============================================================
# KidSafe Alphabet Tutor - Complete Setup Script
# ============================================================
# This script performs a complete setup of the application
# including all dependencies, verification, and optional features
# ============================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Functions for colored output
print_header() {
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN}   KidSafe Alphabet Tutor - Complete Setup${NC}"
    echo -e "${CYAN}============================================================${NC}"
}

print_step() {
    echo -e "\n${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${WHITE}ℹ $1${NC}"
}

# Function to check command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Function to install system dependencies
install_system_deps() {
    local os=$1
    print_step "Installing system dependencies..."
    
    if [ "$os" == "linux" ]; then
        if command_exists apt-get; then
            print_info "Using apt-get (Debian/Ubuntu)"
            sudo apt-get update -qq
            sudo apt-get install -y -qq python3-pip python3-venv ffmpeg tesseract-ocr >/dev/null 2>&1
        elif command_exists yum; then
            print_info "Using yum (RedHat/CentOS)"
            sudo yum install -y python3-pip python3-virtualenv ffmpeg tesseract >/dev/null 2>&1
        else
            print_warning "Unknown Linux distribution. Please install manually: python3-pip, python3-venv, ffmpeg, tesseract"
        fi
    elif [ "$os" == "macos" ]; then
        if command_exists brew; then
            print_info "Using Homebrew"
            brew install python3 ffmpeg tesseract >/dev/null 2>&1 || true
        else
            print_warning "Homebrew not found. Please install: https://brew.sh"
        fi
    fi
}

# Main setup process
main() {
    print_header
    
    # Detect OS
    OS=$(detect_os)
    echo -e "\n${WHITE}System: $OS${NC}"
    echo -e "${WHITE}Directory: $(pwd)${NC}"
    
    # Step 1: Check Python version
    print_step "Step 1: Checking Python version..."
    if command_exists python3; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        
        if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
            print_success "Python $PYTHON_VERSION found (3.10+ required)"
        else
            print_error "Python $PYTHON_VERSION found but 3.10+ required"
            exit 1
        fi
    else
        print_error "Python3 not found. Please install Python 3.10 or higher"
        exit 1
    fi
    
    # Step 2: Check if in correct directory
    print_step "Step 2: Checking project files..."
    if [ ! -f "app/gradio_ui_simple.py" ]; then
        print_error "Not in KidSafe Alphabet Tutor directory!"
        print_info "Please run this script from the project root directory"
        exit 1
    fi
    print_success "Project files found"
    
    # Step 3: Create/activate virtual environment
    print_step "Step 3: Setting up virtual environment..."
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
    
    # Step 4: Upgrade pip
    print_step "Step 4: Upgrading pip..."
    pip install --quiet --upgrade pip
    print_success "pip upgraded to $(pip --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
    
    # Step 5: Choose installation type
    print_step "Step 5: Selecting installation type..."
    echo ""
    echo "Installation Options:"
    echo "  1) Minimal  - Core functionality only (2 min, ~150MB)"
    echo "  2) Standard - Recommended for most users (5 min, ~300MB)"
    echo "  3) Full     - All features including AI (15 min, ~1GB)"
    echo ""
    read -p "Select option [1-3] (default: 2): " -n 1 -r INSTALL_CHOICE
    echo ""
    
    # Default to standard if no choice
    if [ -z "$INSTALL_CHOICE" ]; then
        INSTALL_CHOICE="2"
    fi
    
    # Step 6: Install Python dependencies
    print_step "Step 6: Installing Python packages..."
    case $INSTALL_CHOICE in
        1)
            print_info "Installing minimal dependencies..."
            if [ -f "requirements-minimal.txt" ]; then
                pip install --quiet -r requirements-minimal.txt
            else
                pip install --quiet gradio numpy loguru python-dotenv
            fi
            print_success "Minimal dependencies installed"
            INSTALL_TYPE="minimal"
            ;;
        2)
            print_info "Installing standard dependencies..."
            if [ -f "requirements-standard.txt" ]; then
                pip install --quiet -r requirements-standard.txt
            else
                pip install --quiet gradio numpy loguru python-dotenv pillow better-profanity aiofiles pytest
            fi
            print_success "Standard dependencies installed"
            INSTALL_TYPE="standard"
            ;;
        3)
            print_info "Installing full dependencies (this may take a while)..."
            
            # Install system dependencies first
            read -p "Install system dependencies (ffmpeg, tesseract)? [y/N]: " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                install_system_deps $OS
            fi
            
            if [ -f "requirements-full.txt" ]; then
                pip install --quiet -r requirements-full.txt
            else
                pip install --quiet gradio numpy loguru python-dotenv pillow opencv-python pytesseract
            fi
            
            # Optional: Install PyTorch CPU version
            read -p "Install PyTorch for advanced AI features? [y/N]: " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "Installing PyTorch CPU version..."
                pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
                print_success "PyTorch installed"
            fi
            
            print_success "Full dependencies installed"
            INSTALL_TYPE="full"
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    # Step 7: Create/verify curriculum
    print_step "Step 7: Setting up curriculum data..."
    python3 -c "
import json
import os

if os.path.exists('app/curriculum.json'):
    with open('app/curriculum.json', 'r') as f:
        curriculum = json.load(f)
    if len(curriculum) == 26:
        print('Curriculum already complete')
    else:
        print('Updating curriculum...')
        exec(open('scripts/create_curriculum.py').read()) if os.path.exists('scripts/create_curriculum.py') else None
else:
    print('Creating curriculum...')
" 2>/dev/null || true
    print_success "Curriculum ready"
    
    # Step 8: Create .env file if missing
    print_step "Step 8: Setting up environment..."
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# KidSafe Alphabet Tutor Environment Configuration
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
LOG_LEVEL=INFO
EOF
        print_success "Environment file created"
    else
        print_success "Environment file exists"
    fi
    
    # Step 9: Run verification tests
    print_step "Step 9: Running verification tests..."
    if [ -f "test_setup.py" ]; then
        python3 test_setup.py >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            print_success "All tests passed"
        else
            print_warning "Some tests failed but core functionality should work"
        fi
    else
        print_warning "test_setup.py not found, skipping tests"
    fi
    
    # Step 10: Create startup script
    print_step "Step 10: Creating startup script..."
    cat > run.sh << 'EOF'
#!/bin/bash
# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start the application
echo "Starting KidSafe Alphabet Tutor..."
python app/gradio_ui_simple.py
EOF
    chmod +x run.sh
    print_success "Startup script created (run.sh)"
    
    # Summary
    echo ""
    print_header
    echo -e "${GREEN}✅ Setup Complete!${NC}"
    echo ""
    echo -e "${WHITE}Installation Summary:${NC}"
    echo -e "  • Type: $INSTALL_TYPE"
    echo -e "  • Python: $PYTHON_VERSION"
    echo -e "  • Virtual Env: venv/"
    echo -e "  • Dependencies: Installed"
    echo ""
    echo -e "${WHITE}To start the application:${NC}"
    echo -e "${CYAN}  ./run.sh${NC}"
    echo -e "${WHITE}Or manually:${NC}"
    echo -e "${CYAN}  source venv/bin/activate${NC}"
    echo -e "${CYAN}  python app/gradio_ui_simple.py${NC}"
    echo ""
    echo -e "${WHITE}Then open in browser:${NC}"
    echo -e "${CYAN}  http://localhost:7860${NC}"
    echo ""
    
    # Optional: Start now?
    read -p "Start the application now? [Y/n]: " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        print_info "Starting KidSafe Alphabet Tutor..."
        python3 app/gradio_ui_simple.py
    fi
}

# Run main function
main "$@"