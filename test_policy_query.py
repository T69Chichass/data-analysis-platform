#!/usr/bin/env python3
"""
Test Policy Query with Gemini Pro
Downloads policy PDF from URL and answers specific questions.
"""

import tempenv
import os
import requests
import time
from pathlib import Path
import google.generativeai as genai

def setup_gemini():
    """Setup Gemini configuration."""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment")
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    print("✅ Gemini configured successfully")
    return model

def download_pdf(url, filename="policy.pdf"):
    """Download PDF from URL."""
    try:
        print(f"📥 Downloading PDF from: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ PDF downloaded successfully: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")
        return None

def extract_pdf_text(pdf_path):
    """Extract text from PDF."""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(reader.pages):
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def answer_questions_with_gemini(model, text, questions):
    """Answer specific questions using Gemini."""
    
    prompt = f"""
You are an expert insurance policy analyst. Please answer the following specific questions about this insurance policy document.

IMPORTANT: Answer each question based ONLY on the information provided in the document. If the information is not available in the document, clearly state "Information not found in the document."

Document Content:
{text[:10000]}

Questions to Answer:

"""
    
    for i, question in enumerate(questions, 1):
        prompt += f"{i}. {question}\n"
    
    prompt += """

Please provide clear, accurate answers to each question. Format your response as:

## Question 1: [Question]
**Answer:** [Your answer based on the document]

## Question 2: [Question]
**Answer:** [Your answer based on the document]

[Continue for all questions...]

If any information is not explicitly mentioned in the document, state "Information not found in the document" for that question.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Analysis failed: {e}"

def main():
    """Main function to test the policy query."""
    print("🤖 Testing Policy Query with Gemini Pro")
    print("=" * 50)
    
    # Setup Gemini
    model = setup_gemini()
    if not model:
        return
    
    # Test query data
    test_query = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
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
    }
    
    print(f"📋 Testing {len(test_query['questions'])} questions about the policy")
    
    # Download PDF
    pdf_filename = download_pdf(test_query['documents'])
    if not pdf_filename:
        print("❌ Could not download PDF. Exiting.")
        return
    
    # Extract text
    print("📖 Extracting text from PDF...")
    text = extract_pdf_text(pdf_filename)
    
    if not text.strip():
        print("❌ No text content found in PDF")
        return
    
    print(f"✅ Extracted {len(text)} characters of text")
    
    # Answer questions
    print("🤖 Analyzing policy and answering questions...")
    answers = answer_questions_with_gemini(model, text, test_query['questions'])
    
    if answers and not answers.startswith("❌"):
        print(f"\n📊 POLICY ANALYSIS RESULTS:")
        print("=" * 60)
        print(answers)
        
        # Save results
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        output_file = f"policy_analysis_{timestamp}.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Policy Analysis Results\n")
                f.write("=" * 30 + "\n\n")
                f.write(f"Document URL: {test_query['documents']}\n")
                f.write(f"Analysis Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(answers)
            
            print(f"\n✅ Analysis saved to: {output_file}")
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
    else:
        print(f"❌ Analysis failed: {answers}")
    
    # Clean up downloaded file
    try:
        os.remove(pdf_filename)
        print(f"🧹 Cleaned up temporary file: {pdf_filename}")
    except:
        pass
    
    print(f"\n🎉 Policy query test completed!")

if __name__ == "__main__":
    main()
