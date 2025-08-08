#!/usr/bin/env python3
"""
Test script to debug document upload issue.
"""
import asyncio
from document_processor import DocumentProcessor
import tempfile
import shutil
from pathlib import Path

async def test_document_processing():
    """Test document processing step by step."""
    
    pdf_path = "National_Parivar_Mediclaim_Plus_Policy.pdf"
    
    print("🔍 Testing document processing...")
    
    # Test 1: Check if file exists
    print(f"1. File exists: {Path(pdf_path).exists()}")
    
    # Test 2: Extract text directly
    print("2. Testing text extraction...")
    processor = DocumentProcessor()
    
    try:
        extracted_text = await processor._extract_text_from_pdf(Path(pdf_path))
        print(f"   ✅ Text extracted: {len(extracted_text)} characters")
        print(f"   ✅ Stripped length: {len(extracted_text.strip())} characters")
        print(f"   ✅ First 100 chars: {repr(extracted_text[:100])}")
        
        if not extracted_text.strip():
            print("   ❌ ERROR: No text content after stripping!")
        else:
            print("   ✅ Text content is valid")
            
    except Exception as e:
        print(f"   ❌ Text extraction failed: {e}")
        return
    
    # Test 3: Test full document processing
    print("3. Testing full document processing...")
    
    try:
        result = await processor.process_document(
            file_path=pdf_path,
            document_type="insurance_policy",
            category="health_insurance",
            metadata={"title": "National Parivar Mediclaim Plus Policy"}
        )
        print(f"   ✅ Document processing successful: {result}")
        
    except Exception as e:
        print(f"   ❌ Document processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_document_processing())
