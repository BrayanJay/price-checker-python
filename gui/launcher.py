#!/usr/bin/env python3
"""
Launcher script for the Pricing Engine GUI
This script starts both the FastAPI server and GUI application
"""

import subprocess
import time
import threading
import sys
import os
from pathlib import Path

def start_api_server():
    """Start the FastAPI server in the background"""
    api_dir = Path(__file__).parent.parent / "api"
    os.chdir(api_dir)
    
    try:
        # Start FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", "--reload", "--host", "localhost", "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("API server stopped")

def start_gui():
    """Start the GUI application"""
    gui_dir = Path(__file__).parent
    os.chdir(gui_dir)
    
    # Wait a moment for API server to start
    time.sleep(3)
    
    try:
        # Start GUI
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("GUI application stopped")

def main():
    print("🚀 Starting Pricing Engine - FastAPI Integration")
    print("=" * 50)
    print("Starting API server...")
    
    # Start API server in background thread
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    print("Starting GUI application...")
    
    # Start GUI in main thread
    start_gui()

if __name__ == "__main__":
    main()