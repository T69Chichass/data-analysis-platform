#!/usr/bin/env python3
"""
Comprehensive Pinecone Diagnostic Tool
This script will help identify why Pinecone is not working.
"""

import tempenv
import os
import requests
import json
import time

def check_api_key():
    """Check if the API key is valid."""
    print("🔑 Step 1: Checking API Key")
    print("=" * 40)
    
    api_key = os.environ.get('PINECONE_API_KEY')
    
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    if not api_key.startswith('pcsk_'):
        print("❌ API key format is incorrect (should start with 'pcsk_')")
        return False
    
    print(f"✅ API key format looks correct: {api_key[:10]}...")
    return True

def check_network_connectivity():
    """Check basic network connectivity."""
    print("\n🌐 Step 2: Checking Network Connectivity")
    print("=" * 40)
    
    try:
        # Test basic internet connectivity
        response = requests.get('https://www.google.com', timeout=5)
        print("✅ Basic internet connectivity: OK")
        
        # Test Pinecone controller access
        response = requests.get('https://controller.pinecone.io', timeout=10)
        print("✅ Pinecone controller access: OK")
        
        return True
    except Exception as e:
        print(f"❌ Network connectivity issue: {e}")
        return False

def list_all_indexes():
    """List all indexes to see what exists."""
    print("\n📋 Step 3: Listing All Indexes")
    print("=" * 40)
    
    api_key = os.environ.get('PINECONE_API_KEY')
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('https://controller.pinecone.io/databases', headers=headers, timeout=10)
        
        if response.status_code == 200:
            indexes = response.json()
            print(f"✅ Found {len(indexes)} index(es):")
            
            if len(indexes) == 0:
                print("⚠️ No indexes found - you need to create an index")
                return False
            
            for index in indexes:
                name = index.get('name', 'N/A')
                environment = index.get('environment', 'N/A')
                status = index.get('status', {}).get('ready', 'N/A')
                dimension = index.get('dimension', 'N/A')
                
                print(f"📊 Index: {name}")
                print(f"   Environment: {environment}")
                print(f"   Status: {status}")
                print(f"   Dimension: {dimension}")
                print("-" * 30)
            
            # Check if loopers1 exists
            loopers1_exists = any(index.get('name') == 'loopers1' for index in indexes)
            
            if loopers1_exists:
                print("✅ Index 'loopers1' found!")
                return True
            else:
                print("❌ Index 'loopers1' not found!")
                print("💡 You need to create an index named 'loopers1'")
                return False
                
        elif response.status_code == 401:
            print("❌ Invalid API key")
            return False
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error listing indexes: {e}")
        return False

def test_specific_index():
    """Test connection to the specific index."""
    print("\n🔗 Step 4: Testing Specific Index Connection")
    print("=" * 40)
    
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    print(f"Testing index: {index_name}")
    print(f"Environment: {environment}")
    
    headers = {
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Test different URL formats
    urls_to_test = [
        f"https://{index_name}-{environment}.svc.{environment}.pinecone.io/describe_index_stats",
        f"https://{index_name}-{environment}.svc.{environment}.pinecone.io/describe_index_stats",
        f"https://{index_name}.{environment}.svc.{environment}.pinecone.io/describe_index_stats"
    ]
    
    for i, url in enumerate(urls_to_test, 1):
        print(f"\n🔍 Testing URL format {i}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ SUCCESS! Index is accessible")
                print(f"   Total Vectors: {stats.get('total_vector_count', 0):,}")
                print(f"   Dimension: {stats.get('dimension', 0)}")
                return True
            elif response.status_code == 404:
                print(f"❌ Index not found (404)")
            elif response.status_code == 401:
                print(f"❌ Unauthorized (401) - check API key")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout error")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

def check_environment_compatibility():
    """Check if the environment configuration is correct."""
    print("\n🌍 Step 5: Checking Environment Configuration")
    print("=" * 40)
    
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    print(f"Current configuration:")
    print(f"   Index Name: {index_name}")
    print(f"   Environment: {environment}")
    
    # Common environment patterns
    valid_environments = [
        'gcp-starter',
        'us-east-1',
        'us-west1-gcp',
        'eastus-azure',
        'westus2-azure',
        'us-central1-gcp',
        'us-east1-gcp'
    ]
    
    if environment in valid_environments:
        print(f"✅ Environment '{environment}' is valid")
    else:
        print(f"⚠️ Environment '{environment}' is not in the common list")
        print(f"   Common environments: {', '.join(valid_environments)}")
    
    return True

def main():
    """Run comprehensive diagnostic."""
    print("🌲 Pinecone Diagnostic Tool")
    print("=" * 60)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all diagnostic steps
    steps = [
        ("API Key Check", check_api_key),
        ("Network Connectivity", check_network_connectivity),
        ("List All Indexes", list_all_indexes),
        ("Environment Check", check_environment_compatibility),
        ("Specific Index Test", test_specific_index)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            results.append((step_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    passed = 0
    for step_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{step_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Pinecone should be working.")
    else:
        print("\n💡 RECOMMENDATIONS:")
        if not results[0][1]:  # API key failed
            print("- Check your Pinecone API key")
        if not results[1][1]:  # Network failed
            print("- Check your internet connection")
        if not results[2][1]:  # No indexes
            print("- Create an index named 'loopers1' in Pinecone console")
        if not results[4][1]:  # Index test failed
            print("- Verify the index name and environment match your Pinecone console")

if __name__ == "__main__":
    main()
