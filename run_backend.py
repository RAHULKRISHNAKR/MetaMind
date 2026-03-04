#!/usr/bin/env python3
"""
MetaMind Backend Startup Script

Run this from the MetaMind directory:
    python run_backend.py
"""

import sys
import os
from pathlib import Path

# Add the MetaMind directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Now import and run the FastAPI app
from backend.api.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting MetaMind Backend Server...")
    print("📍 API Documentation: http://localhost:8000/docs")
    print("📍 Health Check: http://localhost:8000/health")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

# Made with Bob
