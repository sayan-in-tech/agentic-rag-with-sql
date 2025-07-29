#!/usr/bin/env python3
"""
Direct test of the chatbot module to verify fixes
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force reload the modules
if 'services.chat.chatbot' in sys.modules:
    del sys.modules['services.chat.chatbot']
if 'services.llm_connector.llm_connector' in sys.modules:
    del sys.modules['services.llm_connector.llm_connector']

from services.chat.chatbot import chatbot
from models.schema import State
from langchain_core.messages import HumanMessage

def test_chatbot_direct():
    """Test the chatbot function directly"""
    print("Testing chatbot function directly...")
    
    # Create a test state
    state = {
        "messages": [HumanMessage(content="Hello")],
        "memory": []
    }
    
    try:
        # Call the chatbot function
        result = chatbot(state)
        print("✅ Chatbot function executed successfully!")
        print(f"Response: {result['messages'][-1].content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Error in chatbot function: {str(e)}")
        return False

if __name__ == "__main__":
    test_chatbot_direct() 