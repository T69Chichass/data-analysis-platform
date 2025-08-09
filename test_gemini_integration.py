#!/usr/bin/env python3
"""
Simple test script to verify Gemini integration
"""

import tempenv
from dependencies import get_gemini_manager

def test_gemini_basic():
    """Test basic Gemini functionality."""
    print("🧪 Testing Gemini Integration")
    print("=" * 40)
    
    try:
        # Get Gemini manager
        manager = get_gemini_manager()
        print(f"✅ Gemini Manager initialized: {type(manager)}")
        print(f"   Mock Mode: {manager.mock_mode}")
        
        if not manager.mock_mode:
            print(f"   API Key: {manager.api_key[:10]}...")
            print(f"   Model: {manager.model}")
            print(f"   Max Tokens: {manager.max_tokens}")
            print(f"   Temperature: {manager.temperature}")
            
            # Test a simple response
            print("\n🔍 Testing response generation...")
            test_prompt = "Say hello in a friendly way"
            response = manager.model.generate_content(test_prompt)
            print(f"✅ Response: {response.text.strip()}")
            
        else:
            print("   ⚠️ Running in mock mode")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_basic()
