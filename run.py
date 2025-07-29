from services.chat.chat import run_chatbot
from utils.cache_cleaner import clean_pycache

# Load environment variables
from config.config import set_env_variables
set_env_variables()

# Load the LLM
from services.llm_connector.llm_connector import load_llm
llm = load_llm()


if __name__ == "__main__":
    clean_pycache()

    run_chatbot()    

    clean_pycache()