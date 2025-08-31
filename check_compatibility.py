#!/usr/bin/env python3
"""
Compatibility checker for KidSafe Alphabet Tutor
Verifies all files and dependencies work together
"""

import sys
import os
import json
from pathlib import Path

def check_imports():
    """Check if all required imports work"""
    print("=" * 60)
    print("CHECKING IMPORTS")
    print("=" * 60)
    
    results = {"success": [], "failed": []}
    
    # Core imports required by simple_app.py
    core_imports = [
        ("gradio", "gradio"),
        ("app.state", "SessionMemory"),
        ("agents.crew_setup_simple", "AlphabetTutorAgents")
    ]
    
    # Add parent directory to path (as simple_app.py does)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    for module_path, item in core_imports:
        try:
            if "." in module_path:
                # Handle submodule imports
                parts = module_path.split(".")
                module = __import__(module_path, fromlist=[item])
                if hasattr(module, item):
                    results["success"].append(f"✓ {module_path}.{item}")
                else:
                    results["failed"].append(f"✗ {module_path}.{item} - attribute not found")
            else:
                # Handle direct module imports
                module = __import__(module_path)
                results["success"].append(f"✓ {module_path}")
        except ImportError as e:
            results["failed"].append(f"✗ {module_path} - {str(e)}")
        except Exception as e:
            results["failed"].append(f"✗ {module_path} - Unexpected error: {str(e)}")
    
    # Print results
    for success in results["success"]:
        print(success)
    for failure in results["failed"]:
        print(failure)
    
    return len(results["failed"]) == 0

def check_files():
    """Check if all required files exist"""
    print("\n" + "=" * 60)
    print("CHECKING FILES")
    print("=" * 60)
    
    required_files = [
        "app/__init__.py",
        "app/simple_app.py",
        "app/state.py",
        "app/curriculum.json",
        "agents/__init__.py",
        "agents/crew_setup_simple.py",
        "requirements.txt",
        "README.md",
        "setup.py"
    ]
    
    missing = []
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0

def check_curriculum():
    """Check if curriculum.json is valid"""
    print("\n" + "=" * 60)
    print("CHECKING CURRICULUM")
    print("=" * 60)
    
    try:
        with open("app/curriculum.json", 'r') as f:
            curriculum = json.load(f)
        
        # Check for required keys
        required_keys = ["letters", "activities"]
        for key in required_keys:
            if key in curriculum:
                print(f"✓ curriculum.json has '{key}' section")
            else:
                print(f"✗ curriculum.json missing '{key}' section")
                return False
        
        # Check if letters have required info
        if "letters" in curriculum:
            letter_count = len(curriculum["letters"])
            print(f"✓ Found {letter_count} letters in curriculum")
            
            # Check a sample letter
            if "A" in curriculum["letters"]:
                a_info = curriculum["letters"]["A"]
                if "sound_description" in a_info and "example_words" in a_info:
                    print(f"✓ Letter 'A' has required fields")
                else:
                    print(f"✗ Letter 'A' missing required fields")
        
        return True
    except json.JSONDecodeError as e:
        print(f"✗ curriculum.json is not valid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ curriculum.json not found")
        return False
    except Exception as e:
        print(f"✗ Error checking curriculum: {e}")
        return False

def check_version_consistency():
    """Check if versions are consistent across files"""
    print("\n" + "=" * 60)
    print("CHECKING VERSION CONSISTENCY")
    print("=" * 60)
    
    # Key packages that must have consistent versions
    key_packages = {
        "gradio": "4.19.2",
        "fastapi": "0.109.2",
        "pydantic": "2.5.3",
        "starlette": "0.36.3",
        "uvicorn": "0.27.1"
    }
    
    # Check requirements.txt
    try:
        with open("requirements.txt", 'r') as f:
            req_lines = f.readlines()
        
        req_versions = {}
        for line in req_lines:
            line = line.strip()
            if "==" in line and not line.startswith("#"):
                pkg, version = line.split("==")
                req_versions[pkg.strip()] = version.strip()
        
        # Compare versions
        all_match = True
        for pkg, expected_version in key_packages.items():
            if pkg in req_versions:
                actual_version = req_versions[pkg]
                if actual_version == expected_version:
                    print(f"✓ {pkg}: {actual_version} (correct)")
                else:
                    print(f"✗ {pkg}: {actual_version} (expected {expected_version})")
                    all_match = False
            else:
                print(f"⚠ {pkg}: not found in requirements.txt")
        
        return all_match
    except Exception as e:
        print(f"✗ Error checking versions: {e}")
        return False

def check_simple_app_compatibility():
    """Check if simple_app.py settings are compatible"""
    print("\n" + "=" * 60)
    print("CHECKING SIMPLE_APP.PY COMPATIBILITY")
    print("=" * 60)
    
    try:
        with open("app/simple_app.py", 'r') as f:
            content = f.read()
        
        # Check for critical settings
        checks = [
            ("show_api=False", "Gradio API disabled (prevents ASGI errors)"),
            ("debug=False", "Debug mode disabled (prevents verbose errors)"),
            ("server_port=7860", "Using standard port 7860"),
            ("gradio as gr", "Using gradio import"),
            ("SessionMemory", "Using SessionMemory class"),
            ("AlphabetTutorAgents", "Using AlphabetTutorAgents class")
        ]
        
        all_good = True
        for check_str, description in checks:
            if check_str in content:
                print(f"✓ {description}")
            else:
                print(f"✗ Missing: {description}")
                all_good = False
        
        return all_good
    except Exception as e:
        print(f"✗ Error checking simple_app.py: {e}")
        return False

def main():
    """Run all compatibility checks"""
    print("\n" + "=" * 60)
    print("KIDSAFE ALPHABET TUTOR - COMPATIBILITY CHECK")
    print("=" * 60)
    
    results = {
        "Files": check_files(),
        "Imports": check_imports(),
        "Curriculum": check_curriculum(),
        "Versions": check_version_consistency(),
        "App Config": check_simple_app_compatibility()
    }
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL COMPATIBILITY CHECKS PASSED")
        print("The project files are fully compatible!")
    else:
        print("⚠️  SOME COMPATIBILITY ISSUES FOUND")
        print("Please review the failed checks above.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())