import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from config.config import set_env_variables

# Set environment variables (e.g. GOOGLE_API_KEY)
set_env_variables()

def load_llm():
    """Initialize the Gemini 2.5 Pro model"""
    try:
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it before running the application.")
        
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=api_key,
            temperature=0.3,
            convert_system_message_to_human=True
        )
    except Exception as e:
        print(f"Error initializing LLM: {str(e)}")
        print("\nTo fix this issue:")
        print("1. Get a Google API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as an environment variable:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("   Or on Windows: set GOOGLE_API_KEY=your-api-key-here")
        print("3. Or create a .env file in the project root with:")
        print("   GOOGLE_API_KEY=your-api-key-here")
        raise

def load_vectorstore():
    """Load FAISS vectorstore for RAG"""
    try:
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return FAISS.load_local("RAG/faiss_index", embedding_model, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error loading vectorstore: {str(e)}")
        print("Make sure the RAG/faiss_index directory exists and contains the index files.")
        raise

def retrieve_context(query: str, k: int = 3) -> str:
    """Perform semantic search over the vectorstore"""
    try:
        vectorstore = load_vectorstore()
        docs = vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return ""

# Initialize LLM only if API key is available
try:
    llm = load_llm()
except Exception:
    llm = None
