#!/usr/bin/env python3
"""
Test script to test specific queries about the National Parivar Mediclaim Plus Policy.
"""
import asyncio
import json
from document_processor import DocumentProcessor
from dependencies import get_embedding_manager, get_pinecone_manager, get_openai_manager
from pathlib import Path

async def test_specific_queries():
    """Test the specific queries about the National Parivar Mediclaim Plus Policy."""
    
    pdf_path = "National_Parivar_Mediclaim_Plus_Policy.pdf"
    
    print("🔍 Testing specific queries for National Parivar Mediclaim Plus Policy...")
    
    # First, process the document
    processor = DocumentProcessor()
    
    try:
        # Process the document
        print("1. Processing document...")
        result = await processor.process_document(
            file_path=pdf_path,
            document_type="insurance_policy",
            category="health_insurance",
            metadata={"title": "National Parivar Mediclaim Plus Policy"}
        )
        print(f"   ✅ Document processed: {result['document_id']}")
        print(f"   📄 Text length: {result['text_length']} characters")
        print(f"   📦 Chunks created: {result['chunk_count']}")
        
        # Define the specific queries
        queries = [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?",
            "What is the No Claim Discount (NCD) offered in this policy?",
            "Is there a benefit for preventive health check-ups?",
            "How does the policy define a 'Hospital'?",
            "What is the extent of coverage for AYUSH treatments?",
            "Are there any sub-limits on room rent and ICU charges for Plan A?"
        ]
        
        # Test each query
        print("\n2. Testing specific queries...")
        
        embedding_manager = get_embedding_manager()
        pinecone_manager = get_pinecone_manager()
        openai_manager = get_openai_manager()
        
        for i, query in enumerate(queries, 1):
            print(f"\n--- Query {i}: {query} ---")
            
            try:
                # Generate embedding for the query
                query_embedding = embedding_manager.encode(query)
                
                # Search for similar chunks (in mock mode, this will return empty)
                if pinecone_manager.mock_mode:
                    print("   🔍 Pinecone in mock mode - using mock search")
                    # For mock mode, let's simulate by searching through the document text
                    extracted_text = await processor._extract_text_from_pdf(Path(pdf_path))
                    
                    # Simple keyword-based search for relevant sections
                    query_lower = query.lower()
                    relevant_sections = []
                    
                    # Split text into paragraphs and search for relevant ones
                    paragraphs = extracted_text.split('\n\n')
                    for para in paragraphs:
                        if any(keyword in para.lower() for keyword in query_lower.split()):
                            relevant_sections.append(para[:500] + "..." if len(para) > 500 else para)
                    
                    if relevant_sections:
                        print(f"   📄 Found {len(relevant_sections)} relevant sections")
                        for j, section in enumerate(relevant_sections[:3], 1):
                            print(f"   Section {j}: {section[:200]}...")
                    else:
                        print("   ❌ No relevant sections found")
                        
                else:
                    # Real Pinecone search
                    search_results = await pinecone_manager.search_similar(query_embedding, top_k=5)
                    print(f"   🔍 Found {len(search_results)} similar chunks")
                
                # Generate response (in mock mode)
                if openai_manager.mock_mode:
                    print("   🤖 OpenAI in mock mode - generating mock response")
                    # Create a mock response based on the query
                    mock_responses = {
                        "grace period": "The grace period for premium payment is typically 30 days from the due date.",
                        "waiting period": "The waiting period for pre-existing diseases is usually 2-4 years depending on the policy.",
                        "maternity": "Maternity expenses are generally not covered under standard health insurance policies.",
                        "cataract": "The waiting period for cataract surgery is typically 2 years.",
                        "organ donor": "Medical expenses for organ donors are usually covered under the policy.",
                        "no claim discount": "No Claim Discount (NCD) is offered for claim-free years, typically 5-10% per year.",
                        "preventive health": "Preventive health check-ups are usually covered once per year.",
                        "hospital": "A hospital is defined as a facility with 15 or more beds and registered with local authorities.",
                        "ayush": "AYUSH treatments are covered up to a specified limit, usually 10-15% of sum insured.",
                        "room rent": "There are sub-limits on room rent and ICU charges, typically 1-2% of sum insured per day."
                    }
                    
                    # Find the most relevant mock response
                    best_match = "Information not found in the document."
                    for keyword, response in mock_responses.items():
                        if keyword in query.lower():
                            best_match = response
                            break
                    
                    print(f"   💬 Mock Response: {best_match}")
                else:
                    # Real OpenAI response
                    print("   🤖 Generating OpenAI response...")
                    # This would use the real OpenAI API
                
            except Exception as e:
                print(f"   ❌ Error processing query: {e}")
        
        print("\n✅ Query testing completed!")
        
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_specific_queries())
