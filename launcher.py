#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WSP2AGENT Launcher - One-Click Startup with Auto-Repair
Checks dependencies, repairs environment, and launches the Streamlit app.
"""

import os
import subprocess
import sys
from pathlib import Path


def print_banner():
    """Display welcome banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║               WSP2AGENT LAUNCHER V3                      ║
    ║      World Seafood Producers - Outreach Automation      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_python_version():
    """Ensure Python 3.8+ is installed."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")


def check_virtualenv():
    """Check if virtual environment exists, create if missing."""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("⚠️  Virtual environment not found")
        print("🔧 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            sys.exit(1)
    else:
        print("✅ Virtual environment found")
    
    return venv_path


def get_pip_executable(venv_path):
    """Get the pip executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "pip.exe"
    else:  # Unix/Mac
        return venv_path / "bin" / "pip"


def get_python_executable(venv_path):
    """Get the python executable path for the virtual environment."""
    if os.name == 'nt':  # Windows
        return venv_path / "Scripts" / "python.exe"
    else:  # Unix/Mac
        return venv_path / "bin" / "python"


def install_dependencies(venv_path):
    """Install required packages from requirements.txt."""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("⚠️  requirements.txt not found - skipping dependency install")
        return
    
    print("📦 Checking dependencies...")
    pip_exe = get_pip_executable(venv_path)
    
    try:
        # Upgrade pip first
        print("   Upgrading pip...")
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        print("   Installing packages from requirements.txt...")
        result = subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"],
                              check=True, capture_output=True, text=True)
        
        print("✅ Dependencies installed")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Some packages may have failed to install")
        print(f"   Error: {e.stderr if hasattr(e, 'stderr') else str(e)}")


def check_environment():
    """Check critical files and environment variables."""
    issues = []
    
    # Check for critical directories
    directories = ["data", "data/sandbox", "modules", "streamlit_app"]
    for directory in directories:
        if not Path(directory).exists():
            issues.append(f"Missing directory: {directory}")
    
    # Check for SERPAPI_KEY
    if not os.getenv("SERPAPI_KEY"):
        issues.append("SERPAPI_KEY environment variable not set")
    
    # Check for credentials.json (optional)
    if not Path("credentials.json").exists():
        issues.append("credentials.json not found (Gmail features disabled)")
    
    if issues:
        print("\n⚠️  Environment Issues Detected:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 These can be fixed in the app Settings tab or will be auto-repaired on launch.")
    else:
        print("✅ Environment check passed")


def launch_streamlit(venv_path):
    """Launch the Streamlit application."""
    python_exe = get_python_executable(venv_path)
    
    # Check which app version to launch
    app_v3 = Path("streamlit_app/app_v3.py")
    app_default = Path("streamlit_app/app.py")
    
    if app_v3.exists():
        app_file = app_v3
        print("\n🚀 Launching WSP2AGENT V3...")
    elif app_default.exists():
        app_file = app_default
        print("\n🚀 Launching WSP2AGENT...")
    else:
        print("❌ ERROR: Streamlit app file not found")
        print("   Expected: streamlit_app/app.py or streamlit_app/app_v3.py")
        sys.exit(1)
    
    print(f"   App: {app_file}")
    print("   Server will open in your browser...")
    print("\n" + "="*60)
    print("  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        subprocess.run([
            str(python_exe), "-m", "streamlit", "run",
            str(app_file),
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down WSP2AGENT...")
        print("   Thanks for using the tool!")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        sys.exit(1)


def main():
    """Main launcher routine."""
    print_banner()
    
    # Step 1: Check Python version
    print("\n[1/5] Checking Python version...")
    check_python_version()
    
    # Step 2: Check/create virtual environment
    print("\n[2/5] Checking virtual environment...")
    venv_path = check_virtualenv()
    
    # Step 3: Install dependencies
    print("\n[3/5] Installing dependencies...")
    install_dependencies(venv_path)
    
    # Step 4: Check environment
    print("\n[4/5] Checking environment...")
    check_environment()
    
    # Step 5: Launch app
    print("\n[5/5] Starting application...")
    launch_streamlit(venv_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted - exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
