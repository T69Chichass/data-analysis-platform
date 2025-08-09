#!/usr/bin/env python3
"""
Check Pinecone index status and environment
"""

import tempenv
import os
import requests
import json

def check_pinecone_index():
    """Check if the Pinecone index exists and get its details."""
    api_key = os.environ.get('PINECONE_API_KEY')
    
    print("🔍 Checking Pinecone Index Status")
    print("=" * 50)
    
    if not api_key:
        print("❌ No Pinecone API key found")
        return
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Get all indexes
        print("📋 Fetching all your indexes...")
        response = requests.get('https://controller.pinecone.io/databases', headers=headers)
        
        if response.status_code == 200:
            indexes = response.json()
            print(f"✅ Found {len(indexes)} index(es):")
            print()
            
            for index in indexes:
                name = index.get('name', 'N/A')
                environment = index.get('environment', 'N/A')
                status = index.get('status', {}).get('ready', 'N/A')
                dimension = index.get('dimension', 'N/A')
                
                print(f"📊 Index: {name}")
                print(f"   Environment: {environment}")
                print(f"   Status: {status}")
                print(f"   Dimension: {dimension}")
                print("-" * 40)
            
            # Check if loopers1 exists
            loopers1_exists = any(index.get('name') == 'loopers1' for index in indexes)
            
            if loopers1_exists:
                print("✅ Index 'loopers1' found!")
                # Get the actual environment for loopers1
                for index in indexes:
                    if index.get('name') == 'loopers1':
                        actual_env = index.get('environment')
                        print(f"📝 Actual environment for 'loopers1': {actual_env}")
                        
                        # Update tempenv.py if needed
                        current_env = os.environ.get('PINECONE_ENVIRONMENT')
                        if actual_env != current_env:
                            print(f"⚠️ Environment mismatch! Current: {current_env}, Actual: {actual_env}")
                            print("💡 You should update your tempenv.py with the correct environment")
                        else:
                            print("✅ Environment configuration is correct!")
                        break
            else:
                print("❌ Index 'loopers1' not found!")
                print("💡 You need to create an index named 'loopers1'")
                
        else:
            print(f"❌ Error fetching indexes: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    check_pinecone_index()
