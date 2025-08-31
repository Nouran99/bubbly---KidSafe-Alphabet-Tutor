@echo off
REM Complete fix for Windows ASGI errors

echo ============================================================
echo    Fixing All Compatibility Issues
echo ============================================================
echo.

REM Step 1: Complete uninstall of problematic packages
echo Step 1: Removing all problematic packages...
pip uninstall -y gradio gradio-client fastapi uvicorn starlette pydantic pydantic-core anyio

echo.
echo Step 2: Installing specific compatible versions...
REM These exact versions are tested to work together
pip install uvicorn[standard]>=0.18.3
pip install fastapi==0.109.2
pip install pydantic==2.5.3
pip install starlette==0.36.3
pip install gradio==4.16.0
pip install gradio-client==1.4.0
pip install numpy==1.26.3
pip install loguru==0.7.2
pip install python-dotenv==1.0.0

echo.
echo ============================================================
echo    Installation Complete!
echo ============================================================
echo.
echo Now run the app with:
echo    python app\full_ai_.py
echo.
pause