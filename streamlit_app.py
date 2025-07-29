import streamlit as st
import time
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.schema import State
from graph.graph import graph
from config.config import set_env_variables
from services.llm_connector.llm_connector import load_llm
from utils.cache_cleaner import clean_pycache

# Initialize environment and LLM
set_env_variables()
llm = load_llm()

# Page configuration
st.set_page_config(
    page_title="Agentic RAG with SQL Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for consistent dark theme styling
st.markdown("""
<style>
    /* Dark theme overrides */
    .main {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
    
    .stApp {
        background-color: #1e1e1e !important;
    }
    
    .stSidebar {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #3d3d3d !important;
        border: 1px solid #555555 !important;
        color: #ffffff !important;
        border-radius: 20px;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #aaaaaa !important;
    }
    
    .stButton > button {
        background-color: #10a37f !important;
        color: white !important;
        border: none !important;
        border-radius: 20px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #0d8a6f !important;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        display: flex;
        align-items: flex-start;
        background-color: #2d2d2d !important;
        border: 1px solid #444444 !important;
    }
    
    .user-message {
        background-color: #3d3d3d !important;
        margin-left: 2rem;
        border-left: 4px solid #10a37f !important;
    }
    
    .assistant-message {
        background-color: #2d2d2d !important;
        margin-right: 2rem;
        border-left: 4px solid #6c757d !important;
    }
    
    .message-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        flex-shrink: 0;
    }
    
    .user-avatar {
        background-color: #10a37f;
        color: white;
    }
    
    .assistant-avatar {
        background-color: #6c757d;
        color: white;
    }
    
    .message-content {
        flex: 1;
        word-wrap: break-word;
        color: #ffffff !important;
        line-height: 1.5;
    }
    
    /* Status indicator */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-processing {
        background-color: #ffc107;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Clear chat button */
    .clear-chat-btn {
        background-color: #dc3545 !important;
        color: white !important;
    }
    
    .clear-chat-btn:hover {
        background-color: #c82333 !important;
    }
    
    /* Text elements */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, div, span {
        color: #ffffff !important;
    }
    
    /* Streamlit specific overrides */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    .stAlert {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    /* Hide SQL output section */
    .sql-output {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "state" not in st.session_state:
        st.session_state.state = {
            "messages": [],
            "memory": []
        }
    if "processing" not in st.session_state:
        st.session_state.processing = False

def clear_chat():
    """Clear the chat history"""
    st.session_state.messages = []
    st.session_state.state = {
        "messages": [],
        "memory": []
    }

def process_message(user_input: str) -> str:
    """Process user message through the agentic RAG system"""
    try:
        # Initialize the graph
        app = graph()
        
        # Add user message to state
        st.session_state.state["messages"].append(HumanMessage(content=user_input))
        
        # Execute graph
        output = app.invoke(st.session_state.state)
        st.session_state.state.update(output)
        
        # Get the last AI message
        if st.session_state.state["messages"]:
            last_message = st.session_state.state["messages"][-1]
            if isinstance(last_message, AIMessage):
                return last_message.content
            else:
                return "I'm sorry, I couldn't generate a response. Please try again."
        else:
            return "I'm sorry, I couldn't generate a response. Please try again."
            
    except Exception as e:
        return f"I'm sorry, I encountered an error: {str(e)}"

def display_message(role: str, content: str):
    """Display a chat message with proper styling"""
    if role == "user":
        avatar = "👤"
        avatar_class = "user-avatar"
        message_class = "user-message"
    else:
        avatar = "🤖"
        avatar_class = "assistant-avatar"
        message_class = "assistant-message"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="message-avatar {avatar_class}">{avatar}</div>
        <div class="message-content">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 Agentic RAG with SQL")
        st.markdown("---")
        
        st.markdown("### About")
        st.markdown("""
        This is an intelligent chatbot that can:
        - Answer questions using RAG (Retrieval-Augmented Generation)
        - Generate and execute SQL queries
        - Provide insights from the Chinook database
        """)
        
        st.markdown("### Features")
        st.markdown("""
        - **Smart Classification**: Automatically determines if SQL is needed
        - **SQL Generation**: Creates SQL queries for database questions
        - **RAG Integration**: Uses knowledge base for contextual answers
        - **Memory**: Remembers conversation context
        """)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat", key="clear_chat", use_container_width=True):
            clear_chat()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### System Status")
        if llm:
            st.success("✅ LLM Connected")
        else:
            st.error("❌ LLM Not Available")
        
        # Display SQL status if available
        if hasattr(st.session_state.state, 'sql_needed_or_not'):
            if st.session_state.state.get('sql_needed_or_not'):
                st.info("🔍 SQL Query Mode")
            else:
                st.info("💬 Chat Mode")
    
    # Main chat area
    st.title("💬 Agentic RAG with SQL Chat")
    st.markdown("Ask me anything about the Chinook database or general questions!")
    
    # Display chat messages
    for message in st.session_state.messages:
        display_message(
            message["role"], 
            message["content"]
        )
    
    # Processing indicator
    if st.session_state.processing:
        with st.container():
            st.markdown("""
            <div style="display: flex; align-items: center; padding: 1rem;">
                <div class="status-indicator status-processing"></div>
                <span>Processing your request...</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Create a form for the chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message here...",
                key="user_input",
                placeholder="Ask me about the Chinook database or anything else!",
                label_visibility="collapsed"
            )
        
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)
    
    # Handle form submission
    if submit_button and user_input.strip():
        # Add user message to display
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Set processing state
        st.session_state.processing = True
        
        # Rerun to show user message
        st.rerun()
    
    # Process the message if we have one and we're not already processing
    if (st.session_state.processing and 
        st.session_state.messages and 
        st.session_state.messages[-1]["role"] == "user"):
        
        # Get the user's message
        user_message = st.session_state.messages[-1]["content"]
        
        # Process the message
        with st.spinner("Thinking..."):
            response = process_message(user_message)
        
        # Add assistant response to display
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Clear processing state
        st.session_state.processing = False
        
        # Rerun to show the response
        st.rerun()

if __name__ == "__main__":
    # Clean cache on startup
    clean_pycache()
    main() 