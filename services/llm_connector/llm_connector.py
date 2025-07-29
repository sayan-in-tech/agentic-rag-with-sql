from langchain_openai import ChatOpenAI
from config.config import set_env_variables
import os

# Set environment variables from config
set_env_variables()

def load_llm():
    """Initialize the LLM with LM Studio configuration"""
    try:
        return ChatOpenAI(
            base_url=os.getenv("BASE_URL"),
            api_key=os.getenv("API_KEY"),
            model=os.getenv("MODEL"),
            streaming=True
        )
    except Exception as e:
        print(f"Error initializing LLM: {str(e)}")
        print("Please ensure LM Studio is running and the model is loaded")
        raise

# Create and export the llm instance
llm = load_llm()