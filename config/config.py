import os
from pathlib import Path

def set_env_variables():
    """Set up environment variables, including loading from .env file if it exists"""
    
    # Try to load from .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip()
    
    # Set default values if not already set
    if "MODEL" not in os.environ:
        os.environ["MODEL"] = "gemini-1.5-pro"
    
    # Check if GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ [config/config.py:set_env_variables] GOOGLE_API_KEY not found in environment variables.")
        print("To fix this:")
        print("1. Get a Google API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as an environment variable:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("   Or on Windows: set GOOGLE_API_KEY=your-api-key-here")
        print("3. Or create a .env file in the project root with:")
        print("   GOOGLE_API_KEY=your-api-key-here")

    # Set the prompts for different roles
    os.environ["PROMPT"] = """
        You are a helpful assistant. Your task is to assist the user with their queries.
        You will receive a message from the user, and you should respond with a helpful answer.
        """