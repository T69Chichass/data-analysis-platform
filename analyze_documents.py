#!/usr/bin/env python3
"""
Simple Document Analysis with Gemini Pro
Interactive script to analyze documents without Pinecone.
"""

import tempenv
import os
import json
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

def analyze_with_gemini(model, text, analysis_type="comprehensive"):
    """Analyze text using Gemini."""
    
    if analysis_type == "comprehensive":
        prompt = f"""
Please provide a comprehensive analysis of this document:

## Document Overview
- Document type and purpose
- Key themes and topics covered

## Key Findings
- Main points and important information
- Critical details and data points

## Important Sections
- Breakdown of major sections
- Key content in each section

## Summary
- Brief executive summary
- Most critical points

Document Content:
{text[:8000]}

Provide a detailed, well-structured analysis.
"""
    elif analysis_type == "summary":
        prompt = f"""
Please provide a concise summary of this document:

## Executive Summary
- Main purpose and scope
- Key points and findings

## Key Takeaways
- Most important points
- Essential details

Document Content:
{text[:6000]}

Provide a clear, concise summary.
"""
    else:  # key_points
        prompt = f"""
Please extract key points from this document:

## Key Points
- Most important points
- Critical information

## Important Details
- Specific data, numbers, dates
- Names, organizations, terms

## Action Items
- What needs to be done
- Deadlines or requirements

Document Content:
{text[:6000]}

Provide focused key points and details.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Analysis failed: {e}"

def main():
    """Main interactive function."""
    print("🤖 Document Analysis with Gemini Pro")
    print("=" * 40)
    
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
    
    # Analysis types
    analysis_types = {
        "1": "comprehensive",
        "2": "summary", 
        "3": "key_points"
    }
    
    print(f"\n📊 Analysis Types:")
    print("   1. Comprehensive Analysis")
    print("   2. Summary")
    print("   3. Key Points")
    
    # Get user choice
    choice = input("\n🎯 Choose analysis type (1-3): ").strip()
    analysis_type = analysis_types.get(choice, "comprehensive")
    
    print(f"\n🔍 Using analysis type: {analysis_type}")
    
    # Process each document
    for pdf_file in pdf_files:
        print(f"\n{'='*60}")
        print(f"📄 Processing: {pdf_file.name}")
        print(f"{'='*60}")
        
        # Extract text
        print("📖 Extracting text from PDF...")
        text = extract_pdf_text(pdf_file)
        
        if not text.strip():
            print("❌ No text content found in PDF")
            continue
        
        print(f"✅ Extracted {len(text)} characters of text")
        
        # Analyze with Gemini
        print("🤖 Analyzing with Gemini Pro...")
        analysis = analyze_with_gemini(model, text, analysis_type)
        
        if analysis:
            print(f"\n📊 ANALYSIS RESULTS:")
            print("-" * 40)
            print(analysis)
            
            # Save results
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"analysis_{pdf_file.stem}_{timestamp}.txt"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Document: {pdf_file.name}\n")
                    f.write(f"Analysis Type: {analysis_type}\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(analysis)
                
                print(f"\n✅ Analysis saved to: {output_file}")
            except Exception as e:
                print(f"❌ Error saving analysis: {e}")
        else:
            print("❌ Analysis failed")
    
    print(f"\n🎉 All documents processed!")

if __name__ == "__main__":
    main()
