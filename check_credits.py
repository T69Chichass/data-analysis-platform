#!/usr/bin/env python3
"""
Credit and Account Status Checker
This script checks the credit status and account information for Gemini and Pinecone APIs.
"""

import tempenv
import os
import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional

def check_gemini_credits() -> Dict[str, Any]:
    """Check Gemini account status and credits."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return {"error": "Gemini API key not found or not configured"}
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Test Gemini API with a simple request
        data = {
            "contents": [{
                "parts": [{"text": "Hello"}]
            }]
        }
        
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return {
                "status": "active",
                "message": "API call successful"
            }
        elif response.status_code == 400:
            error_data = response.json()
            return {"error": f"API error: {error_data}"}
        elif response.status_code == 403:
            return {"error": "Invalid API key or quota exceeded"}
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def check_pinecone_status() -> Dict[str, Any]:
    """Check Pinecone account status and index information."""
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    if not all([api_key, environment, index_name]):
        return {"error": "Missing Pinecone configuration"}
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Check index status
        index_url = f"https://{index_name}-{environment}.svc.{environment}.pinecone.io/describe_index_stats"
        response = requests.get(index_url, headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            return {
                "status": "active",
                "index_name": index_name,
                "environment": environment,
                "index_stats": stats,
                "total_vector_count": stats.get('total_vector_count', 0),
                "dimension": stats.get('dimension', 0)
            }
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 404:
            return {"error": "Index not found"}
        else:
            return {"error": f"API error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}

def test_gemini_quota() -> Dict[str, Any]:
    """Test Gemini quota by making a simple API call."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return {"error": "Gemini API key not found"}
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [{
            "parts": [{"text": "Say hello"}]
        }],
        "generationConfig": {
            "maxOutputTokens": 10
        }
    }
    
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return {"status": "quota_available", "message": "API call successful"}
        elif response.status_code == 403:
            error_data = response.json()
            return {"status": "quota_exceeded", "error": error_data}
        elif response.status_code == 400:
            return {"status": "invalid_request", "error": response.json()}
        else:
            return {"status": "error", "error": f"API error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"status": "error", "error": f"Connection error: {str(e)}"}

def main():
    """Main function to run all credit checks."""
    print("🔍 Credit and Account Status Checker")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check Gemini
    print("🤖 Gemini Status Check")
    print("-" * 30)
    gemini_status = check_gemini_credits()
    if "error" in gemini_status:
        print(f"❌ Error: {gemini_status['error']}")
    else:
        print(f"✅ Status: {gemini_status['status']}")
        if 'message' in gemini_status:
            print(f"📋 Message: {gemini_status['message']}")
    
    print()
    
    # Test Gemini quota
    print("🧪 Gemini Quota Test")
    print("-" * 25)
    quota_test = test_gemini_quota()
    if quota_test['status'] == 'quota_available':
        print("✅ Quota available - API calls working")
    elif quota_test['status'] == 'quota_exceeded':
        print("❌ Quota exceeded - No credits remaining")
        if 'error' in quota_test:
            print(f"   Details: {quota_test['error']}")
    else:
        print(f"⚠️ Status: {quota_test['status']}")
        if 'error' in quota_test:
            print(f"   Error: {quota_test['error']}")
    
    print()
    
    # Check Pinecone
    print("🌲 Pinecone Status Check")
    print("-" * 30)
    pinecone_status = check_pinecone_status()
    if "error" in pinecone_status:
        print(f"❌ Error: {pinecone_status['error']}")
    else:
        print(f"✅ Status: {pinecone_status['status']}")
        print(f"📊 Index: {pinecone_status['index_name']}")
        print(f"🌍 Environment: {pinecone_status['environment']}")
        print(f"🔢 Total Vectors: {pinecone_status['total_vector_count']:,}")
        print(f"📏 Dimension: {pinecone_status['dimension']}")
    
    print()
    
    # Summary
    print("📋 Summary")
    print("-" * 15)
    
    gemini_working = "error" not in gemini_status and quota_test['status'] == 'quota_available'
    pinecone_working = "error" not in pinecone_status
    
    print(f"Gemini: {'✅ Working' if gemini_working else '❌ Issues'}")
    print(f"Pinecone: {'✅ Working' if pinecone_working else '❌ Issues'}")
    
    if gemini_working and pinecone_working:
        print("\n🎉 All services are configured and working!")
    else:
        print("\n⚠️ Some services have issues. Check the details above.")

if __name__ == "__main__":
    main()
