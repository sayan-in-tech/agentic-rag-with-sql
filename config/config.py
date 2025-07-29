import os

# Define the environment variables

def set_env_variables():
    os.environ["API_KEY"] = "AIzaSyBdZ_-VRXW50IUvIlunHzek0na1e-3nFk4"

    # Set the prompts for different roles
    os.environ["PROMPT"] = """
        You are a helpful assistant. Your task is to provide accurate and concise information based on the user's queries.
        """