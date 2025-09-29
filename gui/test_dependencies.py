#!/usr/bin/env python3
"""
Simple test to verify GUI dependencies and basic functionality
"""

import sys
import os

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🧪 Testing GUI Dependencies")
    print("=" * 40)
    
    # Test tkinter
    try:
        import tkinter as tk
        print("✅ tkinter: Available")
    except ImportError:
        print("❌ tkinter: Not available")
        return False
    
    # Test requests
    try:
        import requests
        print("✅ requests: Available")
    except ImportError:
        print("❌ requests: Not available")
        return False
    
    # Test threading
    try:
        import threading
        print("✅ threading: Available")
    except ImportError:
        print("❌ threading: Not available")
        return False
    
    # Test json
    try:
        import json
        print("✅ json: Available")
    except ImportError:
        print("❌ json: Not available")
        return False
    
    print("\n🎉 All dependencies are available!")
    return True

def test_gui_creation():
    """Test basic GUI window creation"""
    print("\n🖥️ Testing GUI Window Creation")
    print("=" * 40)
    
    try:
        import tkinter as tk
        
        # Create a simple test window
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")
        
        label = tk.Label(root, text="GUI Test Successful!", font=("Arial", 14))
        label.pack(expand=True)
        
        # Destroy after 2 seconds
        root.after(2000, root.destroy)
        
        print("✅ GUI window creation: Successful")
        print("💡 Window will appear for 2 seconds...")
        
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ GUI window creation failed: {e}")
        return False

def main():
    print("🚀 Pricing Engine GUI - Dependency Test")
    print("=" * 50)
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ Dependency test failed!")
        sys.exit(1)
    
    # Test GUI creation
    if not test_gui_creation():
        print("\n❌ GUI test failed!")
        sys.exit(1)
    
    print("\n🎯 All tests passed! The GUI is ready to run.")
    print("\nTo start the full application:")
    print("1. Start API server: cd ../api && python main.py")
    print("2. Start GUI: python main.py")
    print("3. Or use launcher: python launcher.py")

if __name__ == "__main__":
    main()