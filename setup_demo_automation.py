#!/usr/bin/env python3
"""
Setup script for automated demo recording
Installs required dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_playwright():
    """Install Playwright and its dependencies"""
    try:
        print("📦 Installing Playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        
        print("🌐 Installing browser binaries...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        
        print("✅ Playwright installation completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Playwright: {e}")
        return False

def create_demo_directory():
    """Create directory for demo videos"""
    try:
        os.makedirs("demo_videos", exist_ok=True)
        print("📁 Created demo_videos directory")
        return True
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return False

def check_aida_running():
    """Check if AIDA is running"""
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ AIDA frontend is running on http://localhost:3000")
            return True
        else:
            print("⚠️  AIDA frontend not responding properly")
            return False
    except Exception:
        print("❌ AIDA frontend not running on http://localhost:3000")
        print("💡 Please start AIDA with: docker-compose up -d")
        return False

def main():
    """Main setup function"""
    print("🎬 AIDA Demo Automation Setup")
    print("=" * 40)
    
    # Install Playwright
    if not install_playwright():
        return False
    
    # Create demo directory
    if not create_demo_directory():
        return False
    
    # Check if AIDA is running
    aida_running = check_aida_running()
    
    print("\n🎯 Setup Summary:")
    print("✅ Playwright installed")
    print("✅ Demo directory created")
    print(f"{'✅' if aida_running else '❌'} AIDA application {'running' if aida_running else 'not running'}")
    
    if aida_running:
        print("\n🚀 Ready to record demo!")
        print("Run: python automated_demo.py")
    else:
        print("\n⚠️  Please start AIDA first:")
        print("1. docker-compose up -d")
        print("2. Wait 30 seconds")
        print("3. python automated_demo.py")
    
    return True

if __name__ == "__main__":
    main()