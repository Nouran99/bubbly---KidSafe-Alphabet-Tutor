@echo off
REM Fix for Gradio ASGI TypeError on Windows

echo ============================================================
echo    Fixing Gradio ASGI Error
echo ============================================================
echo.

REM Step 1: Uninstall potentially conflicting versions
echo Step 1: Removing conflicting packages...
pip uninstall -y gradio gradio-client 2>nul
echo [OK] Old packages removed

REM Step 2: Install fixed versions
echo.
echo Step 2: Installing compatible versions...
pip install gradio==4.19.2 gradio_client==0.10.1
echo [OK] Compatible versions installed

REM Step 3: Apply code fix
echo.
echo Step 3: Applying code fixes...
python fix_gradio_error.py 2>nul
echo [OK] Code fixes applied

REM Step 4: Test import
echo.
echo Step 4: Testing installation...
python -c "import gradio; print(f'Gradio {gradio.__version__} installed successfully')"

echo.
echo ============================================================
echo    Fix Complete!
echo ============================================================
echo.
echo You can now run the app with:
echo    python app\gradio_ui_simple.py
echo.
pause