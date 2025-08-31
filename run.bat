@echo off
REM Activate virtual environment if it exists
if exist "venv" (
    call venv\Scripts\activate.bat
)

REM Start the application
echo Starting KidSafe Alphabet Tutor...
python app\gradio_ui_simple.py
pause
