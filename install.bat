@echo off
REM KidSafe Alphabet Tutor - Windows Installation Script
REM Author: Nouran Darwish

setlocal enabledelayedexpansion

echo ================================================
echo    KidSafe Alphabet Tutor - Installation
echo ================================================
echo.

REM Check Python
echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Check/Create virtual environment
echo Step 2: Setting up virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists
    set /p RECREATE="Recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo [OK] Virtual environment recreated
    )
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Step 3: Upgrading pip...
python -m pip install --quiet --upgrade pip
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Step 4: Installing dependencies...
echo Please select installation type:
echo   1) Quick (Minimal - UI only, ~2 min)
echo   2) Standard (Full Python packages, ~5 min)  
echo   3) Complete (With AI models, ~15 min)
set /p CHOICE="Enter choice [1-3]: "

if "%CHOICE%"=="1" (
    echo Installing minimal dependencies...
    pip install --quiet gradio numpy loguru python-dotenv
    echo [OK] Minimal dependencies installed
    set INSTALL_TYPE=quick
) else if "%CHOICE%"=="2" (
    echo Installing standard dependencies...
    if exist requirements.txt (
        pip install --quiet -r requirements.txt
    ) else (
        pip install --quiet gradio==4.19.2 numpy==1.24.3 loguru==0.7.2 python-dotenv==1.0.0 pillow==10.2.0 opencv-python==4.9.0.80 pytesseract==0.3.10
    )
    echo [OK] Standard dependencies installed
    set INSTALL_TYPE=standard
) else if "%CHOICE%"=="3" (
    echo Installing complete dependencies...
    if exist requirements.txt (
        pip install --quiet -r requirements.txt
    )
    echo Installing AI packages (this may take a while)...
    pip install --quiet faster-whisper ultralytics torch torchvision torchaudio
    echo [OK] All dependencies installed
    
    set /p DOWNLOAD_MODELS="Download AI models now? (y/n): "
    if /i "!DOWNLOAD_MODELS!"=="y" (
        echo Downloading models...
        python -c "from faster_whisper import WhisperModel; model = WhisperModel('tiny.en', device='cpu'); print('Whisper model downloaded')"
        python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('YOLO model downloaded')"
    )
    set INSTALL_TYPE=complete
) else (
    echo [ERROR] Invalid choice
    pause
    exit /b 1
)
echo.

REM Check system dependencies
echo Step 5: Checking system dependencies...
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Tesseract OCR not found
    echo Download from: https://github.com/UB-Mannheim/tesseract/wiki
)

where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg not found
    echo Download from: https://ffmpeg.org/download.html
)
echo.

REM Create environment file
echo Step 6: Setting up environment...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] Environment file created from template
    ) else (
        (
            echo # Auto-generated environment file
            echo GRADIO_SERVER_NAME=0.0.0.0
            echo GRADIO_SERVER_PORT=7860
            echo DEBUG=false
            echo LOG_LEVEL=INFO
        ) > .env
        echo [OK] Environment file created
    )
) else (
    echo [INFO] Environment file already exists
)
echo.

REM Run tests
echo Step 7: Running tests...
if exist test_components.py (
    python test_components.py >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] Component tests passed
    ) else (
        echo [WARNING] Some tests failed (non-critical)
    )
)
echo.

REM Create start script
echo Step 8: Creating start script...
(
    echo @echo off
    echo call venv\Scripts\activate.bat
    echo echo Starting KidSafe Alphabet Tutor...
    echo echo Opening browser at http://localhost:7860
    echo start http://localhost:7860
    echo python app\gradio_ui_simple.py
) > start.bat
echo [OK] Start script created
echo.

REM Final message
echo ================================================
echo    Installation Complete!
echo ================================================
echo.
echo Installation type: %INSTALL_TYPE%
echo.
echo To start the application:
echo   1. Run: start.bat
echo   2. Browser will open automatically
echo.
echo For manual start:
echo   1. Run: venv\Scripts\activate.bat
echo   2. Run: python app\gradio_ui_simple.py
echo.

if "%INSTALL_TYPE%"=="quick" (
    echo [INFO] You installed the minimal version.
    echo To add more features, run this script again and choose option 2 or 3.
)

echo.
echo For help, see USER_GUIDE.md
echo For technical details, see TECHNICAL_GUIDE.md
echo.
echo Enjoy teaching the alphabet with Bubbly!
echo.
pause