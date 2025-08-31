# 🔧 Troubleshooting Guide

## Quick Solutions for Common Issues

### 🚨 Critical Fixes

#### Windows ASGI/Pydantic Error
**Error**: `TypeError: AsyncConnectionPool.__init__() got an unexpected keyword argument 'socket_options'`
**Solution**:
```bash
python setup.py --fix-windows
```

#### Application Won't Start
**Error**: Various import or startup errors
**Solution**:
```bash
# Reinstall with compatible versions
python setup.py --simple
```

---

## 📋 Common Issues and Solutions

### 1. Installation Issues

#### ❌ "Python not found"
**Solution**:
- Install Python 3.8 or higher from [python.org](https://python.org)
- Add Python to PATH during installation
- Verify: `python --version`

#### ❌ "pip not found"
**Solution**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### ❌ Virtual environment not activating
**Windows**:
```bash
# If Scripts not found
python -m venv venv
venv\Scripts\activate.bat  # or .ps1 for PowerShell
```

**Mac/Linux**:
```bash
source venv/bin/activate
# If permission denied
chmod +x venv/bin/activate
```

### 2. Dependency Issues

#### ❌ "No module named 'gradio'"
**Solution**:
```bash
pip install gradio==4.16.0
# Or run full setup
python setup.py --simple
```

#### ❌ Version conflict errors
**Solution**:
```bash
# Uninstall all and reinstall
pip uninstall gradio fastapi pydantic starlette uvicorn -y
pip install -r requirements.txt
```

#### ❌ "Microsoft Visual C++ 14.0 required" (Windows)
**Solution**:
- Download Visual Studio Build Tools
- Or use pre-built wheels:
```bash
pip install --only-binary :all: -r requirements.txt
```

### 3. Runtime Errors

#### ❌ Port 7860 already in use
**Solution**:

**Windows**:
```bash
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

**Mac/Linux**:
```bash
fuser -k 7860/tcp
# Or
lsof -ti:7860 | xargs kill -9
```

**Alternative**: Change port in `simple_app.py`:
```python
server_port=7861  # Use different port
```

#### ❌ "Connection refused" in browser
**Causes & Solutions**:
1. **Application not running**: Start with `python app/simple_app.py`
2. **Firewall blocking**: Allow Python through firewall
3. **Wrong URL**: Use `http://localhost:7860` (not https)
4. **Browser cache**: Clear cache or try incognito mode

#### ❌ Gradio interface not loading
**Solutions**:
1. Clear browser cache (Ctrl+F5)
2. Try different browser
3. Disable browser extensions
4. Check console for errors (F12)

### 4. Functional Issues

#### ❌ Bubbly doesn't respond
**Solutions**:
1. Click "Clear Chat" and try again
2. Refresh the page
3. Check if application is still running
4. Look for errors in terminal

#### ❌ Letters not progressing
**Solutions**:
1. Use clear commands: "Next letter" or "Teach me B"
2. Clear chat and restart
3. Check `curriculum.json` exists and is valid

#### ❌ Speech recognition not working
**Note**: Simple mode doesn't include speech features by default
**Solution**: Install full mode:
```bash
python setup.py --full
```

### 5. Platform-Specific Issues

#### Windows Specific

##### ❌ PowerShell execution policy error
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

##### ❌ Path too long error
**Solution**:
- Move project to shorter path (e.g., `C:\kidsafe\`)
- Enable long paths in Windows:
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

#### Mac Specific

##### ❌ SSL certificate error
**Solution**:
```bash
pip install --upgrade certifi
```

##### ❌ Permission denied errors
**Solution**:
```bash
sudo chmod -R 755 .
```

#### Linux Specific

##### ❌ Missing system dependencies
**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Fedora/RHEL
sudo dnf install python3-pip python3-virtualenv
```

### 6. Performance Issues

#### ❌ Application running slowly
**Solutions**:
1. Close other applications
2. Ensure at least 4GB RAM available
3. Use simple mode instead of full
4. Restart the application

#### ❌ High CPU usage
**Solutions**:
1. Check for infinite loops in terminal
2. Restart application
3. Use simple mode
4. Update to latest code

### 7. Data and State Issues

#### ❌ Progress not saving
**Note**: This is by design! No data is saved for privacy.
**Workaround**: Parents can track progress manually

#### ❌ Session memory full
**Solution**: The app automatically manages memory. If issues:
```python
# In simple_app.py, increase buffer:
session_memory = SessionMemory(max_turns=5)  # Default is 3
```

## 🛠️ Diagnostic Tools

### Run System Check
```bash
python diagnose.py
```
This will check:
- Python version
- Required packages
- File integrity
- System resources

### Run Compatibility Check
```bash
python check_compatibility.py
```
This verifies:
- All files present
- Imports working
- Version compatibility
- Configuration validity

### Check Logs
**Enable debug logging**:
```python
# Add to simple_app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```bash
# Test imports
python -c "import gradio; print(gradio.__version__)"
python -c "from app.state import SessionMemory; print('OK')"

# Test curriculum
python -c "import json; json.load(open('app/curriculum.json')); print('Valid')"
```

## 🔄 Reset and Cleanup

### Complete Reset
```bash
# 1. Stop application (Ctrl+C)

# 2. Clean Python cache
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null
find . -name "*.pyc" -delete

# 3. Reinstall
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
python setup.py --simple

# 4. Start fresh
python app/simple_app.py
```

### Clear Temporary Files
**Windows**:
```bash
del /S /Q *.pyc
rmdir /S /Q __pycache__
```

**Mac/Linux**:
```bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete
```

## 📞 Getting Help

### Before Asking for Help

1. **Check this guide** - Your issue might be listed
2. **Run diagnostics** - `python diagnose.py`
3. **Check compatibility** - `python check_compatibility.py`
4. **Read error messages** - They often indicate the solution
5. **Try the Windows fix** - `python setup.py --fix-windows`

### Information to Provide

When reporting issues, include:
1. **Operating System**: Windows/Mac/Linux version
2. **Python Version**: `python --version`
3. **Error Message**: Complete error text
4. **Steps to Reproduce**: What you did before the error
5. **Diagnostic Output**: Results from `diagnose.py`

### Quick Checklist

Before reporting an issue, verify:
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`python setup.py --simple`)
- [ ] Using correct URL (`http://localhost:7860`)
- [ ] No firewall blocking
- [ ] Port 7860 available

## 💡 Pro Tips

1. **Always use virtual environment** - Prevents conflicts
2. **Run setup after pulling updates** - Ensures compatibility
3. **Use simple mode first** - Fewer dependencies, fewer issues
4. **Keep terminal open** - Watch for error messages
5. **Try different browser** - Sometimes browser-specific issues occur

## 🔗 Additional Resources

- [GitHub Issues](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor/issues)
- [Python Documentation](https://docs.python.org/3/)
- [Gradio Documentation](https://gradio.app/docs)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/gradio)

---

*If your issue isn't resolved, please open an issue on [GitHub](https://github.com/Nouran99/bubbly---KidSafe-Alphabet-Tutor/issues) with the diagnostic information.*