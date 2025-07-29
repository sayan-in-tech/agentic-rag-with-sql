import os

# Define the environment variables

def set_env_variables():
    # os.environ["BASE_URL"] = "http://127.0.0.1:1234/v1"
    # os.environ["API_KEY"] = "lm-studio"
    os.environ["MODEL"] = "gemini-2.5-flash"

    # Set the prompts for different roles
    os.environ["PROMPT"] = """
        You are a helpful assistant. Your task is to assist the user with their queries.
        You will receive a message from the user, and you should respond with a helpful answer.
        """