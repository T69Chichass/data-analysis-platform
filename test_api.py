#!/usr/bin/env python3
"""
Test script for the Insurance Policy Analyzer API
"""

import requests
import json

def test_api():
    """Test the API endpoints."""
    
    # API base URL (change this to your Render URL after deployment)
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Insurance Policy Analyzer API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Test endpoint
    print("\n3. Testing test endpoint...")
    try:
        response = requests.post(f"{base_url}/test")
        if response.status_code == 200:
            result = response.json()
            print("✅ Test endpoint passed")
            print(f"   Accuracy: {result.get('accuracy', 0):.1f}%")
            print(f"   Message: {result.get('message', '')}")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Test endpoint error: {e}")
    
    # Test 4: Analyze endpoint
    print("\n4. Testing analyze endpoint...")
    test_query = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?"
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/analyze",
            json=test_query,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analyze endpoint passed")
            print(f"   Accuracy: {result.get('accuracy', 0):.1f}%")
            print(f"   Found: {result.get('found_count', 0)}/{result.get('total_questions', 0)} questions")
            print(f"   Message: {result.get('message', '')}")
            
            # Show first result
            if result.get('results'):
                first_result = result['results'][0]
                print(f"   Sample Answer: {first_result.get('answer', '')[:100]}...")
        else:
            print(f"❌ Analyze endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Analyze endpoint error: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api()
