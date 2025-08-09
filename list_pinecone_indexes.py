#!/usr/bin/env python3
"""
Script to list all available Pinecone indexes
"""

import tempenv
import os
import requests
import json

def list_pinecone_indexes():
    """List all available Pinecone indexes."""
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    
    if not api_key:
        print("❌ Pinecone API key not found")
        return
    
    print(f"🔍 Listing Pinecone indexes for environment: {environment}")
    print("=" * 60)
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # List all indexes
        response = requests.get('https://controller.pinecone.io/databases', headers=headers)
        
        if response.status_code == 200:
            indexes = response.json()
            print(f"✅ Found {len(indexes)} indexes:")
            print()
            
            for index in indexes:
                print(f"📊 Index Name: {index.get('name', 'N/A')}")
                print(f"   Environment: {index.get('environment', 'N/A')}")
                print(f"   Status: {index.get('status', {}).get('ready', 'N/A')}")
                print(f"   Dimension: {index.get('dimension', 'N/A')}")
                print(f"   Metric: {index.get('metric', 'N/A')}")
                print(f"   Host: {index.get('host', 'N/A')}")
                print("-" * 40)
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    list_pinecone_indexes()
