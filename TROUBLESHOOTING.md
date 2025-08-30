# Troubleshooting Guide

## Common Setup Issues and Solutions

### 1. Application Won't Start

**Symptom**: Error when running `python app/gradio_ui_simple.py`

**Solutions**:
```bash
# 1. Ensure all dependencies are installed
pip install -r requirements-minimal.txt

# 2. Test the setup
python test_setup.py

# 3. Check for missing packages
python diagnose.py
```

### 2. Import Errors

**Symptom**: `ModuleNotFoundError` or `ImportError`

**Solutions**:
```bash
# Install missing core packages
pip install gradio numpy loguru python-dotenv

# Verify Python version (must be 3.10+)
python --version
```

### 3. Port Already in Use

**Symptom**: `[Errno 48] Address already in use` or similar

**Solutions**:
```bash
# Find and kill process using port 7860
lsof -i :7860  # Find process
kill -9 <PID>  # Kill process

# Or use a different port
python -c "import os; os.environ['GRADIO_SERVER_PORT']='7861'; exec(open('app/gradio_ui_simple.py').read())"
```

### 4. Curriculum Not Loading

**Symptom**: Application starts but no letters available

**Solution**:
```bash
# Verify curriculum file exists and is complete
python -c "import json; c=json.load(open('app/curriculum.json')); print(f'Letters: {len(c)}')"

# If missing or incomplete, the setup will recreate it
python test_setup.py
```

### 5. Memory Errors

**Symptom**: `AttributeError` related to SessionMemory

**Solution**:
```bash
# Ensure app/state.py is not corrupted
python -c "from app.state import SessionMemory; print('✓ Memory module OK')"
```

### 6. Agent System Not Responding

**Symptom**: No response when typing messages

**Solution**:
```bash
# Test agent system directly
python -c "
from app.state import SessionMemory
from agents.crew_setup_simple import AlphabetTutorAgents
m = SessionMemory()
a = AlphabetTutorAgents(m)
r = a.process_interaction('Hello')
print('Response:', r['response'] if isinstance(r, dict) else r)
"
```

### 7. UI Not Loading

**Symptom**: Browser shows error or blank page

**Solutions**:
- Clear browser cache
- Try different browser
- Check console for JavaScript errors (F12)
- Ensure JavaScript is enabled

### 8. Slow Performance

**Symptom**: Application is very slow to respond

**Solutions**:
- Use minimal installation (not full)
- Close other applications
- Restart the application
- Check CPU/memory usage

## Quick Diagnostic Commands

### Test Everything
```bash
python test_setup.py
```

### Check Dependencies
```bash
python diagnose.py
```

### Verify Core Functionality
```bash
python final_test.py
```

### Manual Start with Logging
```bash
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
exec(open('app/gradio_ui_simple.py').read())
"
```

## Environment Variables

The app uses these environment variables (in `.env` file):
```
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

Modify if needed for your environment.

## Still Having Issues?

1. **Check Python Version**: Must be 3.10 or higher
   ```bash
   python --version
   ```

2. **Clean Install**:
   ```bash
   # Remove and reinstall packages
   pip uninstall gradio numpy loguru -y
   pip install -r requirements-minimal.txt
   ```

3. **Use Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements-minimal.txt
   ```

4. **Check Repository**:
   ```bash
   # Ensure you have the latest code
   git pull origin main
   ```

## Contact

If issues persist after trying these solutions:
1. Run `python diagnose.py > diagnostic_output.txt`
2. Check the error messages carefully
3. Open an issue on GitHub with the diagnostic output