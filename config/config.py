import os

# Define the environment variables

def set_env_variables():
    # Set the model name consistently
    os.environ["MODEL"] = "gemini-1.5-pro"
    
    # Check if GOOGLE_API_KEY is set in environment
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables.")
        print("Please set your Google API key as an environment variable:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        print("Or create a .env file with: GOOGLE_API_KEY=your-api-key-here")

    # Set the prompts for different roles
    os.environ["PROMPT"] = """
        You are a helpful assistant. Your task is to assist the user with their queries.
        You will receive a message from the user, and you should respond with a helpful answer.
        """