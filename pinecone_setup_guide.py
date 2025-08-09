#!/usr/bin/env python3
"""
Pinecone Setup Guide and Configuration Fixer
This script helps you set up Pinecone properly and fix configuration issues.
"""

import tempenv
import os
import requests
import json
from datetime import datetime

def check_pinecone_api_key():
    """Check if Pinecone API key is valid."""
    api_key = os.environ.get('PINECONE_API_KEY')
    
    print("🔑 Checking Pinecone API Key")
    print("=" * 40)
    
    if not api_key:
        print("❌ No Pinecone API key found")
        return False
    
    if api_key.startswith('pcsk_'):
        print("✅ API key format looks correct (starts with 'pcsk_')")
        return True
    else:
        print("❌ API key format looks incorrect (should start with 'pcsk_')")
        return False

def list_all_environments():
    """List all available Pinecone environments."""
    api_key = os.environ.get('PINECONE_API_KEY')
    
    print("\n🌍 Checking Available Environments")
    print("=" * 40)
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Get all environments
        response = requests.get('https://controller.pinecone.io/databases', headers=headers)
        
        if response.status_code == 200:
            indexes = response.json()
            environments = set()
            
            for index in indexes:
                env = index.get('environment', 'unknown')
                environments.add(env)
                print(f"📊 Found index '{index.get('name', 'N/A')}' in environment '{env}'")
            
            print(f"\n✅ Available environments: {', '.join(environments)}")
            return list(environments)
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return []

def create_pinecone_index():
    """Create a new Pinecone index."""
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    
    print(f"\n🏗️ Creating Pinecone Index")
    print("=" * 40)
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Index configuration
    index_config = {
        "name": "loopers1",
        "dimension": 384,  # For all-MiniLM-L6-v2 model
        "metric": "cosine",
        "spec": {
            "serverless": {
                "cloud": "aws",
                "region": "us-east-1"
            }
        }
    }
    
    try:
        print(f"Creating index 'loopers1' in environment '{environment}'...")
        response = requests.post('https://controller.pinecone.io/databases', 
                               headers=headers, json=index_config)
        
        if response.status_code == 201:
            print("✅ Index creation initiated successfully!")
            print("⏳ Index will be ready in a few minutes...")
            return True
        elif response.status_code == 409:
            print("ℹ️ Index 'loopers1' already exists")
            return True
        else:
            print(f"❌ Error creating index: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_index_connection():
    """Test connection to the Pinecone index."""
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    print(f"\n🔗 Testing Index Connection")
    print("=" * 40)
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Test index stats
        index_url = f"https://{index_name}-{environment}.svc.{environment}.pinecone.io/describe_index_stats"
        response = requests.get(index_url, headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Index connection successful!")
            print(f"📊 Index: {index_name}")
            print(f"🌍 Environment: {environment}")
            print(f"🔢 Total Vectors: {stats.get('total_vector_count', 0):,}")
            print(f"📏 Dimension: {stats.get('dimension', 0)}")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def update_environment_config():
    """Update environment configuration based on available environments."""
    print(f"\n⚙️ Updating Environment Configuration")
    print("=" * 40)
    
    environments = list_all_environments()
    
    if not environments:
        print("❌ No environments found. Please check your API key.")
        return False
    
    # Try to find the best environment
    preferred_envs = ['gcp-starter', 'us-east-1', 'us-west1-gcp']
    
    for env in preferred_envs:
        if env in environments:
            print(f"✅ Found preferred environment: {env}")
            
            # Update tempenv.py
            update_tempenv_environment(env)
            return True
    
    # If no preferred environment, use the first available
    if environments:
        env = environments[0]
        print(f"✅ Using available environment: {env}")
        update_tempenv_environment(env)
        return True
    
    return False

def update_tempenv_environment(environment):
    """Update the environment in tempenv.py."""
    print(f"📝 Updating tempenv.py with environment: {environment}")
    
    # Read current tempenv.py
    with open('tempenv.py', 'r') as f:
        content = f.read()
    
    # Update environment
    import re
    updated_content = re.sub(
        r"os\.environ\['PINECONE_ENVIRONMENT'\] = '[^']*'",
        f"os.environ['PINECONE_ENVIRONMENT'] = '{environment}'",
        content
    )
    
    # Write back
    with open('tempenv.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ tempenv.py updated successfully!")

def main():
    """Main setup function."""
    print("🌲 Pinecone Setup Guide")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Check API key
    if not check_pinecone_api_key():
        print("\n❌ Please get a valid Pinecone API key from https://app.pinecone.io")
        return
    
    # Step 2: List environments and update config
    if not update_environment_config():
        print("\n❌ Could not determine environment configuration")
        return
    
    # Step 3: Create index if needed
    if not create_pinecone_index():
        print("\n❌ Could not create index")
        return
    
    # Step 4: Test connection
    if test_index_connection():
        print("\n🎉 Pinecone setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Your index is ready for use")
        print("2. You can now upload documents and make queries")
        print("3. Run 'python main.py' to start your application")
    else:
        print("\n⚠️ Setup completed but connection test failed")
        print("The index might still be initializing. Try again in a few minutes.")

if __name__ == "__main__":
    main()
