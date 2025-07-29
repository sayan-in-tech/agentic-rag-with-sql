#!/usr/bin/env python3
"""
Test script to verify Gemini API integration fixes
"""

import os
from services.llm_connector.llm_connector import load_llm
from langchain_core.messages import HumanMessage, SystemMessage

def test_gemini_connection():
    """Test basic Gemini API connection"""
    try:
        # Check if API key is set
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables.")
            print("Please set your Google API key:")
            print("1. Get a key from: https://makersuite.google.com/app/apikey")
            print("2. Set it as: export GOOGLE_API_KEY='your-key-here'")
            return False
        
        print("✅ GOOGLE_API_KEY found")
        
        # Test LLM initialization
        llm = load_llm()
        print("✅ LLM initialized successfully")
        
        # Test simple message
        messages = [
            HumanMessage(content="Hello, how are you?")
        ]
        
        response = llm.invoke(messages)
        print(f"✅ Basic message test passed: {response.content[:100]}...")
        
        # Test with system message
        messages_with_system = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="What is 2+2?")
        ]
        
        response2 = llm.invoke(messages_with_system)
        print(f"✅ System message test passed: {response2.content[:100]}...")
        
        print("\n🎉 All tests passed! The Gemini API integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Gemini API integration...")
    test_gemini_connection() 