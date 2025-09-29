#!/usr/bin/env python3
"""
Complete Integration Example - Pricing Engine GUI with FastAPI
This script demonstrates the full integration between GUI and API
"""

import subprocess
import time
import threading
import sys
import os
import requests
from pathlib import Path

class IntegrationManager:
    def __init__(self):
        self.api_process = None
        self.gui_process = None
        self.api_running = False
        
    def check_api_health(self, retries=10, delay=1):
        """Check if API server is healthy"""
        for i in range(retries):
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    return True
            except:
                pass
            time.sleep(delay)
        return False
    
    def start_api_server(self):
        """Start the FastAPI server"""
        print("🚀 Starting FastAPI server...")
        api_dir = Path(__file__).parent.parent / "api"
        
        try:
            # Start the API server
            self.api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "main:app", "--reload", "--host", "localhost", "--port", "8000"
            ], cwd=api_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to be ready
            if self.check_api_health():
                self.api_running = True
                print("✅ FastAPI server is running on http://localhost:8000")
                return True
            else:
                print("❌ Failed to start FastAPI server")
                return False
                
        except Exception as e:
            print(f"❌ Error starting API server: {e}")
            return False
    
    def start_gui(self, demo_mode=False):
        """Start the GUI application"""
        if demo_mode:
            print("🖥️ Starting GUI in demo mode...")
            gui_script = "demo.py"
        else:
            print("🖥️ Starting GUI with API integration...")
            gui_script = "main.py"
        
        gui_dir = Path(__file__).parent
        
        try:
            self.gui_process = subprocess.Popen([
                sys.executable, gui_script
            ], cwd=gui_dir)
            
            print(f"✅ GUI started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error starting GUI: {e}")
            return False
    
    def stop_servers(self):
        """Stop both API and GUI"""
        print("\n🛑 Stopping servers...")
        
        if self.api_process:
            self.api_process.terminate()
            print("✅ API server stopped")
            
        if self.gui_process:
            self.gui_process.terminate()
            print("✅ GUI application stopped")
    
    def run_full_integration(self):
        """Run complete integration - API + GUI"""
        print("🎯 Pricing Engine - Complete Integration")
        print("="*50)
        
        # Start API server
        if not self.start_api_server():
            print("❌ Failed to start API server. Exiting...")
            return False
        
        # Load sample data
        print("📊 Loading sample data...")
        try:
            response = requests.post("http://localhost:8000/load-sample-data")
            if response.status_code == 200:
                print("✅ Sample data loaded successfully")
            else:
                print("⚠️ Warning: Could not load sample data")
        except:
            print("⚠️ Warning: Could not load sample data")
        
        # Start GUI
        if not self.start_gui(demo_mode=False):
            print("❌ Failed to start GUI. Stopping API...")
            self.stop_servers()
            return False
        
        print("\n🎉 Integration complete!")
        print("="*50)
        print("📡 API Server: http://localhost:8000")
        print("🖥️ GUI Application: Running")
        print("📖 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop all services")
        
        try:
            # Wait for GUI to close
            self.gui_process.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_servers()
        
        return True
    
    def run_demo_mode(self):
        """Run GUI in demo mode only"""
        print("🎯 Pricing Engine - Demo Mode")
        print("="*50)
        print("📝 Running GUI with mock data (no API required)")
        
        if self.start_gui(demo_mode=True):
            print("✅ Demo GUI started successfully")
            try:
                self.gui_process.wait()
            except KeyboardInterrupt:
                pass
            finally:
                if self.gui_process:
                    self.gui_process.terminate()
        
        return True

def show_menu():
    """Show integration options menu"""
    print("\n🚀 Pricing Engine - FastAPI Integration")
    print("="*50)
    print("Choose an integration mode:")
    print("1. 🎯 Full Integration (API + GUI)")
    print("2. 📝 Demo Mode (GUI only with mock data)")
    print("3. 🚀 API Server Only")
    print("4. 🖥️ GUI Only (requires API running)")
    print("5. 🧪 Test Dependencies")
    print("6. ❌ Exit")
    print("="*50)

def main():
    manager = IntegrationManager()
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🎯 Starting Full Integration...")
            manager.run_full_integration()
            
        elif choice == "2":
            print("\n📝 Starting Demo Mode...")
            manager.run_demo_mode()
            
        elif choice == "3":
            print("\n🚀 Starting API Server Only...")
            if manager.start_api_server():
                print("✅ API server running. Press Ctrl+C to stop...")
                try:
                    manager.api_process.wait()
                except KeyboardInterrupt:
                    manager.stop_servers()
            
        elif choice == "4":
            print("\n🖥️ Starting GUI Only...")
            if manager.check_api_health(retries=1):
                manager.start_gui(demo_mode=False)
                try:
                    manager.gui_process.wait()
                except KeyboardInterrupt:
                    if manager.gui_process:
                        manager.gui_process.terminate()
            else:
                print("❌ API server not running. Start it first or use Demo Mode.")
            
        elif choice == "5":
            print("\n🧪 Testing Dependencies...")
            test_cmd = [sys.executable, "test_dependencies.py"]
            subprocess.run(test_cmd, cwd=Path(__file__).parent)
            
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Integration manager stopped.")
    except Exception as e:
        print(f"\n❌ Error: {e}")