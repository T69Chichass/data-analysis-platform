#!/usr/bin/env python3
"""
Gemini-Only Document Analysis System
This system uses Gemini Pro for document analysis without Pinecone vector database.
"""

import tempenv
import os
import json
import time
from typing import List, Dict, Any
import google.generativeai as genai
from pathlib import Path

class GeminiDocumentAnalyzer:
    """Document analyzer using only Gemini Pro."""
    
    def __init__(self):
        """Initialize Gemini configuration."""
        self.api_key = os.environ.get('GEMINI_API_KEY')
        self.model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.max_tokens = int(os.environ.get('GEMINI_MAX_TOKENS', '1500'))
        self.temperature = float(os.environ.get('GEMINI_TEMPERATURE', '0.1'))
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        print(f"✅ Gemini configured with model: {self.model_name}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using basic text extraction."""
        try:
            import PyPDF2
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
                
                return text
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {e}")
            return ""
    
    def analyze_document(self, document_path: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze document using Gemini Pro."""
        
        print(f"📄 Analyzing document: {document_path}")
        
        # Extract text from document
        if document_path.lower().endswith('.pdf'):
            document_text = self.extract_text_from_pdf(document_path)
        else:
            # For other file types, read as text
            try:
                with open(document_path, 'r', encoding='utf-8') as file:
                    document_text = file.read()
            except Exception as e:
                return {"error": f"Could not read file: {e}"}
        
        if not document_text.strip():
            return {"error": "No text content found in document"}
        
        # Create analysis prompt based on type
        if analysis_type == "comprehensive":
            prompt = self._create_comprehensive_prompt(document_text)
        elif analysis_type == "summary":
            prompt = self._create_summary_prompt(document_text)
        elif analysis_type == "key_points":
            prompt = self._create_key_points_prompt(document_text)
        else:
            prompt = self._create_comprehensive_prompt(document_text)
        
        try:
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            if response.text:
                return {
                    "success": True,
                    "analysis_type": analysis_type,
                    "document": os.path.basename(document_path),
                    "analysis": response.text,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {"error": "No response generated from Gemini"}
                
        except Exception as e:
            return {"error": f"Gemini analysis failed: {e}"}
    
    def _create_comprehensive_prompt(self, text: str) -> str:
        """Create comprehensive analysis prompt."""
        return f"""
Please provide a comprehensive analysis of the following document. Structure your response as follows:

## Document Overview
- Document type and purpose
- Key themes and topics covered
- Overall structure and organization

## Key Findings
- Main points and important information
- Critical details and data points
- Significant insights

## Important Sections
- Breakdown of major sections
- Key content in each section
- Notable clauses or provisions

## Recommendations
- Action items or next steps
- Important considerations
- Areas requiring attention

## Summary
- Brief executive summary
- Most critical points

Document Content:
{text[:8000]}  # Limit text length for Gemini

Please provide a detailed, well-structured analysis that captures all important aspects of this document.
"""
    
    def _create_summary_prompt(self, text: str) -> str:
        """Create summary analysis prompt."""
        return f"""
Please provide a concise summary of the following document:

## Executive Summary
- Main purpose and scope
- Key points and findings
- Critical information

## Key Takeaways
- Most important points
- Essential details
- Action items

Document Content:
{text[:6000]}

Please provide a clear, concise summary that captures the essence of this document.
"""
    
    def _create_key_points_prompt(self, text: str) -> str:
        """Create key points analysis prompt."""
        return f"""
Please extract the key points from the following document:

## Key Points
- List the most important points
- Highlight critical information
- Note any deadlines or requirements

## Important Details
- Specific data, numbers, or dates
- Names, organizations, or entities
- Terms, conditions, or provisions

## Action Items
- What needs to be done
- Who is responsible
- When actions are due

Document Content:
{text[:6000]}

Please provide a focused list of key points and important details.
"""
    
    def batch_analyze(self, document_paths: List[str], analysis_type: str = "comprehensive") -> List[Dict[str, Any]]:
        """Analyze multiple documents."""
        results = []
        
        for i, doc_path in enumerate(document_paths, 1):
            print(f"\n📋 Processing document {i}/{len(document_paths)}: {os.path.basename(doc_path)}")
            
            result = self.analyze_document(doc_path, analysis_type)
            results.append(result)
            
            # Add small delay between requests
            time.sleep(1)
        
        return results
    
    def save_analysis(self, analysis: Dict[str, Any], output_path: str = None) -> str:
        """Save analysis results to file."""
        if output_path is None:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            doc_name = analysis.get('document', 'unknown').replace('.pdf', '').replace('.txt', '')
            output_path = f"analysis_{doc_name}_{timestamp}.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Analysis saved to: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
            return ""

def main():
    """Main function to demonstrate the system."""
    print("🤖 Gemini-Only Document Analysis System")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = GeminiDocumentAnalyzer()
        
        # Find PDF documents in current directory
        pdf_files = list(Path('.').glob('*.pdf'))
        
        if not pdf_files:
            print("❌ No PDF files found in current directory")
            print("💡 Please place your PDF documents in this folder")
            return
        
        print(f"📁 Found {len(pdf_files)} PDF document(s):")
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"   {i}. {pdf_file.name}")
        
        # Analyze each document
        for pdf_file in pdf_files:
            print(f"\n{'='*60}")
            print(f"📄 Analyzing: {pdf_file.name}")
            print(f"{'='*60}")
            
            # Perform comprehensive analysis
            result = analyzer.analyze_document(str(pdf_file), "comprehensive")
            
            if result.get("success"):
                print("\n📊 ANALYSIS RESULTS:")
                print("-" * 40)
                print(result["analysis"])
                
                # Save analysis
                analyzer.save_analysis(result)
            else:
                print(f"❌ Analysis failed: {result.get('error')}")
        
        print(f"\n🎉 Analysis complete! Check the generated JSON files for detailed results.")
        
    except Exception as e:
        print(f"❌ System error: {e}")

if __name__ == "__main__":
    main()
