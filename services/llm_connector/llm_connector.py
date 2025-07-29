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
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
            convert_system_message_to_human=True,
            streaming=True
        )
    except Exception as e:
        print(f"Error initializing LLM: {str(e)}")
        raise

def load_vectorstore():
    """Load FAISS vectorstore for RAG"""
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local("RAG/faiss_index", embedding_model, allow_dangerous_deserialization=True)

def retrieve_context(query: str, k: int = 3) -> str:
    """Perform semantic search over the vectorstore"""
    vectorstore = load_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])

# Exported objects
llm = load_llm()
