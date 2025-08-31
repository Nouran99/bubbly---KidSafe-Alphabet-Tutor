# How to Run KidSafe Alphabet Tutor

## For Windows Users (Your Case)

Since you already have the project cloned at:
`E:\My_Projects\Interviews tasks\bubbly---KidSafe-Alphabet-Tutor`

### Step 1: Update Your Local Copy
```cmd
git pull origin main
```

### Step 2: Install/Update Dependencies
```cmd
pip uninstall -y gradio gradio-client
pip install -r requirements-minimal.txt
```

### Step 3: Run the Application
```cmd
python app\gradio_ui_simple.py
```

That's it! The app will start at http://localhost:7860

## Fresh Installation (Any Platform)

```bash
# 1. Clone
git clone https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor.git
cd bubbly---KidSafe-Alphabet-Tutor

# 2. Install
pip install -r requirements-minimal.txt

# 3. Run
python app/gradio_ui_simple.py
```

## What Was Fixed

✅ Gradio ASGI error - Fixed by using compatible versions
✅ Requirements - All updated to working versions
✅ Removed 17 unnecessary files
✅ Simplified to just the essentials

## Files You Need

Essential files only:
- `app/gradio_ui_simple.py` - Main application
- `app/state.py` - Memory management
- `agents/crew_setup_simple.py` - Agent system
- `requirements-minimal.txt` - Dependencies

## If You Have Issues

The most common fix:
```cmd
pip uninstall -y gradio gradio-client
pip install gradio==4.19.2 gradio_client==0.10.1 numpy loguru python-dotenv
python app\gradio_ui_simple.py
```