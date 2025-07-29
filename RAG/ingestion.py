from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_faiss_index():
    """Create FAISS index from knowledge base"""
    try:
        loader = TextLoader(r"RAG\chinook_knowledge_base.txt", encoding="utf-8")
        docs = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        vectorstore = FAISS.from_documents(chunks, embedding_model)
        vectorstore.save_local(r"RAG\faiss_index")
        
        print("✅ [RAG/ingestion.py:create_faiss_index] FAISS index created successfully")
        
    except Exception as e:
        print(f"❌ [RAG/ingestion.py:create_faiss_index] Error creating FAISS index: {str(e)}")
        raise

if __name__ == "__main__":
    create_faiss_index()