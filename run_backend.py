#!/usr/bin/env python3
"""
Quick backend runner for testing
"""
import subprocess
import sys
import os

def run_backend():
    """Run backend directly without Docker"""
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Install dependencies
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        # Run the backend
        print("🚀 Starting AIDA backend...")
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], check=True)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try running manually:")
        print("cd backend")
        print("pip install -r requirements.txt")
        print("python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    run_backend()