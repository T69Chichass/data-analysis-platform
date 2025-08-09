#!/usr/bin/env python3
"""
Test script to verify Gemini integration works independently
"""

import tempenv
from dependencies import get_gemini_manager

def test_gemini_response():
    """Test Gemini response generation."""
    print("🧪 Testing Gemini Response Generation")
    print("=" * 50)
    
    try:
        # Get Gemini manager
        manager = get_gemini_manager()
        print(f"✅ Gemini Manager initialized: {type(manager)}")
        print(f"   Mock Mode: {manager.mock_mode}")
        
        if not manager.mock_mode:
            print(f"   API Key: {manager.api_key[:10]}...")
            print(f"   Model: {manager.model}")
            print(f"   Max Tokens: {manager.max_tokens}")
            print(f"   Temperature: {manager.temperature}")
            
            # Test a simple response
            print("\n🔍 Testing basic response generation...")
            test_prompt = "Say hello in a friendly way"
            response = manager.model.generate_content(test_prompt)
            print(f"✅ Response: {response.text.strip()}")
            
            # Test document analysis prompt
            print("\n📄 Testing document analysis prompt...")
            doc_prompt = """You are an AI assistant designed to analyze legal and policy documents with high accuracy and provide clear, well-reasoned answers.

CORE TASK:
Analyze the provided document excerpts to answer the following user query with precision and clarity.

USER QUERY:
What is the grace period for premium payment?

[CONTEXT]
Document 1 (ID: doc_001):
The grace period for premium payment is 30 days from the due date. During this period, the policy remains in force, but any claims arising during the grace period may be subject to the outstanding premium being paid.
Relevance Score: 0.950

INSTRUCTIONS:
1. Do NOT use any external knowledge beyond what is provided in the context above
2. If the answer cannot be found in the provided context, state this clearly
3. Base your answer ONLY on the document excerpts provided
4. Identify specific clauses, sections, or excerpts that support your answer
5. Provide clear reasoning for your conclusions
6. Assess your confidence level in the answer (high/medium/low)

RESPONSE FORMAT:
Provide your response as a single JSON object with the following structure:
{
    "answer": "Your clear and concise answer to the user's question",
    "supporting_clauses": [
        {
            "text": "Exact text from the document that supports your answer",
            "document_id": "The document ID from the context",
            "confidence_score": 0.85
        }
    ],
    "explanation": "Detailed explanation of your reasoning and how you arrived at this answer",
    "confidence": "high/medium/low - your overall confidence in this answer"
}

IMPORTANT: Respond ONLY with the JSON object. Do not include any other text, markdown formatting, or explanations outside the JSON structure."""
            
            response = manager.model.generate_content(doc_prompt)
            print(f"✅ Document Analysis Response: {response.text.strip()}")
            
        else:
            print("   ⚠️ Running in mock mode")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_gemini_response()
