#!/usr/bin/env python3
"""
MetaMind Frontend Startup Script

Run this from the MetaMind directory:
    python run_frontend.py
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the MetaMind directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

if __name__ == "__main__":
    print("🎨 Starting MetaMind Frontend...")
    print("📍 Frontend URL: http://localhost:8501")
    print("📍 Make sure the backend is running at http://localhost:8000")
    print("\nPress CTRL+C to stop the frontend\n")
    
    # Run Streamlit
    subprocess.run([
        "streamlit", "run",
        "frontend/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--browser.gatherUsageStats=false"
    ])

# Made with Bob
