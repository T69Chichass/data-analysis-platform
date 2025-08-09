#!/usr/bin/env python3
"""
Simple Pinecone API Test
"""

import tempenv
import os
import requests

def test_pinecone_api():
    """Test Pinecone API directly."""
    print("🌲 Testing Pinecone API Directly")
    print("=" * 40)
    
    api_key = os.environ.get('PINECONE_API_KEY')
    print(f"API Key: {api_key[:10]}...")
    
    # Test with direct API call
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Test listing indexes
        print("\n📋 Testing API with direct call...")
        response = requests.get('https://controller.pinecone.io/databases', headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ API key is valid!")
            return True
        else:
            print(f"❌ API key is invalid. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_pinecone_api()
