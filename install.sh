#!/bin/bash

# KidSafe Alphabet Tutor - Automated Installation Script
# Author: Nouran Darwish

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}   KidSafe Alphabet Tutor - Installation${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

# Start installation
print_header

# Step 1: Check Python
echo "Step 1: Checking Python installation..."
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    REQUIRED_VERSION="3.10"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        print_success "Python $PYTHON_VERSION meets requirements (>= $REQUIRED_VERSION)"
    else
        print_error "Python $PYTHON_VERSION is below required version $REQUIRED_VERSION"
        exit 1
    fi
else
    print_error "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi
echo ""

# Step 2: Check and create virtual environment
echo "Step 2: Setting up virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Virtual environment recreated"
    fi
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"
echo ""

# Step 3: Upgrade pip
echo "Step 3: Upgrading pip..."
pip install --quiet --upgrade pip
print_success "pip upgraded to $(pip --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
echo ""

# Step 4: Install dependencies
echo "Step 4: Installing dependencies..."
echo "Please select installation type:"
echo "  1) Quick (Minimal - UI only, ~2 min)"
echo "  2) Standard (Full Python packages, ~5 min)"
echo "  3) Complete (With AI models, ~15 min)"
read -p "Enter choice [1-3]: " -n 1 -r
echo ""

case $REPLY in
    1)
        print_info "Installing minimal dependencies..."
        pip install --quiet gradio numpy loguru python-dotenv
        print_success "Minimal dependencies installed"
        INSTALL_TYPE="quick"
        ;;
    2)
        print_info "Installing standard dependencies..."
        if [ -f "requirements.txt" ]; then
            pip install --quiet -r requirements.txt
        else
            pip install --quiet \
                gradio==4.19.2 \
                numpy==1.24.3 \
                loguru==0.7.2 \
                python-dotenv==1.0.0 \
                pillow==10.2.0 \
                opencv-python==4.9.0.80 \
                pytesseract==0.3.10
        fi
        print_success "Standard dependencies installed"
        INSTALL_TYPE="standard"
        ;;
    3)
        print_info "Installing complete dependencies with AI models..."
        if [ -f "requirements.txt" ]; then
            pip install --quiet -r requirements.txt
        fi
        
        # Additional AI packages
        print_info "Installing AI packages (this may take a while)..."
        pip install --quiet \
            faster-whisper \
            ultralytics \
            torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        
        print_success "All dependencies installed"
        
        # Download models
        read -p "Download AI models now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Downloading models..."
            python3 -c "
from faster_whisper import WhisperModel
print('Downloading Whisper model...')
model = WhisperModel('tiny.en', device='cpu')
print('✅ Whisper model downloaded')
            " || print_warning "Whisper download failed"
            
            python3 -c "
from ultralytics import YOLO
print('Downloading YOLO model...')
model = YOLO('yolov8n.pt')
print('✅ YOLO model downloaded')
            " || print_warning "YOLO download failed"
        fi
        INSTALL_TYPE="complete"
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac
echo ""

# Step 5: Check system dependencies
echo "Step 5: Checking system dependencies..."
MISSING_DEPS=""

check_command tesseract || MISSING_DEPS="$MISSING_DEPS tesseract"
check_command ffmpeg || MISSING_DEPS="$MISSING_DEPS ffmpeg"

if [ ! -z "$MISSING_DEPS" ]; then
    print_warning "Missing system dependencies:$MISSING_DEPS"
    echo "Install them with:"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  sudo apt-get install$MISSING_DEPS"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install$MISSING_DEPS"
    fi
fi
echo ""

# Step 6: Create environment file
echo "Step 6: Setting up environment..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
    else
        cat > .env << EOF
# Auto-generated environment file
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
DEBUG=false
LOG_LEVEL=INFO
EOF
        print_success "Environment file created"
    fi
else
    print_info "Environment file already exists"
fi
echo ""

# Step 7: Run tests
echo "Step 7: Running tests..."
if [ -f "test_components.py" ]; then
    python test_components.py > /dev/null 2>&1 && \
        print_success "Component tests passed" || \
        print_warning "Some tests failed (non-critical)"
fi

if [ -f "tests/test_acceptance.py" ] && [ "$INSTALL_TYPE" != "quick" ]; then
    python tests/test_acceptance.py > /dev/null 2>&1 && \
        print_success "Acceptance tests passed" || \
        print_warning "Some acceptance tests failed (expected without models)"
fi
echo ""

# Step 8: Create start script
echo "Step 8: Creating start script..."
cat > start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
echo "Starting KidSafe Alphabet Tutor..."
echo "Opening browser at http://localhost:7860"
python app/gradio_ui_simple.py
EOF
chmod +x start.sh
print_success "Start script created"
echo ""

# Final message
print_header
print_success "Installation Complete!"
echo ""
echo "Installation type: $INSTALL_TYPE"
echo ""
echo "To start the application:"
echo "  1. Run: ${GREEN}./start.sh${NC}"
echo "  2. Open browser at: ${GREEN}http://localhost:7860${NC}"
echo ""
echo "For manual start:"
echo "  1. Activate venv: ${GREEN}source venv/bin/activate${NC}"
echo "  2. Run app: ${GREEN}python app/gradio_ui_simple.py${NC}"
echo ""

if [ "$INSTALL_TYPE" = "quick" ]; then
    print_info "You installed the minimal version."
    echo "To add more features, run this script again and choose option 2 or 3."
fi

echo ""
print_info "For help, see USER_GUIDE.md"
print_info "For technical details, see TECHNICAL_GUIDE.md"
echo ""
echo "Enjoy teaching the alphabet with Bubbly! 🫧"