#!/usr/bin/env python3
"""
Verify Pinecone API Key
"""

import tempenv
import os
import requests

def verify_api_key():
    """Verify the API key format and test it."""
    print("🔑 Verifying Pinecone API Key")
    print("=" * 40)
    
    api_key = os.environ.get('PINECONE_API_KEY')
    print(f"Current API Key: {api_key}")
    
    # Check format
    if not api_key.startswith('pcsk_'):
        print("❌ API key format is incorrect (should start with 'pcsk_')")
        return False
    
    if len(api_key) < 50:
        print("❌ API key seems too short")
        return False
    
    print(f"✅ API key format looks correct")
    print(f"   Length: {len(api_key)} characters")
    print(f"   Prefix: {api_key[:10]}...")
    
    # Test with direct API call
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        print("\n🌐 Testing API key with direct call...")
        response = requests.get('https://controller.pinecone.io/databases', headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API key is valid!")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid (401 Unauthorized)")
            print("💡 Please check your API key in the Pinecone console")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

if __name__ == "__main__":
    verify_api_key()
