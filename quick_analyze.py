#!/usr/bin/env python3
"""
Quick Document Analysis with Gemini Pro
Automatically analyzes all PDF documents in the current directory.
"""

import tempenv
import os
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

def analyze_with_gemini(model, text):
    """Analyze text using Gemini with comprehensive analysis."""
    
    prompt = f"""
Please provide a comprehensive analysis of this insurance policy document:

## Document Overview
- Document type and purpose
- Insurance company and policy details
- Key themes and coverage areas

## Policy Details
- Policy number and holder information
- Coverage limits and benefits
- Premium amounts and payment terms
- Policy period and renewal terms

## Key Coverage Areas
- What is covered under the policy
- Exclusions and limitations
- Claim procedures and requirements
- Important terms and conditions

## Critical Information
- Important deadlines or requirements
- Contact information for claims
- Documents needed for claims
- Special conditions or riders

## Summary
- Brief executive summary
- Most critical points for policyholder
- Action items or next steps

Document Content:
{text[:8000]}

Provide a detailed, well-structured analysis that helps understand the policy clearly.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Analysis failed: {e}"

def main():
    """Main function to analyze all documents."""
    print("🤖 Quick Document Analysis with Gemini Pro")
    print("=" * 50)
    
    # Setup Gemini
    model = setup_gemini()
    if not model:
        return
    
    # Find PDF files
    pdf_files = list(Path('.').glob('*.pdf'))
    
    if not pdf_files:
        print("❌ No PDF files found in current directory")
        print("💡 Please place your PDF documents in this folder")
        return
    
    print(f"\n📁 Found {len(pdf_files)} PDF document(s):")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file.name}")
    
    print(f"\n🔍 Starting comprehensive analysis...")
    
    # Process each document
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n{'='*70}")
        print(f"📄 Processing Document {i}/{len(pdf_files)}: {pdf_file.name}")
        print(f"{'='*70}")
        
        # Extract text
        print("📖 Extracting text from PDF...")
        text = extract_pdf_text(pdf_file)
        
        if not text.strip():
            print("❌ No text content found in PDF")
            continue
        
        print(f"✅ Extracted {len(text)} characters of text")
        
        # Analyze with Gemini
        print("🤖 Analyzing with Gemini Pro...")
        analysis = analyze_with_gemini(model, text)
        
        if analysis and not analysis.startswith("❌"):
            print(f"\n📊 ANALYSIS RESULTS:")
            print("-" * 50)
            print(analysis)
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"analysis_{pdf_file.stem}_{timestamp}.txt"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Document: {pdf_file.name}\n")
                    f.write(f"Analysis Type: Comprehensive Insurance Policy Analysis\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    f.write(analysis)
                
                print(f"\n✅ Analysis saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving analysis: {e}")
        else:
            print(f"❌ Analysis failed: {analysis}")
        
        # Add delay between documents
        if i < len(pdf_files):
            print("\n⏳ Waiting 2 seconds before next document...")
            time.sleep(2)
    
    print(f"\n🎉 All documents processed!")
    print(f"📁 Check the generated analysis files for detailed results.")

if __name__ == "__main__":
    main()
