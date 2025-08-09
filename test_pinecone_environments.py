#!/usr/bin/env python3
"""
Test different Pinecone environment configurations
"""

import tempenv
import os
import requests
import time

def test_environment(environment):
    """Test a specific Pinecone environment."""
    api_key = os.environ.get('PINECONE_API_KEY')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Test index stats
        index_url = f"https://{index_name}-{environment}.svc.{environment}.pinecone.io/describe_index_stats"
        response = requests.get(index_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ {environment}: SUCCESS")
            print(f"   Total Vectors: {stats.get('total_vector_count', 0):,}")
            print(f"   Dimension: {stats.get('dimension', 0)}")
            return True
        else:
            print(f"❌ {environment}: Failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ {environment}: Error - {str(e)[:50]}...")
        return False

def main():
    """Test multiple environment configurations."""
    print("🌲 Testing Pinecone Environment Configurations")
    print("=" * 60)
    
    # Common Pinecone environments to test
    environments = [
        'gcp-starter',
        'us-east-1',
        'us-west1-gcp',
        'eastus-azure',
        'westus2-azure',
        'us-central1-gcp',
        'us-east1-gcp'
    ]
    
    working_environments = []
    
    for env in environments:
        print(f"\n🔍 Testing environment: {env}")
        if test_environment(env):
            working_environments.append(env)
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 60)
    print("📋 RESULTS SUMMARY")
    print("=" * 60)
    
    if working_environments:
        print("✅ Working environments:")
        for env in working_environments:
            print(f"   - {env}")
        
        # Update tempenv.py with the first working environment
        best_env = working_environments[0]
        print(f"\n📝 Updating tempenv.py with environment: {best_env}")
        
        # Read and update tempenv.py
        with open('tempenv.py', 'r') as f:
            content = f.read()
        
        import re
        updated_content = re.sub(
            r"os\.environ\['PINECONE_ENVIRONMENT'\] = '[^']*'",
            f"os.environ['PINECONE_ENVIRONMENT'] = '{best_env}'",
            content
        )
        
        with open('tempenv.py', 'w') as f:
            f.write(updated_content)
        
        print("✅ Configuration updated successfully!")
        print(f"\n🎉 Your Pinecone is now configured with environment: {best_env}")
        
    else:
        print("❌ No working environments found")
        print("\nPossible issues:")
        print("1. Index 'loopers1' doesn't exist")
        print("2. API key is invalid")
        print("3. Network connectivity issues")
        print("4. Index is still initializing")
        
        print("\n💡 Next steps:")
        print("1. Check your Pinecone console at https://app.pinecone.io")
        print("2. Verify the index name and environment")
        print("3. Make sure the index is fully initialized")
        print("4. Check your API key")

if __name__ == "__main__":
    main()
