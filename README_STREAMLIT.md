# Agentic RAG with SQL - Streamlit Chat Interface

A modern, ChatGPT-like web interface for the Agentic RAG with SQL system, built with Streamlit.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Make sure you have your Google API key configured in your environment or `.env` file:
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Launch the Chat Interface

**Option A: Using the launcher script**
```bash
python run_streamlit.py
```

**Option B: Direct Streamlit command**
```bash
streamlit run streamlit_app.py
```

### 4. Open Your Browser
The chat interface will automatically open at: http://localhost:8501

## 🎯 Features

### ChatGPT-like Interface
- **Modern UI**: Clean, responsive design similar to ChatGPT
- **Real-time Chat**: Instant message processing and responses
- **Message History**: Persistent conversation memory
- **SQL Results Display**: Special formatting for SQL query results
- **Processing Indicators**: Visual feedback during processing

### Agentic RAG Capabilities
- **Smart Classification**: Automatically determines if SQL queries are needed
- **SQL Generation**: Creates and executes SQL queries for database questions
- **RAG Integration**: Uses knowledge base for contextual answers
- **Memory Management**: Remembers conversation context

### Sidebar Features
- **System Status**: Shows LLM connection status
- **Mode Indicator**: Displays whether SQL or chat mode is active
- **Clear Chat**: One-click conversation reset
- **Feature Overview**: Information about system capabilities

## 💬 Usage Examples

### Database Queries
```
User: "Show me all customers from Germany"
Assistant: [Generates SQL query and displays results]

User: "What's the total revenue by country?"
Assistant: [Creates SQL aggregation and shows formatted results]
```

### General Questions
```
User: "What is the Chinook database?"
Assistant: [Uses RAG knowledge base to provide information]

User: "How does this system work?"
Assistant: [Explains the agentic RAG architecture]
```

## 🎨 Interface Features

### Message Styling
- **User Messages**: Right-aligned with green avatar
- **Assistant Messages**: Left-aligned with robot avatar
- **SQL Results**: Special code-block formatting with syntax highlighting
- **Processing Animation**: Pulsing indicator during processing

### Responsive Design
- **Mobile Friendly**: Works on tablets and phones
- **Wide Layout**: Optimized for desktop screens
- **Sidebar**: Collapsible information panel
- **Form Input**: Modern chat input with send button

## 🔧 Technical Details

### Architecture
- **Streamlit**: Web framework for the interface
- **LangGraph**: Backend workflow orchestration
- **LangChain**: LLM integration and RAG
- **SQLAlchemy**: Database operations
- **FAISS**: Vector similarity search

### State Management
- **Session State**: Persistent conversation memory
- **Message History**: Complete chat transcript
- **Processing States**: Real-time status updates
- **Error Handling**: Graceful error display

### Performance
- **Async Processing**: Non-blocking message handling
- **Memory Management**: Efficient state updates
- **Cache Cleaning**: Automatic cleanup of temporary files
- **Error Recovery**: Robust error handling and display

## 🛠️ Customization

### Styling
The interface uses custom CSS for ChatGPT-like styling. You can modify the styles in the `streamlit_app.py` file:

```python
# Custom CSS section
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

### Features
- **Avatar Icons**: Change emoji avatars in `display_message()`
- **Color Scheme**: Modify CSS variables for different themes
- **Layout**: Adjust sidebar content and main area layout
- **Animations**: Customize processing indicators and transitions

## 🚨 Troubleshooting

### Common Issues

**1. LLM Not Available**
- Check your Google API key configuration
- Verify internet connection
- Ensure API quota is not exceeded

**2. Import Errors**
- Install all requirements: `pip install -r requirements.txt`
- Check Python version compatibility
- Verify all dependencies are installed

**3. Database Connection Issues**
- Ensure Chinook database files are present
- Check file permissions
- Verify SQLite installation

**4. Streamlit Not Starting**
- Check if port 8501 is available
- Try different port: `streamlit run streamlit_app.py --server.port 8502`
- Verify Streamlit installation

### Debug Mode
For debugging, you can run with verbose output:
```bash
streamlit run streamlit_app.py --logger.level debug
```

## 📱 Mobile Support

The interface is fully responsive and works on:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly interface

## 🔒 Security Notes

- API keys are handled securely through environment variables
- No sensitive data is stored in the interface
- Database queries are sanitized and validated
- Error messages don't expose sensitive information

## 🎉 Enjoy Your Chat!

The Streamlit interface provides a modern, user-friendly way to interact with your Agentic RAG with SQL system. Ask questions, explore the database, and enjoy the intelligent responses! 