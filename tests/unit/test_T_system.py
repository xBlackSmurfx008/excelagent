#!/usr/bin/env python3
"""
Test script to verify the unified dashboard system
"""

import os
import sys
from pathlib import Path

def test_system():
    """Test the unified dashboard system"""
    print("🧪 Testing Excel Agent Unified Dashboard System")
    print("=" * 50)
    
    # Test 1: Check if all required files exist
    print("📁 Checking required files...")
    required_files = [
        "unified_dashboard.py",
        "Launch_Unified_Dashboard.command"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING!")
            return False
    
    # Test 2: Check if directories exist
    print("\n📂 Checking required directories...")
    required_dirs = ["templates", "uploads", "venv"]
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ - MISSING!")
            return False
    
    # Test 3: Check if at least one data folder exists (data or Data)
    print("\n📂 Checking data folders (data/ or Data/)...")
    data_exists = Path("data").exists() or Path("Data").exists()
    if data_exists:
        print("   ✅ Data folder present")
    else:
        print("   ❌ No data folder found (will be created on launch)")

    # Test 4: Check if virtual environment has required packages
    print("\n📦 Checking Python dependencies...")
    try:
        import flask
        import flask_socketio
        import pandas
        import openpyxl
        print("   ✅ All dependencies available")
    except ImportError as e:
        print(f"   ❌ Missing dependency: {e}")
        return False
    
    # Test 5: Check if template file exists
    print("\n🎨 Checking template file...")
    template_file = Path("templates/unified_dashboard.html")
    if template_file.exists():
        print("   ✅ Template file exists")
    else:
        print("   ❌ Template file missing!")
        return False
    
    # Test 6: Check file permissions
    print("\n🔐 Checking file permissions...")
    launcher = Path("Launch_Unified_Dashboard.command")
    if launcher.exists() and os.access(launcher, os.X_OK):
        print("   ✅ Launcher script is executable")
    else:
        print("   ❌ Launcher script not executable!")
        return False
    
    print("\n🎉 All tests passed! System is ready to use.")
    print("\n🚀 To launch the system:")
    print("   1. Double-click: Launch_Unified_Dashboard.command")
    print("   2. The launcher opens your browser automatically (port starts at 5001)")
    print("   3. Start using your Excel Agent!")
    
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
