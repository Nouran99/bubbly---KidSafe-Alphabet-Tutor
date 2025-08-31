#!/bin/bash
# Fix for Gradio ASGI TypeError on Linux/Mac

echo "============================================================"
echo "   Fixing Gradio ASGI Error"
echo "============================================================"
echo ""

# Step 1: Uninstall potentially conflicting versions
echo "Step 1: Removing conflicting packages..."
pip uninstall -y gradio gradio-client 2>/dev/null
echo "✓ Old packages removed"

# Step 2: Install fixed versions
echo ""
echo "Step 2: Installing compatible versions..."
pip install gradio==4.19.2 gradio_client==0.10.1
echo "✓ Compatible versions installed"

# Step 3: Apply code fix
echo ""
echo "Step 3: Applying code fixes..."
python fix_gradio_error.py 2>/dev/null || python3 fix_gradio_error.py 2>/dev/null
echo "✓ Code fixes applied"

# Step 4: Test import
echo ""
echo "Step 4: Testing installation..."
python -c "import gradio; print(f'Gradio {gradio.__version__} installed successfully')" || \
python3 -c "import gradio; print(f'Gradio {gradio.__version__} installed successfully')"

echo ""
echo "============================================================"
echo "   Fix Complete!"
echo "============================================================"
echo ""
echo "You can now run the app with:"
echo "   python app/gradio_ui_simple.py"
echo ""