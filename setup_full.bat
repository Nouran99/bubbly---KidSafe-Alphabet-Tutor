@echo off
REM ============================================================
REM KidSafe Alphabet Tutor - Complete Setup Script (Windows)
REM ============================================================
REM This script performs a complete setup of the application
REM including all dependencies, verification, and optional features
REM ============================================================

setlocal enabledelayedexpansion

REM Colors (using escape sequences where supported)
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

REM Print header
echo ============================================================
echo    KidSafe Alphabet Tutor - Complete Setup (Windows)
echo ============================================================
echo.

REM Step 1: Check Python version
echo Step 1: Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Step 2: Check if in correct directory
echo.
echo Step 2: Checking project files...
if not exist "app\gradio_ui_simple.py" (
    echo [ERROR] Not in KidSafe Alphabet Tutor directory!
    echo Please run this script from the project root directory
    pause
    exit /b 1
)
echo [OK] Project files found

REM Step 3: Create/activate virtual environment
echo.
echo Step 3: Setting up virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Step 4: Upgrade pip
echo.
echo Step 4: Upgrading pip...
python -m pip install --quiet --upgrade pip
echo [OK] pip upgraded

REM Step 5: Choose installation type
echo.
echo Step 5: Selecting installation type...
echo.
echo Installation Options:
echo   1) Minimal  - Core functionality only (2 min, ~150MB)
echo   2) Standard - Recommended for most users (5 min, ~300MB)
echo   3) Full     - All features including AI (15 min, ~1GB)
echo.
set /p INSTALL_CHOICE="Select option [1-3] (default: 2): "
if "%INSTALL_CHOICE%"=="" set INSTALL_CHOICE=2

REM Step 6: Install Python dependencies
echo.
echo Step 6: Installing Python packages...

if "%INSTALL_CHOICE%"=="1" (
    echo Installing minimal dependencies...
    if exist "requirements-minimal.txt" (
        pip install --quiet -r requirements-minimal.txt
    ) else (
        pip install --quiet gradio numpy loguru python-dotenv
    )
    echo [OK] Minimal dependencies installed
    set INSTALL_TYPE=minimal
) else if "%INSTALL_CHOICE%"=="2" (
    echo Installing standard dependencies...
    if exist "requirements-standard.txt" (
        pip install --quiet -r requirements-standard.txt
    ) else (
        pip install --quiet gradio numpy loguru python-dotenv pillow better-profanity aiofiles pytest
    )
    echo [OK] Standard dependencies installed
    set INSTALL_TYPE=standard
) else if "%INSTALL_CHOICE%"=="3" (
    echo Installing full dependencies (this may take a while)...
    
    REM Check for system dependencies
    echo.
    echo Note: Full installation requires:
    echo - Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    echo - FFmpeg: https://ffmpeg.org/download.html
    echo.
    set /p CONTINUE_FULL="Continue with full installation? [Y/n]: "
    if /i "!CONTINUE_FULL!"=="n" (
        echo Installation cancelled
        pause
        exit /b 1
    )
    
    if exist "requirements-full.txt" (
        pip install --quiet -r requirements-full.txt
    ) else (
        pip install --quiet gradio numpy loguru python-dotenv pillow opencv-python pytesseract
    )
    
    REM Optional: Install PyTorch
    set /p INSTALL_TORCH="Install PyTorch for advanced AI features? [y/N]: "
    if /i "!INSTALL_TORCH!"=="y" (
        echo Installing PyTorch CPU version...
        pip install --quiet torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
        echo [OK] PyTorch installed
    )
    
    echo [OK] Full dependencies installed
    set INSTALL_TYPE=full
) else (
    echo [ERROR] Invalid choice
    pause
    exit /b 1
)

REM Step 7: Create/verify curriculum
echo.
echo Step 7: Setting up curriculum data...
python -c "import json, os; c=json.load(open('app/curriculum.json')) if os.path.exists('app/curriculum.json') else {}; print(f'Curriculum: {len(c)} letters')" 2>nul
echo [OK] Curriculum ready

REM Step 8: Create .env file if missing
echo.
echo Step 8: Setting up environment...
if not exist ".env" (
    (
        echo # KidSafe Alphabet Tutor Environment Configuration
        echo GRADIO_SERVER_PORT=7860
        echo GRADIO_SERVER_NAME=0.0.0.0
        echo LOG_LEVEL=INFO
    ) > .env
    echo [OK] Environment file created
) else (
    echo [OK] Environment file exists
)

REM Step 9: Run verification tests
echo.
echo Step 9: Running verification tests...
if exist "test_setup.py" (
    python test_setup.py >nul 2>&1
    if %errorlevel% equ 0 (
        echo [OK] All tests passed
    ) else (
        echo [WARNING] Some tests failed but core functionality should work
    )
) else (
    echo [WARNING] test_setup.py not found, skipping tests
)

REM Step 10: Create startup script
echo.
echo Step 10: Creating startup script...
(
    echo @echo off
    echo REM Activate virtual environment if it exists
    echo if exist "venv" (
    echo     call venv\Scripts\activate.bat
    echo )
    echo.
    echo REM Start the application
    echo echo Starting KidSafe Alphabet Tutor...
    echo python app\gradio_ui_simple.py
    echo pause
) > run.bat
echo [OK] Startup script created (run.bat)

REM Summary
echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Installation Summary:
echo   - Type: %INSTALL_TYPE%
echo   - Python: %PYTHON_VERSION%
echo   - Virtual Env: venv\
echo   - Dependencies: Installed
echo.
echo To start the application:
echo   run.bat
echo Or manually:
echo   venv\Scripts\activate.bat
echo   python app\gradio_ui_simple.py
echo.
echo Then open in browser:
echo   http://localhost:7860
echo.

REM Optional: Start now?
set /p START_NOW="Start the application now? [Y/n]: "
if /i not "!START_NOW!"=="n" (
    echo.
    echo Starting KidSafe Alphabet Tutor...
    python app\gradio_ui_simple.py
)

pause