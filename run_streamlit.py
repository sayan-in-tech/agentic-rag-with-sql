#!/usr/bin/env python3
"""
Launcher script for the Streamlit-based Agentic RAG with SQL Chat interface.
This provides a ChatGPT-like web interface for the agentic RAG system.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    print("🚀 Starting Agentic RAG with SQL Chat Interface...")
    print("📱 Opening web browser...")
    print("🌐 The app will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down the chat interface...")
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        print("💡 Make sure you have installed the requirements:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 