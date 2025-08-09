#!/usr/bin/env python3
"""
Test Pinecone Connection with New API Key
"""

import tempenv
import os
from pinecone import Pinecone

def test_pinecone():
    """Test Pinecone connection."""
    print("🌲 Testing Pinecone Connection")
    print("=" * 40)
    
    # Get configuration
    api_key = os.environ.get('PINECONE_API_KEY')
    environment = os.environ.get('PINECONE_ENVIRONMENT')
    index_name = os.environ.get('PINECONE_INDEX_NAME')
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Environment: {environment}")
    print(f"Index Name: {index_name}")
    
    try:
        # Initialize Pinecone with new API
        print("\n🔗 Initializing Pinecone...")
        pc = Pinecone(api_key=api_key)
        print("✅ Pinecone initialized successfully")
        
        # List indexes
        print("\n📋 Listing available indexes...")
        indexes = pc.list_indexes()
        print(f"✅ Found {len(indexes)} indexes")
        
        # Connect to index
        print(f"\n📊 Connecting to index: {index_name}")
        index = pc.Index(index_name)
        print("✅ Connected to index successfully")
        
        # Get index stats
        print("\n📈 Getting index statistics...")
        stats = index.describe_index_stats()
        print(f"✅ Index stats retrieved")
        print(f"   Total Vectors: {stats.get('total_vector_count', 0):,}")
        print(f"   Dimension: {stats.get('dimension', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_pinecone()
